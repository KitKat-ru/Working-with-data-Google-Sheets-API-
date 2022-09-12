import os

import googleapiclient.discovery
import httplib2
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv(dotenv_path=".env")

CREDENTIALS_FILE = '../creads.json'
spreadsheet_id = os.getenv('SPREADSHEET_ID')


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]
)

httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build(
    serviceName='sheets',
    version='v4',
    http=httpAuth,
)
