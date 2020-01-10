import requests
import csv
from bs4 import BeautifulSoup
base_url = "http://www.nepalstock.com/"
rows2 = []
for i in range(1,10):
    trail_url = 'main/todays_price/index/'+str(i)
    response = requests.get(base_url+trail_url)
    html_soup = BeautifulSoup(response.content, 'lxml')
    tables = html_soup.find_all("table")
    table = tables[0]
    raw_trs = table.find_all("tr")
    if(i==9):
        clean_trs = raw_trs[1:19]
    else:
        clean_trs = raw_trs[1:22]
    raw_columns, raw_rows = clean_trs[0], clean_trs[1:]
    columns = [td.text for td in raw_columns.find_all("td")]
    rows = [[td.text.split('\xa0')[0] for td in row.find_all("td")] for row in raw_rows]
    rows2 = rows2 + rows
     
def get_dict(**datas):
    columns = datas.get('columns')
    rows = datas.get('rows')
    return [dict(zip(columns, row)) for row in rows]

def write_to_csv(filename, datas):
    with open(filename, 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)

columns, rows = get_data(base_url, 'todaysprice')
datas = get_dict(columns=columns, rows=rows2)
write_to_csv("stock_market.csv", datas)