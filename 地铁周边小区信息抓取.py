#https://wh.lianjia.com/xiaoqu/su1/?from=rec
#爬取小区名字等信息
import requests
from bs4 import BeautifulSoup
from lxml import etree
import asyncio
import time
import re
import json

pagenum = {}
def get_num():
    url = "https://wh.lianjia.com/xiaoqu/su1/?from=rec"
    r = requests.get(url).text
    num = int(etree.HTML(r).xpath("//h2[@class='total fl']/span/text()")[0].strip())
    print(num)
 

def getPage():
    r = requests.get("https://wh.lianjia.com/xiaoqu/su1/?from=rec")       
    soup = BeautifulSoup(r.text, "html5lib")
    pagenum = eval(soup.html.body.find(class_="page-box house-lst-page-box").attrs["page-data"])["totalPage"]
    print(pagenum)
    getInfo(1)


def getInfo(i):
    url = "https://wh.lianjia.com/xiaoqu/su" + str(i) + "/?from=rec"
    r = requests.get(url)
        
    soup = BeautifulSoup(r.text, "html5lib")

    list1 = soup.html.body.find_all(class_="clear xiaoquListItem")
    for child in list1:
        dict = {}
        dict['name'] = child.find(class_="info").find(class_="title").a.text.strip() #小区名字
        dict['allSell'] = child.find(class_="info").find(class_="houseInfo").find_all("a")[0].text.strip()#成交套数
        dict['lease'] = child.find(class_="info").find(class_="houseInfo").find_all("a")[1].text.strip() #出租套数
        dict['area'] = child.find(class_="info").find(class_="positionInfo").find_all("a")[0].text.strip() #行政区域
        dict['detailArea'] = child.find(class_="info").find(class_="positionInfo").find_all("a")[1].text.strip() #详细区域
        dict['buildYear'] = child.find(class_="info").find(class_="positionInfo").contents[6].replace('\n', '').replace('\r', '').strip()[2:] #建成年份 未正常工作
        dict['subway'] = child.find(class_="info").find(class_="tagList").text.strip().replace("\n", "") #近地铁情况      
        dict['price'] = child.find(class_="xiaoquListItemRight").find(class_="totalPrice").span.text.strip() #小区均价
        dict['nowSell'] = child.find(class_="xiaoquListItemRight").find(class_="xiaoquListItemSellCount").a.span.text.strip() #小区在售套数
        print(dict)
        
#print (soup.html.body.find_all(class_="leftContent"))
getPage()