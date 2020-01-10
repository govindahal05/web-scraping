import requests
from bs4 import BeautifulSoup
import csv
url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
response = requests.get(url)
datas = BeautifulSoup(response.content,'lxml')
col_sm_4 = col_md_9.find_all("div",class_="col-sm-4")
col_sm_4 = col_md_9.find_all("div",class_="col-sm-4")
columns = ['sno.','Title','Price','Description','Ratings']
sn = 0
datalists = []
for col_sm in col_sm_4:
    sn = sn + 1
    title = col_sm.find("a",class_="title").text
    price = col_sm.find("h4",class_="pull-right").text
    description = col_sm.find("p",class_="description").text
    datalist = [sn,title,price,description]
    datalists.append(datalist)
#     print(sn)
#     print(title)
#     print(price)
#     print(description)
#     print(col_sm)
#	  print(datalists)
def get_dict(**datas):
    columns = datas.get('columns')
    rows = datas.get('rows')
    return [dict(zip(columns, row)) for row in rows]

datas = get_dict(columns=columns, rows=datalists)

def write_to_csv(datas):
    with open('ecommerce.csv', 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=datas[0].keys())
        writer.writeheader()
        writer.writerows(datas)
        
write_to_csv(datas)
