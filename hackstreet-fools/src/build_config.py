import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def check_NA(str) :
    return str.lower().replace(" ", "") == "na"

def add_to_recipient_list(list_of_recipients, row, col1, col2) :
    print(row[col1-1] + ' --> ' + row[col1])
    print(row[col2-1] + ' --> ' + row[col2])
    if check_NA(row[col1]) == False :
        list_of_recipients.append(row[col1].replace("-", ""))
    if check_NA(row[col2]) == False :
        list_of_recipients.append(row[col2].replace("-", ""))

def fetch_recipients_from_gsheet(team_name, count) :
    # set up Google Sheets client
    print(team_name)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
    ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    CRED_FILE = ROOT_DIR + '/configuration/credentials.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(CRED_FILE, scope)
    client = gspread.authorize(creds)
    # open the Google Sheet
    sheet = client.open('Escalation Matrix').worksheet('Sheet1')
    # Iterate over rows we'll check the first column.
    # First column & team name --> string --> spaces remove --> lower case
    # If they match then, we'll pull the column values based on the count.
    all_data = sheet.get_all_values()
    list_of_recipients = []
    for row in all_data:
        team_name_on_sheet = row[0].strip()
        if team_name.lower().replace(" ", "") == team_name_on_sheet.lower().replace(" ", "") :
            print("Found a match.")
            if count <= 3 :
                add_to_recipient_list(list_of_recipients, row, 3, 5)
            elif count > 3 and count <= 5:
                add_to_recipient_list(list_of_recipients, row, 7, 9)

    return list_of_recipients


