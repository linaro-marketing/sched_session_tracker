import requests
from sched_session_tracker.googlesheet import GoogleSheetAPI

class SchedSessionTracker:
    def __init__(self, schedURL, googleSheetObj, secretFile="API_KEY.secret"):
        # Store the url for the sched event
        self.schedURL = "https://linaroconnectsandiego.sched.com/"
        # Creates a new instance of the GoogleSheetAPI
        self.googleSheet = GoogleSheetAPI(googleSheetObj["sheetID"], googleSheetObj["sheetName"])
        # Sched REST API endpoint
        self.apiEndpoint = "/api/session/list?api_key={0}&since=1282755813&format=json"
        # Fetch Secret API Key
        api_secret_file = open(secretFile)
        self.API_KEY = api_secret_file.readline()
        api_secret_file.close()

    def fetchData():
        """This method fetches the latest session data from the Sched API"""
        pass

    def get_api_results(self, endpoint):
        """
            Gets the results from a specified endpoint
        """
        endpoint = self.sched_url + endpoint.format(self.API_KEY)
        try:
            resp = requests.get(url=endpoint)
            data = resp.json()
            return data
        except Exception as e:
            print(e)
            return False
