import googleapiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

# Токены для service_account в Google Cloud
CREDENTIALS_FILE = 'creads.json'

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


def values_read(sheet_id, range, position='ROWS'):
    """Функция для считывания таблицы из Google Sheets в формате json."""
    return service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range,  # 'A1:D51'
        majorDimension=position,  # 'ROWS'
    ).execute()


def values_write(sheet_id, range, position='COLUMNS', *args):
    """Функция для записи в таблицу Google Sheets."""
    return service.spreadsheets().values().batchUpdate(
        spreadsheetId=sheet_id,
        body={
            'valueInputOption': 'USER_ENTERED',
            'data': [
                {
                    'range': range,  # 'E1:F51'
                    'majorDimension': position,  # 'COLUMNS'
                    'values': args
                    # 'values': [
                    #     contain_cow_e,
                    #     contain_cow_f,
                    # ]
                }
            ]
        }
    ).execute()
