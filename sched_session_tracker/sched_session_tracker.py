import requests
import json
from sched_session_tracker.googlesheet import GoogleSheetAPI
import re

class SchedSessionTracker:
    def __init__(self, schedURL, googleSheetObj, verbose=True, configFile="config.json",secretsFile="API_KEY.secret"):
        # Verbosity Setting
        self._verbose = verbose
        # Config File name
        self.config_file_name = configFile
        # Secrets File name
        self.secrets_file_name = secretsFile
        # Store the url for the sched event
        self.schedURL = "https://linaroconnectsandiego.sched.com/"
        # Creates a new instance of the GoogleSheetAPI
        self.googleSheet = GoogleSheetAPI(googleSheetObj["sheetID"], googleSheetObj["sheetName"])
        # Sched REST API endpoint
        self.apiEndpoint = "/api/session/list?api_key={0}&since=1282755813&format=json"
        # Get the sched_session_tracker config
        self.config_settings = self.load_config(self.config_file_name)
        # Fetch Secret API Key
        self.API_KEY = self.load_secrets(self.secrets_file_name)
        # Run the main method
        self.main()

    def main(self):
        self.schedData = self.get_api_results(self.apiEndpoint)
        formatted_results  = self.formatResultsUsingConfig(self.schedData, self.config_settings[0]["structure"])
        self.crudGoogleSheet(formatted_results)

    def load_secrets(self, secretsFile):
        """Loads secrets"""
        with open(secretsFile) as secrets:
            return secrets.readline().rstrip('\n')

    def load_config(self, config_file_name):
        """Loads the config.json file"""
        try:
            if self._verbose:
                print("Loading sched_session_tracker config from config.json...")
            with open(config_file_name) as json_file:
                settings = json.load(json_file)
                return settings
        except Exception as e:
            if self._verbose:
                print(e)


    def formatResultsUsingConfig(self, data, config):
        """
        This method formats the Sched API results using the supplied config.json file. Fore more info please read the docs at https://github.com/linaro-marketing/sched_session_tracker
        """
        google_sheet_rows = []
        for entry in data:
            new_googlesheet_row = {}
            for configEntry in config:
                # Check to see if the config entry contains a sched_key
                try:
                    if configEntry["sched_key"]:
                        if configEntry["store_key"]:
                            try:
                                regex = configEntry["regex_match"]
                                var_regex = re.compile(configEntry["regex_match"])
                                var_val_regex = var_regex.findall(entry[configEntry["sched_key"]])[0]
                                try:
                                    if configEntry['force_lower'] == True:
                                        var_val_regex = var_val_regex.lower()
                                except KeyError as e:
                                    pass
                                new_googlesheet_row[configEntry["store_key"]] = var_val_regex
                            except Exception as e:
                                new_googlesheet_row[configEntry["store_key"]] = entry[configEntry["sched_key"]]
                        else:
                            new_googlesheet_row[configEntry["sched_key"]] = entry[configEntry["sched_key"]]
                except KeyError as e:
                    # If no sched_key is present then check if the store_key is set
                    try:
                        if configEntry["store_key"]:
                            # See if the configEntry has a variable sub included
                            if "[" in configEntry["value"]:
                                # Find the variable sub in the configEntries value field
                                var_name = configEntry["value"].split("[")[1]
                                var_name = var_name.split("]")[0]
                                # Get the var val from the already set related
                                var_val = new_googlesheet_row["{0}".format(var_name)]
                                replace_val = configEntry["value"].replace("[{0}]".format(var_name), var_val)
                                new_googlesheet_row[configEntry["store_key"]] = replace_val
                            # Not yet applicable/implemented
                            else:
                                new_googlesheet_row[configEntry["store_key"]] = ""
                    except KeyError as e:
                        print("Config entry is missing a store key...")
                        break
            google_sheet_rows.append(new_googlesheet_row)
        return google_sheet_rows

    def numberToCharacter(self, number):
        """Returns the column character for google sheet based on length of headers array"""
        return chr(26 + (38 + number))


    def crudGoogleSheet(self, formatted_data):
        """Takes the sched export data and adds to the Google Sheet"""
        headers = self.getHeaders(formatted_data)
        print(headers)
        columnChar = self.numberToCharacter(len(headers))
        data_length = len(formatted_data) + 1
        sheet_range = "A2:{0}{1}".format(columnChar,data_length)
        print(sheet_range)

        data = []
        for entry in formatted_data:
            dataEntry = []
            for item in entry:
                dataEntry.append(entry[item])
            data.append(dataEntry)
        print(data)
        print("Adding initial google sheet data")
        self.googleSheet.updateValues(sheet_range, data)


    def getHeaders(self, results):
        first_entry = results[0]
        headers = []
        for key, value in first_entry.items():
            headers.append(key)
        return headers

    def get_api_results(self, endpoint):
        """
            Gets the results from a specified endpoint
        """
        endpoint = self.schedURL + endpoint.format(self.API_KEY)
        if self._verbose:
            print("Fetching Sched.com data from {0}".format(endpoint))
        try:
            resp = requests.get(url=endpoint)
            data = resp.json()
            return data
        except Exception as e:
            print(e)
            return False
