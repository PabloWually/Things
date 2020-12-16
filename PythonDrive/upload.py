from __future__ import print_function
import pickle
import os
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

PATH = '/Users/asistemas/Desktop/Txt/'
PATH_ = '/Users/asistemas/Desktop/PythonDrive/'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # List path and create or open log file
    content = os.listdir(PATH_)
    if "log.log" in content:
        file = open(PATH_ + "log.log", "a")
        file.write("File log edited         " + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    else:
        file = open(PATH_ + "log.log", "w")
        file.write("File log created        " + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)

    # Search the folder Txt or created it.
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder'", pageSize=10, fields="nextPageToken, files(name, id)").execute() # pylint: disable=maybe-no-member
    items = results.get('files', [])

    idFolder = findFolder(items,'Txt')
    if idFolder:
        file.write('Folder Txt found        ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    else:
        file.write('Folder Txt not found        ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
        file_metadata = {
            'name': 'Txt',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        fileDrive = service.files().create(body=file_metadata, fields='id').execute() # pylint: disable=maybe-no-member
        file.write('Folder created Folder ID: %s' % fileDrive.get('id') + '         ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
        idFolder = fileDrive.get('id')

    # filesToUpload = getFileToUpload()
    # file_metadata = {[]}
    # for fileToUpload in filesToUpload:
    #     file_metadata.add('name':fileToUpload, 'parents':[idFolder])
    

def findFolder(items, name):
    """ Search folder by the name and return the ID of Folder 
    """
    for s in range(len(items)):
        if items[s]['name'] == name:
            return items[s]['id']
        else:
            return None

def getFileToUpload():
    """ Get .txt files in a folder to upload
    """ 
    contenido = os.listdir(PATH)
    txt = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(PATH, fichero)) and fichero.endswith('.txt'):
            txt.append(fichero)
    return	txt

if __name__ == '__main__':
    main()
