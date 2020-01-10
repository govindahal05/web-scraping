import requests
from bs4 import BeautifulSoup
import csv
base_url = "https://globalimebank.com/forex.html"

def get_data(base_url, trail_url=''):
    response = requests.get(base_url)
    datas = BeautifulSoup(response.content,'lxml')

    tables = datas.find("table")
    table_rows = tables.find_all('tr')
    raw_columns, raw_rows = table_rows[0], table_rows[1:]
    columns = [th.text for th in raw_columns.find_all("th")]
    columns.insert(0,'Sno.')
    # rows = [[td.text for td in row.find_all("td")] for row in raw_rows]
    inc = 0
    rows = []
    for row in raw_rows:
            inc = inc + 1
            data = [td.text for td in row.find_all("td")]
            data.insert(0,inc)
            rows.append(data)
    return columns, rows

def get_dict(**datas):
    columns = datas.get('columns')
    rows = datas.get('rows')
    return [dict(zip(columns, row)) for row in rows]

def write_to_csv(filename, datas):
    with open(filename, 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)
columns, rows = get_data(base_url)    
datas = get_dict(columns=columns, rows=rows)
write_to_csv("Exchange-rate.csv", datas)
        