from __future__ import print_function
from os import path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time

class cmd_flags(object):
    """
        Used to provide command-line level authentication rather than
        working through a web browser.
    """

    def __init__(self):
        self.auth_host_name = 'localhost'
        self.auth_host_port = [8080, 8090]
        self.logging_level = 'ERROR'
        self.noauth_local_webserver = True

class GoogleSheetAPI:

    """
        This class interacts with a Google Sheet to retreive and update cell values
    """

    def __init__(self, sheetID, sheetName, interactive=False):
        # If modifying these scopes, delete the file token.json.
        self._scopes = 'https://www.googleapis.com/auth/spreadsheets'
        # The ID and range of a sample spreadsheet.
        self._spreadsheet_id = sheetID
        self._sheet_name = sheetName
        # Update this with the name of your client secrets.json export from your Google cloud console project.
        self._client_secret_file = "client_secret_384596001461-l747m0qou2kaf8cjai01cq1mdna6rs8a.apps.googleusercontent.com.json"
        # Get a new service object upon instantiation of the GoogleSheetAPI object
        self.service = self.getGoogleSheetServiceObject(interactive)
        self._value_input_option = ["USER_ENTERED", "RAW"]

    def getGoogleSheetServiceObject(self, interactive):
        """Create a new Google Sheets service object"""
        if not interactive and not path.isfile('token.json'):
            raise FileNotFoundError(
                "Run googlesheet interactively to create authentication token.")
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                self._client_secret_file, self._scopes)
            flow.user_agent = "Connect Automation"
            creds = tools.run_flow(flow, store, cmd_flags())
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        return service

    def getValuesFromRange(self, my_range):
        # Call the Sheets API
        result = self.service.spreadsheets().values().get(spreadsheetId=self._spreadsheet_id,
                                                          range=my_range).execute()
        values = result.get('values', [])
        return values

    def getAllValues(self):
        result = self.getValuesFromRange("A1:B")
        return result

    def updateValues(self, range_name, values):
        body = {
            "valueInputOption": self._value_input_option[0] ,
            "data": [
                    {
                    "range": range_name,
                    "majorDimension": "ROWS",
                    "values": values
                }
            ]
        }
        result = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id, body=body).execute()

        return result

    def updateGoogleSheet(self, missing_presentations):

        sheet_range = "A2:B{0}".format(len(missing_presentations))
        data = []
        for each in missing_presentations:
            session_id = each[0]
            speakers = each[1]
            email_list = ""
            if speakers != None:
                for speaker in speakers:
                    email_list += speaker["email"] + ","
                email_list.rstrip(",")
            data.append([session_id, email_list[0:-1]])
        print(data)
        input()
        self.updateValues(sheet_range, data)


if __name__ == '__main__':
    api = GoogleSheetAPI(False, False, True)
