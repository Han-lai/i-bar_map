import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
import time

resource_path = (r'./whisky')
if not os.path.exists(resource_path):
    os.mkdir(resource_path)

url = 'https://thewhiskyphiles.com/whisky-reviews/whisky-scores/'

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

headers_post = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
           '__user': '100001971050758', '__a': '1', '__dyn': '7xe6FoO13xu1syWwHh963m1FwAxu13wmEW4UKewSAwHxW4E2czobohwrbwdK4o4O0C82Vwb-q1ewcG0KEswdC2W2y1nzU1vrzo5-1HwOwsU9kbxS0lK2W2C4U2IzUuxy0wU3mwkE5G0zE',
           '__csr': '', '__req': '1', '__beoa': '0', '__pc': 'PHASED:plugin_default_pkg', 'dpr': '1', '__ccg': 'EXCELLENT', '__rev': '1002261326', '__s': ':1jqwo9:61nrg6', '__hsi': '6839527445554016898-0',
           '__comet_req': '0', 'locale': 'en_US', 'fb_dtsg': 'AQHcVbTlSzgk:AQEAK5Misa2R', 'jazoest': '22100', '__sp': '1'}

res = requests.get(url=url, headers=headers)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, 'html.parser')

df = pd.DataFrame(
    columns=['酒名', '酒廠', 'url', '年分', '產地', '酒精度', '照片url', '內容', '評論', '價錢'])
all = []

#日本威士忌37種
for page in range(1,8): #共有7頁
    Japan_URL = soup.select('li.cat-item-507046 a')[0]['href'] + 'page/{}'.format(str(page))

    res = requests.get(url=Japan_URL, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    whisky = soup.select('div#main-content h2.posttitle')

    for wh in whisky:#每一款酒的評論連結  主要資訊都在這
        data1 = []
        url = wh.select('a')[0]['href'] #連結'url'
        # print(url)
        res = requests.post(url=url, headers=headers_post)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, 'html.parser')
        img = soup.select('meta[property="og:image"]')[0]['content']

        # print(img)
        name = soup.select('h1[class="title"]')[0].text
        content = soup.select('section[class="entry"]')[0].text.split('What they say')[1].split('What I say')[0].replace("\n", "")
        comment = soup.select('section[class="entry"]')[0].text.split('What I say')[1].split('Overall')[0].replace("\n", "")
        # print(name)
        info = soup.select_one('section.entry').select_one('ul').text.rstrip('TweetMore') # 酒的類別

        pattern1 = re.compile('Category.*')  # 威士忌類別(單一麥芽...)
        pattern2 = re.compile('ABV.*')  # 酒精濃度
        pattern3 = re.compile('Cost.*')  # 價錢
        pattern4 = re.compile('Origin.*')  # 酒廠 標籤為產地，在此處當作酒廠)
        pattern5 = re.compile('Age.*')
        if len(info) > 1:
            try:
                if 'Category:' in pattern1.findall(info)[0]:
                    Category = pattern1.findall(info)[0].split(':')[1]  # 威士忌類別(單一麥芽...)
                else:
                    Category = (info + 'Category:null').split('Category:')[1]
            except IndexError as e:
                Category = 'null'

            try:
                if 'ABV:' in pattern2.findall(info)[0]:
                    ABV = pattern2.findall(info)[0].split(':')[1]#酒精濃度  # 酒精濃度
                else:
                    ABV = (info + 'ABV:null').split('ABV:')[1]
            except IndexError as e:
                ABV = 'null'

            try:
                if 'Cost' in pattern3.findall(info)[0]:
                    Cost = pattern3.findall(info)[0].split(':')[1].replace('£?', 'null').replace('£n/a', 'null').replace('?', 'null')#價錢
                else:
                    Cost = (info + 'Cost:null').split('Cost:')[1]
            except IndexError as e:
                Cost = 'null'

            try:
                if 'Origin:' in pattern4.findall(info)[0]:
                    factory = pattern4.findall(info)[0].split(':')[1].replace('?','null')#酒廠
                else:
                    factory = (info + 'Origin:null').split('Origin:')[1]
            except IndexError as e:
                factory = 'null'


            try:
                if 'Age:' in pattern5.findall(info)[0]:
                    Age = pattern5.findall(info)[0].split(':')[1].replace('NAS','null')#木桶年分'年分'
                else:
                    Age = 'null'
            except IndexError as e:
                Age = 'null'

        else:
            info2 = soup.select('meta[property="og:description"]')[0]['content']
            Age = 'null'
            Category = 'null'
            factory = 'null'

            for m in re.finditer(re.compile(r'\d\d\S\sABV'), info2):
                ABV = m.group().split('ABV')[0]
            print(ABV)

            for m in re.finditer(re.compile(r'£\d.*\s'), info2):
                Cost = m.group().split('for')[0]
            print(Cost)
    #
        time.sleep(3)
        data1.append(name)
        data1.append(factory)
        data1.append(url)
        data1.append(Age)
        data1.append('Japan')
        data1.append(ABV)
        data1.append(img)
        data1.append(content)
        data1.append(comment)
        data1.append(Cost)
        all.append(data1)
    print('---------------')
    a_df = df.append(pd.DataFrame(all, columns=['酒名', '酒廠', 'url', '年分', '產地', '酒精度', '照片url', '內容', '評論', '價錢']))
    a_df = a_df.drop_duplicates('酒名')
    a_df.to_csv(r'./whisky/Japan.csv', index=False, encoding='utf-8-sig')
