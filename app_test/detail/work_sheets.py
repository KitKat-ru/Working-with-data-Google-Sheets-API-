import datetime

from detail.api_auth import service, usd_rate

USD_ID = 'R01235'
DT_NOW = datetime.datetime.now()


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


# data = [
#     ['45', '1786437', '618', '28.05.2022'],
#     ['46', '1485012', '1124', '09.05.2022'],
#     ['47', '1741017', '514', '16.05.2022'],
#     ['48', '1497493', '1198', '30.05.2022'],
#     ['49', '1877503', '1204', '29.05.2022'],
#     ['50', '1426726', '1997', '20.05.2022'],
# ]

def formatting_value(data_sheets):
    """Добавляет дополнительную колонку с ценой в рублях."""
    rate = usd_rate(DT_NOW, USD_ID)

    for arr in data_sheets:
        rub_rate = int(arr[2]) * float(rate)
        arr.append(str(rub_rate))
    return data_sheets

# formatting_value(data)