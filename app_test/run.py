from pprint import pprint
from detail.work_sheets import values_read
from detail.api_auth import spreadsheet_id


# contain_cow_e = [str(i**2) for i in range(0, 51)]
# contain_cow_f = [str(i**2) for i in range(0, 51)]
# pprint(detail.work_sheets.values_read(detail.api_auth.spreadsheet_id, 'A1:D51'))

if __name__ == "__main__":
    pprint(values_read(spreadsheet_id, 'A1:D51'))
