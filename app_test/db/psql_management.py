import logging
from logging.handlers import RotatingFileHandler
from pprint import pprint

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'log_db_testcase_kanal.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s - %(lineno)s '
)
handler.setFormatter(formatter)


def db_login(arr):
    """Подключениие к базе данных."""
    return psycopg2.connect(
            user=arr['POSTGRES_USER'],
            password=arr['POSTGRES_PASSWORD'],
            host=arr['DB_HOST'],
            port=arr['DB_PORT'],
            database=arr['DB_NAME'],
    )


def db_ping(tokens):
    try:
        connection = db_login(tokens)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print('Информация о сервере PostgreSQL')
        print(connection.get_dsn_parameters(), '\n')
        # Выполнение SQL-запроса
        cursor.execute('SELECT version();')
        # Получить результат
        record = cursor.fetchone()
        logger.info("Вы подключены к - ", record, "\n")
    except (Exception, Error) as error:
        logger.debug('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info('Соединение с PostgreSQL закрыто')


def db_create_table(tokens, table_name):
    """Создание таблицы необходимой по тестовому заданию."""
    try:
        connection = db_login(tokens)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_request = (
            f'CREATE TABLE IF NOT EXISTS {table_name}('
            f'id INTEGER PRIMARY KEY,'
            f'delivery INTEGER,'
            f'price_usd INTEGER,'
            f'delivery_date DATE,'
            f'price_rub NUMERIC (36,2)'
            f');'
        )
        cursor.execute(sql_request)
        connection.commit()
        logger.info(f'Таблица {table_name} успешно создана в PostgreSQL')
    except (Exception, Error) as error:
        logger.debug('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info('Соединение с PostgreSQL закрыто')


def db_style_change_date(tokens, db_name):
    """Создание таблицы необходимой по тестовому заданию."""
    try:
        connection = db_login(tokens)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_request = (
            f'ALTER DATABASE {db_name} SET datestyle TO "ISO, DMY";'
        )
        cursor.execute(sql_request)
        connection.commit()
        logger.info(f'Стиль времени в таблице {db_name} успешно изменен '
                    f'с YYYY.MM.DD на DD.MM.YYYY')
    except (Exception, Error) as error:
        logger.debug('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info('Соединение с PostgreSQL закрыто')


def db_populate(data_sheets, tokens, table_name):
    """
    Наполнение таблицы актуальными данными полученными через API Google Sheets.
    """
    try:
        connection = db_login(tokens)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_request = (
            f'INSERT INTO {table_name} (id, '
            f'                          delivery, '
            f'                          price_usd, '
            f'                          delivery_date, '
            f'                          price_rub) '
            f'VALUES(%s,%s,%s,%s,%s);'
        )
        cursor.executemany(sql_request, vars_list=data_sheets)
        connection.commit()
        logger.info(f'Таблица {table_name} успешно обновлена в PostgreSQL')
    except (Exception, Error) as error:
        logger.debug('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info('Соединение с PostgreSQL закрыто')


def db_delete_table(tokens, table_name):
    """
    Удаление данных.
    Удаляет всю информацию из таблицы PSQL
    ранее сохраненную из API Google Sheets.
    """
    try:
        connection = db_login(tokens)
        cursor = connection.cursor()
        sql_request = f'DELETE FROM {table_name};'
        cursor.execute(sql_request)
        connection.commit()
        logger.info(f'Таблица {table_name} успешно очищена в PostgreSQL')
    except (Exception, Error) as error:
        logger.debug('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info('Соединение с PostgreSQL закрыто')


def db_show_table(tokens, table_name):
    """
    Выводит информацию из таблицы PSQL ранее сохраненную из API Google Sheets.
    """
    try:
        connection = db_login(tokens)
        cursor = connection.cursor()
        cursor.execute(
            f'SELECT id, '
            f'       delivery, '
            f'       price_usd, '
            f'       price_rub, '
            f'       delivery_date '
            f'FROM   {table_name};'
        )
        record = cursor.fetchall()
        logger.info(f'Таблица {table_name} успешно выведена для чтения')
        pprint(record)
    except (Exception, Error) as error:
        logger.debug('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info('Соединение с PostgreSQL закрыто')
