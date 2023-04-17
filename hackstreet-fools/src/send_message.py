def message_body_builder(issue) :
   # manipulate issue so that we extract the main content from the issue
   # title + 500 chars of description + ticketid
   title = issue.fields.summary
   desc = issue.fields.description
   ticket_id = issue.key
   assignee = issue.fields.assignee.displayName
   msg = 'Title : ' + title + '\n'
   msg += 'Ticket ID : ' + ticket_id + '\n'
   msg += 'Assignee : ' + assignee + '\n'
   if(len(desc) < 500):
      msg += 'Description : ' + desc[:len(desc)] + '\n\n'
   else:
      msg += 'Description : ' + desc[:500] + '\n\n'

   msg += "PLEASE MARK THE TICKET AS IN PROGRESS, IF YOU ARE GOING TO WORK ON IT!"
   return msg

def send_message_to_recipient(client, list_of_recipients, issue) :
   msg_body = message_body_builder(issue)
   for recipient in list_of_recipients:
      try :
         message = client.messages.create(
         from_='whatsapp:+14155238886',
         body=msg_body,
         to='whatsapp:+91' + recipient
         )
         print("Whatsapp message sent to --> " + recipient + " --> " + message.sid)
      except :
         print("Whatsapp message was not sent to --> " + recipient)
         print("Sending text message to --> " + recipient)
         try :
            message = client.messages.create(
               from_='whatsapp:+14155238886',
               body = msg_body,
               to='+91' + recipient
            )
            print("Text message sent to --> " + recipient)
         except :
            print("Text message was not sent to --> " + recipient)