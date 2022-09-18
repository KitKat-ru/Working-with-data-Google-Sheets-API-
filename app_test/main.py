import datetime
import logging
import os
import time
from logging.handlers import RotatingFileHandler

from cbrf.models import DailyCurrenciesRates
from db.psql_management import (db_create_table, db_delete_table, db_ping,
                                db_populate, db_show_table_expired_orders,
                                db_style_change_date, db_show_table)
from detail.work_sheets import values_read
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'log_main_testcase_kanal.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s - %(lineno)s '
)
handler.setFormatter(formatter)


# Интервал пуллинга
RETRY_TIME = 5
# Название таблицы в базе данных PSQL
TABLE_NAME = 'orders'
# ID доллара согласно ЦБ РФ
USD_ID = 'R01235'
DT_NOW = datetime.datetime.now()

TOKEN_DICT = {
    # логин, который указали при установке PostgreSQL
    'POSTGRES_USER': os.getenv('POSTGRES_USER', default='postgres'),
    # пароль, который указали при установке PostgreSQL
    'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
    # Адрес обращения к базе данных
    'DB_HOST': os.getenv('DB_HOST', default='db'),
    # порт для подключения к БД
    'DB_PORT': os.getenv('DB_PORT', default=5432),
    # дефолтная база данных postgres
    'DB_NAME': os.getenv('DB_NAME', default='postgres'),
    # ID таблицы в Google Sheets
    'SPREADSHEET_ID': os.getenv(
        'SPREADSHEET_ID',
        default='My-Table-Is-Google-Sheets-In-TestCase-Kanals'
    ),
}


def usd_rate(dt, id_currency):
    """Функция для получения актуального курса доллара из API ЦБ РФ."""
    return DailyCurrenciesRates(dt).get_by_id(id_currency).value


def formatting_value(data_sheets):
    """Добавляет дополнительную колонку с ценой в рублях."""
    rate = usd_rate(DT_NOW, USD_ID)
    for arr in data_sheets:
        rub_rate = int(arr[2]) * float(rate)

        arr.append(str(rub_rate))
    return data_sheets


def check_tokens(arr):
    """Проверяет доступность переменных окружения."""

    for key, values in arr.items():
        if not values or values is None:
            logger.debug(f'Отсутствует переменная окружения {key} !')
            return False
    logger.info('Все переменные в наличии...')
    return True


def main():
    """Основная логика работы скрипта."""
    logger.info('Запускаю скрипт...')
    if not check_tokens(TOKEN_DICT):
        logger.debug('Отсутствует доступ к переменным окружения.')
        raise KeyError('Отсутствует доступ к переменным окружения.')
    db_ping(TOKEN_DICT)
    db_create_table(TOKEN_DICT, TABLE_NAME)
    db_style_change_date(TOKEN_DICT, TOKEN_DICT['DB_NAME'])
    while True:
        try:
            db_delete_table(TOKEN_DICT, TABLE_NAME)
            data_sheets = values_read(
                TOKEN_DICT['SPREADSHEET_ID'], 'Лист1'
            )['values'][1:]
            formatting = formatting_value(data_sheets)
            db_populate(formatting, TOKEN_DICT, TABLE_NAME)
            db_show_table(TOKEN_DICT, TABLE_NAME)
            db_show_table_expired_orders(TOKEN_DICT, TABLE_NAME)
            time.sleep(RETRY_TIME)
        except Exception as error:
            logger.error(f'Произошел сбой в программе, Ошибка - {error}!')
            time.sleep(RETRY_TIME)


if __name__ == "__main__":
    main()
