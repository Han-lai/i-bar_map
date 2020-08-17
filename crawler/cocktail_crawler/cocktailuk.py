import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------------------
resource_path = (r'./cocktail')
if not os.path.exists(resource_path):
    os.mkdir(resource_path)

#-------------------------------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame(
    columns=['酒名', '酒譜', 'url', '介紹', '評論'])
store_details = {'name': '', 'ingredient': '', 'url': '', 'instruction': '', 'review': ''}

all = []
#-------------------------------------------------------------------------------------------------------------------------------------------
# https://www.cocktail.uk.com/cocktails?page=2
for page in range(145,151):#總共185  要跑到151
    url = 'https://www.cocktail.uk.com/cocktails?page={}'.format((str(page)))

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    params = {''}
    res = requests.get(url=url, headers=headers, params=params)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.select('div#content  div.small-11') #每款酒的資訊

    for n in a:
        url = 'https://www.cocktail.uk.com' + n.select('a')[0]['href']
        print(url)
        res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            name = soup.select('h1[itemprop="name"]')[0].text
        except IndexError as e:
            print(url)
            continue
        instruction = soup.select('p[itemprop="instructions"]')[0].text

# -------------------------------------------------------------------------------------------------------------------------------------------
        info = soup.select('div[style="margin-left: 1.5em;"] li') #取出酒譜裡的容量
        print(info)
        amount = [ab.select('span')[0].text for ab in info]#取出酒譜裡的容量
        inname = [i.select('span[itemprop="name"] a')[0].text for i in info]# 取出酒譜裡的材料名稱
        ingredient = dict(zip(inname,amount))
        print(ingredient)
        review_list = soup.select('div.review')
        review = [[c.select('p')[0].text.lstrip('\n').split('by')[0].strip()] for c in review_list]
        if len(name) != 0:
            store_details['name'] = name
        else:
            store_details['name'] = 'null'
        store_details['ingredient'] = ingredient
        store_details['url'] = url
        if len(instruction) != 0:
            store_details['instruction'] = instruction
        else:
            store_details['instruction'] = 'null'

        if len(review)!=0:
            store_details['review'] = review
        else:
            store_details['review'] = 'null'
        print(store_details)

        time.sleep(0.9)

        each = list(store_details.values())  # 取每個網站的資訊
        all.append(each)  # 將所有網站的資訊丟入同一個list中



    dff = df.append(pd.DataFrame(all,
            columns=['酒名', '酒譜', 'url', '介紹', '評論']))
    a_df = dff.drop_duplicates('url')
    # a_df.to_csv(r'./cocktail/cocktail_ukm.csv', index=False,encoding="utf-8-sig")