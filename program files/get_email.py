import base64
import os.path
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from sys import platform

# Define the scopes for Gmail and Google Drive APIs
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

# Set the user ID for the Gmail account
user_id = 'me'

# Define a search query to find messages with attachments
query = 'from:uctenky@smichoff.cz'

# Define the directory to save attachments to
if platform == 'win' or 'win32' or 'win64':
    save_dir = os.getcwd() + '\\Photos_for_scan\\'
else:
    save_dir = os.getcwd() + '/Photos_for_scan/'

def main():
    # Get the API credentials from the token.json file
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    try:
        # Build the Gmail API client
        service = build('gmail', 'v1', credentials=creds)

        # Use the Gmail API to search for messages with attachments
        messages = []
        response = service.users().messages().list(userId=user_id,q=query,).execute()
        if 'messages' in response:
            messages.extend(response['messages'])
        
        attachments = []
        for message in messages:
            msg = service.users().messages().get(userId=user_id,  id=message['id']).execute()
            if 'parts' in msg['payload']:
                parts = msg['payload']['parts']
                for part in parts:
                    filename = part.get('filename')
                    if filename:
                        att_id = part['body']['attachmentId']
                        att = service.users().messages().attachments().get(userId=user_id, messageId=message['id'], id=att_id).execute()
                        attachments.append({'messageId': message['id'], 'filename': filename, 'data': att['data']})

        # Download attachments for each message with attachments
        for att in attachments:
            message = service.users().messages().get(userId=user_id, id=att['messageId']).execute()
            headers = message['payload']['headers']
            for header in headers:
                if header['name'] == 'From':
                    sender = header['value']
                if header['name'] == 'Subject':
                    subject = header['value']
            file_data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
            path = ''.join([save_dir, att['filename']])
            with open(path, 'wb') as f:
                f.write(file_data)
            print(f'Saved attachment {att["filename"]} from {sender} with subject "{subject}"')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
