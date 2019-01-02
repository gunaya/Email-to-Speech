from __future__ import print_function

import time

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools, client
from gtts import gTTS
import pygame
from langdetect import detect

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API, only get 1 of the the recent message ids
    # First get the message id for the message
    results = service.users().messages().list(userId='me', maxResults=1).execute()

    # get the message id from the results object
    message_id = results['messages'][0]['id']

    # use the message id to get the actual message, including any attachments
    message = service.users().messages().get(userId='me', id=message_id).execute()

    # now the message object contains the entire recent message
    print(message['snippet'])

    # deteksi bahasa
    lang = detect(message['snippet'])
    print(lang)
    if not lang == 'en':
        language = 'id'
    else:
        language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=message['snippet'], lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    myobj.save("welcome.mp3")

    # Playing the converted file
    pygame.mixer.init()
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    time.sleep(20)

    # music = pyglet.resource.media('welcome.mp3')
    # music.play()
    # pyglet.app.run()



if __name__ == '__main__':
    main()