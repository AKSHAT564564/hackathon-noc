import firebase_admin
from firebase_admin import credentials
from twilio.rest import Client
from firebase_admin import firestore
from jira import JIRA
from datetime import datetime, timedelta
from build_config import fetch_recipients_from_gsheet
from send_message import send_message_to_recipient
from json import load
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_FILE_PATH = ROOT_DIR + '/configuration/config.json'
FIREBASE_FILE_PATH = ROOT_DIR + '/configuration/firebase-key.json'
with open(CONFIG_FILE_PATH, 'r') as config_file:
    data = load(config_file)

cred = credentials.Certificate(FIREBASE_FILE_PATH)
firebase_admin.initialize_app(cred,{
    'databaseURL': data["FIREBASE_DB_URL"]
})
db = firestore.client()


class TicketData:
    def __init__(self,ticketId: str, escalationLevel: int, status: str, updatedAt: datetime, lastMessageSentAt: datetime):
        self.ticketId = ticketId
        self.escalationLevel = escalationLevel
        self.status = status
        self.updatedAt = updatedAt
        self.lastMessageSentAt = lastMessageSentAt

def checkTimeDiffOfOneHour(timeStamp):
    timeStamp_datetime = datetime.strptime(timeStamp.strftime('%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')
    time_diff = datetime.now() - timeStamp_datetime
    return time_diff > timedelta(hours=1)

def checkEscalationLevel(client, ticket_data, issue):
    lastMessageSentAt = ticket_data['lastMessageSentAt']
    if(checkTimeDiffOfOneHour(lastMessageSentAt)):
       escalation_level = ticket_data['escalationLevel'] + 1
       sendMessageHandler(client, issue, escalation_level)
       updateTicketData(ticket_data, escalation_level)
    else:
        return

def performTicketOperations(issue, client):
    ticket_doc_ref = db.collection('noc-tickets').document(issue.key)
    ticket_doc = ticket_doc_ref.get()
    if ticket_doc.exists:
      ticket_data = ticket_doc.to_dict()
      checkEscalationLevel(client, ticket_data,issue)
    else:
        sendMessageHandler(client, issue, 1)
        ticket_doc_ref.set({
        'ticketId': issue.key,
        'escalationLevel': 1,
        'updatedAt': datetime.now(),
        'lastMessageSentAt': datetime.now()
        })

def sendMessageHandler(client, issue, escalation_level):
       lst_of_recievers = fetch_recipients_from_gsheet(issue.fields.customfield_16578.value, escalation_level)
       send_message_to_recipient(client, lst_of_recievers, issue)

def updateTicketData(initial_data, escalation_level):
    ticket_doc_ref = db.collection('noc-tickets').document(initial_data['ticketId'])
    ticket_doc_ref.update({
        'escalationLevel': escalation_level,
        'updatedAt': datetime.now(),
        'lastMessageSentAt': datetime.now()
    })
