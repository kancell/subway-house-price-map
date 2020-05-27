#根据小区名字抓取高德地图中的小区id
import requests
from bs4 import BeautifulSoup
import asyncio
import time
import re
import random
import json

def loadJson():
    with open("./数据资源/链家信息.json",'r',encoding='utf8') as loadInfo:
        info  = json.load(loadInfo)
        return info

def getUrl(residentialQuarters):
    url = "https://restapi.amap.com/v3/place/text?key=4b86820a7590de60e4f81f53e59ae17f&citylimit=true&output=json&keywords=" +residentialQuarters+ "&city=武汉"
    return url

infoList = []
def generator():
    info = loadJson()
    for item in info:  
        url = getUrl(item["name"])
        getId(url, item["name"])
        time.sleep(random.randint(1, 4))

    jstr = json.dumps(infoList, indent=2,sort_keys=True, ensure_ascii=False)
    saveUrl = "./数据资源/" + "高德信息" + ".json"
    with open(saveUrl, "w", encoding='utf8') as f:
        f.write(jstr)
    
def getId(url, name):
    r = requests.get(url)
    info = r.json()["pois"] #以后记得做错误处理


    for item in info:
        infoDict = {}
        infoDict["id"] = item["id"]
        infoDict["name"] = item["name"]
        infoDict["type"] = item["type"]
        infoDict["address"] = item["address"]
        infoDict["location"] = item["location"]
        infoDict["pname"] = item["pname"]
        infoDict["cityname"] = item["cityname"]
        infoDict["adname"] = item["adname"]
        
        infoList.append(infoDict)
    print(name + "爬取完毕")
generator()