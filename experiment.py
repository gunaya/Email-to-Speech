from __future__ import print_function

import base64
import time

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools, client
from gtts import gTTS
import pygame
from langdetect import detect

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def get_sender():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials_dummy.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    results = service.users().messages().list(userId='me', labelIds=['UNREAD', 'CATEGORY_PERSONAL', 'INBOX'],
                                              maxResults=1).execute()
    message_id = results['messages'][0]['id']
    message = service.users().messages().get(userId='me', id=message_id).execute()

    mesega = message['payload']['headers']
    sender = mesega[16]['value']

    return sender


def get_message():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials_dummy.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=['UNREAD', 'CATEGORY_PERSONAL', 'INBOX'],
                                              maxResults=1).execute()

    # get the message id from the results object
    message_id = results['messages'][0]['id']

    # use the message id to get the actual message, including any attachments
    message = service.users().messages().get(userId='me', id=message_id).execute()

    # now the message object contains the entire recent message
    mesega = message['payload']['parts']
    msg_raw = mesega[0]['body']['data']

    # decode base64
    msg_clean = msg_raw.replace("-", "+")
    msg_clean = msg_clean.replace("_", "/")

    msg_clean = base64.b64decode(msg_clean)

    # remove  b' \r \r
    message_final = msg_clean.decode().strip()

    # deteksi bahasa
    lang = detect(message_final)
    if lang == 'id':
        language = 'id'
    elif lang == 'en':
        language = 'en'
    else:
        language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=message_final, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    myobj.save("email.mp3")

    return message_final

def play_audio():
    # Playing the converted file
    pygame.mixer.init()
    pygame.mixer.music.load('email.mp3')
    pygame.mixer.music.play()
    time.sleep(0)

if __name__ == "__main__":
    get_sender()