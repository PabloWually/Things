# gdrive-upload
Upload file to specific folder using Google Drive API

## Getting Start :
#### 1. Clone this code for local copy
`git clone https://github.com/PabloWually/Things.git`
and go to cloned folder
`cd Things/PythonDrive`

#### 2. Obtain OAuth 2.0 credentials from the Google Developers Console.
Visit the [Google Developers Console](https://console.developers.google.com/) to obtain OAuth 2.0 credentials such as a client ID and client secret that are known to both Google and your application. Choose option to download it as JSON format and save to `credentials.json` in `Things/PythonDrive` folder as this code.

or follow [step 1 in this guideline](https://developers.google.com/drive/v3/web/quickstart/python#step_1_turn_on_the_api_name). We will use this key as [web service token](https://developers.google.com/identity/protocols/OAuth2WebServer)

#### 3. Install require package
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```