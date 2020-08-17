import requests
from bs4 import BeautifulSoup

import time
import os
import pandas as pd


#-------------------------------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame(
    columns=['酒名', '酒譜', 'url', '介紹', '評論'])
store_details = {'name': '', 'ingredient': '', 'url': '', 'instruction': '', 'review': ''}


#-------------------------------------------------------------------------------------------------------------------------------------------
# https://www.diffordsguide.com/cocktails/search?rating=3%2C3.5%2C4%2C4.5%2C5%2C5.5&sort=name&offset={}&limit=48'.format((str(page*48)))
# for page in range(0,4):#總共93
url = 'https://www.diffordsguide.com/cocktails/search?rating=3%2C3.5%2C4%2C4.5%2C5%2C5.5&sort=name&offset=0&limit=48'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
res = requests.get(url=url, headers=headers) #
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, 'html.parser')
info = soup.select('div[class="cell main-content"] div[class="grid-x grid-margin-x grid-margin-y pad-bottom"] a')
for c in info:
    c_url = 'https://www.diffordsguide.com' + c['href']
    name = c.select('h3[class="box__title"]')[0].text
    print(c_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Cookie': 'diffordsguide_com=0qpkkk3iqc27brdiopm0bb5vbu; __asc=ebc9258e17303be738be8dc8998; __auc=ebc9258e17303be738be8dc8998; _ga=GA1.2.331797616.1593495680; _gid=GA1.2.1387957266.1593495680; _fbp=fb.1.1593495680301.1086156574; diffordsguide_com_subscribe=1; _gat_gtag_UA_6108581_5=1',
    'Refer':str(c_url)}
    data = {'display':'fl oz'}

    res = requests.get(url=c_url, headers=headers, data=data)#如果是formdata 就要帶入files
    soup = BeautifulSoup(res.text,'html.parser')

    # ok-----------------------
    step_info = soup.select('div[class="grid-x grid-margin-y"] div[class="cell small-8 medium-12"] div[class="cell"]')[2:3]
    step = [i.select('p')[0].text for i in step_info]
    # -----------------------
    # ing_tt = soup.select('table[class="no-margin ingredients-table"] tbody')[0].text.replace(' ','').strip()

    # print(ing_tt)

    ing_info = soup.select(' table[class="no-margin ingredients-table"] tbody tr')
    for ia in ing_info:
        ia = ia.select('td[class="no-wrap td-min-width td-align-top pad-right"]')
        amount = [a.text.strip()for a in ia]
    for iname in ing_info:
        try:
            ing_name = iname.select('td[class="td-align-top"]')
            name = [b.text.strip()for b in ing_name]
            store_details['instruction'] = name
            print(name)
            try:
                ing_name = iname.select('td[class="td-align-top pad-bottom"]')
                name = [b.text.strip() for b in ing_name]
                store_details['instruction'] = name
                print(name)
            except:
                continue
        except:
            continue



# ingredient = dict(zip(inname,amount))
#
