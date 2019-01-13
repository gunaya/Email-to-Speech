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

class email2speak:
    def gmail_api(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
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

        # print(message)
        return message

    def get_sender(self):
        message = self.gmail_api()
        if message is None:
            sender = 'none'
        else:
            mesega = message['payload']['headers']
            sender = mesega[16]['value']
        return sender

    def get_message(self):
        message = self.gmail_api()
        if message is None:
            message_final = 'none'
        else:
            # now the message object contains the entire recent message
            mesega = message['payload']['parts']
            msg_raw = mesega[0]['body']['data']

            #decode base64
            msg_clean = msg_raw.replace("-", "+")
            msg_clean = msg_clean.replace("_", "/")

            msg_clean = base64.b64decode(msg_clean)

            #remove  b' \r \n
            message_final = msg_clean.decode().strip()

        return message_final

    def save_audio(self):
        message = self.get_message()
        sender = self.get_sender()

        # deteksi bahasa
        lang = detect(message)
        if lang == 'id':
            op_sender = 'pesan dikirim oleh '
            op_message = '. Berikut isi pesannya. '
            print('Pesan Berbahasa Indonesia')
            language = 'id'
        elif lang == 'en':
            op_sender = 'message sent by '
            op_message = '. Content of the message is, '
            print('Pesan Berbahasa Inggris')
            language = 'en'
        else:
            op_sender = 'message sent by '
            op_message = '. Content of the message is, '
            language = 'en'

        message_final = op_sender + sender + op_message + message
        print(message_final)

        # Passing the text and language to the engine,
        # here we have marked slow=False. Which tells
        # the module that the converted audio should
        # have a high speed
        speech = gTTS(text=message_final, lang=language, slow=False)

        # Saving the converted audio in a mp3 file named
        speech.save("email.mp3")

    def play_audio(self):
        # Playing the converted file
        pygame.mixer.init()
        pygame.mixer.music.load('email.mp3')
        pygame.mixer.music.play()
        time.sleep(0)

