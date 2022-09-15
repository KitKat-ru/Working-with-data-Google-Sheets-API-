import os

import googleapiclient.discovery
import httplib2
from cbrf.models import DailyCurrenciesRates
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv(dotenv_path=".env")

CREDENTIALS_FILE = '../creads.json'

spreadsheet_id = os.getenv('SPREADSHEET_ID')

# Получение доступа к API Google Sheets
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

# Получение данных о курсе USD к RUB на текущую дату
def usd_rate(dt, id_currency):
    daily= DailyCurrenciesRates(dt)
    return daily.get_by_id(id_currency).value
