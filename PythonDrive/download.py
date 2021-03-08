from __future__ import print_function
import pickle
import os
import io
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# PATH_: path of project's folder
# PATH: path of file's folder
# FOLDER_NAME: folder's name in Google Driver
PATH = '/Users/asistemas/Desktop/Txt/'
PATH_ = 'C:/Repositories/Things/PythonDrive/'
DOWNLOAD_PATH = 'C:/Users/pablo/Desktop/Txt/'
FOLDER_NAME = 'Txt'
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """ Upload txt files of a specific folder in local to folder in google drive using google drive api v3
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

    # Search the folder Txt or create it.
    # List only folders  in drive account and return foder's name and id.
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder' and trashed = false", pageSize=10, fields="nextPageToken, files(name, id)").execute() # pylint: disable=maybe-no-member
    items = results.get('files', [])

    # If folder Txt do not exist, create it and return the id
    # If the folder Txt exist only return the id
    idFolder = findFolder(items,FOLDER_NAME)
    if idFolder:
        file.write('Folder '+FOLDER_NAME+' found        ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
        response = service.files().list(q= '"%s" in parents and trashed = false' %idFolder, # pylint: disable=maybe-no-member
                                        fields='nextPageToken, files(id, name)',
                                        pageSize=10).execute()
        for arch in response.get('files', []):
            downloadFiles(arch.get('id'), arch.get('name'),service)
            file.write('Found file: %s (%s)' % (arch.get('name'), arch.get('id')) + os.linesep)
    else:
        file.write('The folder not exist, please first create the foder with files to download ')

def downloadFiles(id, name, service):
    request = service.files().get_media(fileId = id) # pylint: disable=maybe-no-member
    fh = io.FileIO(DOWNLOAD_PATH + name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

def findFolder(items, name):
    """ Searchs folder by name and return the ID of Folder
        param list items This parameter represent all folder on google drive account
        param String name This parameter represent the name of folder to find
        returns the id of folder if is founded and None if isn't founded. 
    """
    for s in range(len(items)):
        if items[s]['name'] == name:
            return items[s]['id']
        else:
            return None

if __name__ == '__main__':
    main()
 