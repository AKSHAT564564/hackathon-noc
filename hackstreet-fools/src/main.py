import os
from json import load
from jira import JIRA
from twilio.rest import Client
from build_config import fetch_recipients_from_gsheet
from send_message import send_message_to_recipient
from firebase_utils import performTicketOperations

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_FILE_PATH = ROOT_DIR + '/configuration/config.json'
with open(CONFIG_FILE_PATH, 'r') as config_file:
    data = load(config_file)


# Initialize Jira API
jira = JIRA(
    server=data["SERVER_NAME"],
    basic_auth=(data["JIRA_AUTH_MAIL"], data["JIRA_AUTH_TOKEN"])
)

# TODO - configuration for columns to get numbers from

# Initialize Twilio API
account_sid = data["TWILIO_ACCOUNT_SID"]
auth_token = data["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# JQL query to fetch all tickets in projects that start with 'NOC' and have priority 'Major'
query = 'project=NOC AND priority in (Major, Blocker, Critical) AND status=Open'
# Fetch all issues matching the JQL query
issues = jira.search_issues(query)
# Print the details of each issue
for issue in issues:
   #  We'll check how many times this issue has been informed to the engineering team
   #  We'll fetch the count number from the Firebase connected to the issue Id/key
   #  If this number is less than 3, then we'll send the notification/alert to again the 4 levels
   #  >3 that means ab unke boss ko contact karna h, that means the first column.
    print("Issue ID : " + issue.key)
    performTicketOperations(issue, client)
