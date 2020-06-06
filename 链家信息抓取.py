#https://wh.lianjia.com/xiaoqu/su1/?from=rec
#爬取小区名字等信息
#按页码只拿到30页信息，需要按网址继续抓取
#当前仅为武汉近地铁，后期加入城市、价格、位置选择，楼龄20年内
import requests
from bs4 import BeautifulSoup
import random
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
 
infoList = []
def getPage():
    r = requests.get("https://wh.lianjia.com/xiaoqu/su1/?from=rec")       
    soup = BeautifulSoup(r.text, "html5lib")
    pagenum = eval(soup.html.body.find(class_="page-box house-lst-page-box").attrs["page-data"])["totalPage"]
    print(pagenum)
    i = 1
    pagenum = 44
    while(i <= pagenum):
        
        time.sleep(random.randint(1, 10))
        print(i)
        getInfo(i)
        i = i+1
        

    jstr = json.dumps(infoList, indent=2,sort_keys=True, ensure_ascii=False)
    saveUrl = "./数据资源/" + "链家信息"  + ".json"
    with open(saveUrl, "w", encoding='utf8') as f:
        f.write(jstr)

def getInfo(i):
    url = "https://wh.lianjia.com/xiaoqu/su1pg"+ str(i) +"y4/" #近地铁二十年内楼龄
    print(url)
    r = requests.get(url)
        
    soup = BeautifulSoup(r.text, "html5lib")
    list1 = soup.html.body.find_all(class_="clear xiaoquListItem")

    
    
    for child in list1:
        infoDict = {}
        infoDict['name'] = child.find(class_="info").find(class_="title").a.text.strip() #小区名字
        infoDict['allSell'] = child.find(class_="info").find(class_="houseInfo").find_all("a")[0].text.strip()#成交套数
        infoDict['lease'] = child.find(class_="info").find(class_="houseInfo").find_all("a")[1].text.strip() #出租套数
        infoDict['area'] = child.find(class_="info").find(class_="positionInfo").find_all("a")[0].text.strip() #行政区域
        infoDict['detailArea'] = child.find(class_="info").find(class_="positionInfo").find_all("a")[1].text.strip() #详细区域
        infoDict['buildYear'] = child.find(class_="info").find(class_="positionInfo").contents[6].replace('\n', '').replace('\r', '').strip()[2:] #建成年份 未正常工作
        infoDict['subway'] = child.find(class_="info").find(class_="tagList").text.strip().replace("\n", "") #近地铁情况      
        infoDict['price'] = child.find(class_="xiaoquListItemRight").find(class_="totalPrice").span.text.strip() #小区均价
        infoDict['nowSell'] = child.find(class_="xiaoquListItemRight").find(class_="xiaoquListItemSellCount").a.span.text.strip() #小区在售套数
        infoList.append(infoDict)
    print("第" + str(i) + "页抓取完成")


#print (soup.html.body.find_all(class_="leftContent"))
getPage()