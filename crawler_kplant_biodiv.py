import requests
from bs4 import BeautifulSoup
from lxml import etree
import numpy as np
import pandas as pd

headers = {'Cookie': '_ga=GA1.2.858307561.1520347273; __utmc=115003869; __utma=115003869.858307561.1520347273.1576161345.1577411178.54; __utmz=115003869.1577411178.54.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

res = requests.get('http://kplant.biodiv.tw/%E6%A4%8D%E7%89%A9%E7%9B%AE%E9%8C%84-%E4%BE%9D%E7%AD%86%E5%8A%83.htm')#植物名稱目錄索引-依筆劃
res.encoding = "utf-8"
soup = BeautifulSoup(res.text,'html.parser')

url_list = []
name_list = []
for soupfindloop in soup.find_all('a'):

    htm = str('http://kplant.biodiv.tw/'+soupfindloop.get('href'))
    name = soupfindloop.text
    value = [name,htm]
    print(value)
    url_list += [htm]
    name_list += [name]
url_list = np.array(url_list[13:3524])#13:3524
name_list = np.array(name_list[13:3524])#[a:b]--a到b-1



stem_list = []
leaf_list = []
flower_list = []
fruit_list = []
characteristic_list = []
whole_list = []
for url_list_loop in url_list:
    res2 = requests.get(url_list_loop,headers=headers)
    res2.encoding = "utf-8"
    content = etree.HTML(res2.content)
       
    stem = content.xpath('//table[2]/tr[9]/td[2]/descendant::*/text()')
    stem = [x.replace("\r\n      ","") for x in stem]
    
    leaf = content.xpath('//table[2]/tr[10]/td[2]/descendant::*/text()')
    leaf = [x.replace("\r\n      ","") for x in leaf]
   
    flower = content.xpath('//table[2]/tr[11]/td[2]/descendant::*/text()')
    flower = [x.replace("\r\n      ","") for x in flower]
    
    fruit = content.xpath('//table[2]/tr[12]/td[2]/descendant::*/text()')
    fruit = [x.replace("\r\n      ","") for x in fruit]
    
    characteristic = content.xpath('//table[2]/tr[13]/td[2]/descendant::*/text()') #
    characteristic = [x.replace("\r\n      ","") for x in characteristic]
    
    whole = stem +leaf+flower+fruit+characteristic
    #print(whole)
    stem_list += [stem]
    leaf_list += [leaf]
    flower_list += [flower]
    fruit_list += [fruit]    
    characteristic_list += [characteristic]
    whole_list += [whole]
characteristic_list = np.array(characteristic_list)
stem_list = np.array(stem_list)
leaf_list = np.array(leaf_list)
flower_list = np.array(flower_list)
fruit_list = np.array(fruit_list)    
whole_list = np.array(whole_list)


form = {'植物名': name_list,
        'URL' : url_list,
        '莖' : stem_list,
        '葉' : leaf_list,
        '花': flower_list,
        '果實': fruit_list,
        '特性' : characteristic_list,
        '全部特徵' : whole_list }
form_df = pd.DataFrame(form)
form_df.to_csv('crawler.csv',encoding = 'utf-8_sig')



