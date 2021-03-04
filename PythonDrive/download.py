from __future__ import print_function
import pickle
import os
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# PATH_: path of project's folder
# PATH: path of file's folder
# FOLDER_NAME: folder's name in Google Driver
PATH = '/Users/asistemas/Desktop/Txt/'
PATH_ = '/Users/asistemas/Repositories/Things/PythonDrive/'
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
        response = service.files().list(q= '"%s" in parents' %idFolder,
                                        fields='nextPageToken, files(id, name)',
                                        pageSize=10).execute()
        for arch in response.get('files', []):
            file.write('Found file: %s (%s)' % (arch.get('name'), arch.get('id')) + os.linesep)
    else:
        file.write('The folder not exist, please first create the foder with files to download ')


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

    # if idFolder:
    #     file.write('Folder '+FOLDER_NAME+' found        ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    # else:
    #     file.write('Folder '+FOLDER_NAME+' not found        ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    #     file_metadata = {
    #         'name': FOLDER_NAME,
    #         'mimeType': 'application/vnd.google-apps.folder'
    #     }
    #     fileDrive = service.files().create(body=file_metadata, fields='id').execute() # pylint: disable=maybe-no-member
    #     if fileDrive:
    #         file.write('Folder '+FOLDER_NAME+' created whit ID: %s' % fileDrive.get('id') + '         ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    #     else:
    #         file.write('There was an error at create the folder' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    #     idFolder = fileDrive.get('id')
    # file.close()

#     results = service.files().list(q="mimeType='text/plain' and trashed = false and '"+idFolder+"' in parents", pageSize=10, fields="nextPageToken, files(name, id)").execute() # pylint: disable=maybe-no-member
#     items = results.get('files', [])
    
#     if items:
#         updateFiles(idFolder,service,PATH,items)
#     else:
#         createFiles(idFolder,service,PATH)

# def updateFiles(idFolder,service,PATH,items):
#     """ Update files if these files already exist on folder in google drive
#         param idFolder Is the ID of the folder created at google drive.
#         param service Is the credentials to get access to google drive.
#         param PATH Is the path of the folder in local to upload.
#         param items Are the files founded in google drive.
#     """
#     file = open(PATH_ + "log.log", "a")
#     file.write('Preparing to update files       ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
#     filesToUpload = getFileToUpload()
#     file.write('Files found to update:' + ' '.join(map(str,filesToUpload)) + os.linesep)

#     for fileLocal, mimeType in filesToUpload:
#         fileExist = False
#         for item in items:
#             if item['name'] == fileLocal:
#                 fileExist = True
#                 metadata = {'name': fileLocal,
#                         'mimeType': mimeType,
#                         'addParents': [idFolder]
#                         }
#                 res = service.files().update(fileId=item['id'], body=metadata, media_body=PATH+fileLocal).execute() # pylint: disable=maybe-no-member
#                 if res:
#                     file.write(res['name']+'    '+res['id']+ '  ' +res['mimeType']+'    '+ os.linesep) 
#                 else:
#                     file.write('There was an error at update the file: ' +fileLocal + ' ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
    
#         if not fileExist:
#             metadata = {'name': fileLocal,
#                         'mimeType': mimeType,
#                         'parents': [idFolder]
#                         }
#             res = service.files().create(body=metadata, media_body=PATH+fileLocal).execute() # pylint: disable=maybe-no-member
#             if res:
#                 file.write(res['name']+'    '+res['id']+ '  ' +res['mimeType']+'    '+ os.linesep) 
#             else:
#                 file.write('There was an error at create the file: ' +fileLocal + ' ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
#             file.write('Files created succesfully       ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)

#     file.write('Files updated succesfully       ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)        
#     file.close()

# def createFiles(idFolder, service, PATH):
#     """ Create files founded in local on a folder in google drive
#         param idFolder Is the ID of the folder created at google drive.
#         param service Is the credentials to get access to google drive.
#         param PATH Is the path of the folder in local to upload.
#     """
#     file = open(PATH_ + "log.log", "a")
#     file.write('Preparing to upload files       ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
#     filesToUpload = getFileToUpload() #Get the files of the PATH
#     file.write('Files found to upload:' + ' '.join(map(str,filesToUpload)) + os.linesep)

#     #Create new files to google drive on specific folder
#     for filename, mimeType in filesToUpload:
#         metadata = {'name': filename,
#                     'mimeType': mimeType,
#                     'parents': [idFolder]
#                     }
#         res = service.files().create(body=metadata, media_body=PATH+filename).execute() # pylint: disable=maybe-no-member
#         if res:
#             file.write(res['name']+'    '+res['id']+ '  ' +res['mimeType']+'    '+ os.linesep) 
#         else:
#             file.write('There was an error at create the file: ' +filename + ' ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
            
#     file.write('Files created succesfully       ' + datetime.today().strftime('%Y/%m/%d %H:%M:%S') + os.linesep)
#     file.close()



# def getFileToUpload():
#     """ Get .txt files of folder to upload
#         returns the list of archives to upload ['name','type_Archive']
#     """ 
#     contenido = os.listdir(PATH)
#     txt = []
#     for fichero in contenido:
#         if os.path.isfile(os.path.join(PATH, fichero)) and fichero.endswith('.txt'):
#             txt.append((fichero, 'text/plain'))
#     return	txt

if __name__ == '__main__':
    main()
 