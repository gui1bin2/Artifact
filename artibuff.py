# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 16:06:44 2018

@author: lenovo
"""

import datetime
import pandas as pd
import requests 
import bs4

#官方API调取
b=requests.get('https://media.st.dl.bscstorage.net/apps/583950/resource/card_set_1.E991EF727CDCD9C8194209A9576C76A2E2A1AFB5.json')
jx = b.json()
jx2 = b.json()['card_set']['card_list']

df1 = pd.DataFrame(index=[0])
data = pd.DataFrame()
for i in range(357):
    data = pd.DataFrame(index=[i])
    data['卡牌ID'] = str(jx2[i]['card_id'])
    data['中文名称'] = jx2[i]['card_name']['schinese']
    data['名称'] = jx2[i]['card_name']['english']
    if 'is_blue' in jx2[i]:data['颜色']='蓝'
    elif 'is_red' in jx2[i]:data['颜色']='红'
    elif 'is_green' in jx2[i]:data['颜色']='绿'
    elif 'is_black' in jx2[i]:data['颜色']='黑'
    else:data['颜色']='无'
    if 'rarity' in jx2[i]:data['稀有度']=str(jx2[i]['rarity'])
    else:data['稀有度']='无'
    df1 =pd.concat([df1,data])
df1 = df1.dropna()

#爬artibuff地址和用户
url = 'https://www.artibuff.com/stats/heroes?mode=draft'
useragent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

#请求，得到整个网页源码
r = requests.get(url,headers=useragent)
print(r.text)

#用beautifulSoup解析
soup = bs4.BeautifulSoup(r.text,'lxml')
list1 = soup.find_all('tr', class_='color-black')
list2 = soup.find_all('tr', class_='color-red')
list3 = soup.find_all('tr', class_='color-green')
list4 = soup.find_all('tr', class_='color-blue')

#创建新的空表
df = pd.DataFrame(index=[0])
data = pd.DataFrame()

for i in list1:
    data = pd.DataFrame(index=[1])
    data['名称'] = i.find('td', class_='cardName').a.text.strip()
    data['胜率'] = i.find('td', class_='winRate').text.strip()
    data['使用率'] = i.find('td', class_='pickRate').text.strip()
    df =pd.concat([df,data])
for i in list2:
    data = pd.DataFrame(index=[1])
    data['名称'] = i.find('td', class_='cardName').a.text.strip()
    data['胜率'] = i.find('td', class_='winRate').text.strip()
    data['使用率'] = i.find('td', class_='pickRate').text.strip()
    df =pd.concat([df,data])    
for i in list3:
    data = pd.DataFrame(index=[1])
    data['名称'] = i.find('td', class_='cardName').a.text.strip()
    data['胜率'] = i.find('td', class_='winRate').text.strip()
    data['使用率'] = i.find('td', class_='pickRate').text.strip()
    df =pd.concat([df,data])
for i in list4:
    data = pd.DataFrame(index=[1])
    data['名称'] = i.find('td', class_='cardName').a.text.strip()
    data['胜率'] = i.find('td', class_='winRate').text.strip()
    data['使用率'] = i.find('td', class_='pickRate').text.strip()
    df =pd.concat([df,data]) 
df = df.dropna()
df = df.reset_index(drop=True)
df['类别'] = '英雄'
df['抓取日期'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


df2 = pd.merge(df,df1,left_on='名称',right_on='名称',how='left')
df2 = df2[['抓取日期','中文名称','名称','颜色','胜率','使用率','稀有度']].sort_values(['胜率'],ascending=[False])
df2.to_excel('C:/Users/lenovo/Desktop/artibuff.xlsx',index=0)




