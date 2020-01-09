import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.nepalpolice.gov.np/index.php/safety-security-tips/emergency-numbers"
response = requests.get(base_url)

data = BeautifulSoup(response.content,'lxml')
tables = data.find_all("table")
rows = tables[1].find_all("tr")
rows2 = tables[2].find_all("tr")
raw_columns, raw_datas, raw_datas2 = rows[0], rows[1:], rows2[1:]

columns = [data.text for data in raw_columns.find_all("td")]
datas = [[td.text for td in tr.find_all("td")] for tr in raw_datas]
datas2 = [[td.text for td in tr.find_all("td")] for tr in raw_datas2]
joindata = datas+datas2

def get_dict(**datas):
    columns = datas.get('columns')
    rows = datas.get('rows')
    return [dict(zip(columns, row)) for row in rows]

datas = get_dict(columns=columns, rows=joindata)

def write_to_csv(datas):
    with open('nepal_emergency_number.csv', 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)
        
write_to_csv(datas)