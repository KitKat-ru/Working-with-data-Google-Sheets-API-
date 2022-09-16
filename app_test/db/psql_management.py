import os
from pprint import pprint

import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv(dotenv_path="../.env")

TABLE_NAME = 'orders10'

def db_login():
    """Подключениие к базе данных."""
    return psycopg2.connect(
            # логин, который указали при установке PostgreSQL
            user=os.getenv('POSTGRES_USER'),
            # пароль, который указали при установке PostgreSQL
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            # дефолтная база данных postgres
            database=os.getenv('DB_NAME'),
    )


def db_ping():
    try:
        connection = db_login()
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print('Информация о сервере PostgreSQL')
        print(connection.get_dsn_parameters(), '\n')
        # Выполнение SQL-запроса
        cursor.execute('SELECT version();')
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Соединение с PostgreSQL закрыто')


def db_create_table():
    """Создание таблицы необходимой по тестовому заданию."""
    try:
        connection = db_login()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_request = (
            f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}('
            f'id INTEGER PRIMARY KEY,'
            f'delivery INTEGER,'
            f'price_usd INTEGER,'
            f'delivery_date DATE,'
            f'price_rub NUMERIC (36,2)'
            f');'
        )

        cursor.execute(sql_request)
        connection.commit()
        print(f'Таблица {TABLE_NAME} успешно создана в PostgreSQL')
    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Соединение с PostgreSQL закрыто')


def db_populate(data_sheets):
    """
    Наполнение таблицы актуальными данными полученными через API Google Sheets.
    """
    try:
        connection = db_login()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_request = f'INSERT INTO {TABLE_NAME} VALUES(%s,%s,%s,%s,%s);'
        cursor.executemany(sql_request, vars_list=data_sheets)
        connection.commit()
        print(f'Таблица {TABLE_NAME} успешно обновлена в PostgreSQL')
    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Соединение с PostgreSQL закрыто')


def db_show():
    """
    Выводит информацию из таблицы PSQL ранее сохраненную из API Google Sheets.
    """
    try:
        connection = db_login()
        cursor = connection.cursor()
        cursor.execute(
            f'SELECT id, '
            f'       delivery, '
            f'       price_usd, '
            f'       price_rub, '
            f'       delivery_date '
            f'FROM   {TABLE_NAME}'
        )
        record = cursor.fetchall()
        pprint(record)
    except (Exception, Error) as error:
        print('Ошибка при работе с PostgreSQL', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Соединение с PostgreSQL закрыто')
