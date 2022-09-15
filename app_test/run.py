from pprint import pprint

from db.psql_management import db_create_table, db_login, db_ping, db_populate
from detail import api_auth
from detail.work_sheets import formatting_value, values_read

# contain_cow_e = [str(i**2) for i in range(0, 51)]
# contain_cow_f = [str(i**2) for i in range(0, 51)]


if __name__ == "__main__":
    db_ping()
    db_create_table()
    # pprint(values_read(api_auth.spreadsheet_id, 'Лист1')['values'][1:])
    data_sheets = values_read(api_auth.spreadsheet_id, 'Лист1')['values'][1:]
    formatting = formatting_value(data_sheets)
    db_populate(formatting)
