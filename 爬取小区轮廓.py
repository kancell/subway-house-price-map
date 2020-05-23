#根据小区名字抓取高德地图中的小区id
import requests
from bs4 import BeautifulSoup
from lxml import etree
import asyncio
import time
import re
import json

def loadJson():
    with open("小区信息.json",'r',encoding='utf8') as loadInfo:
        info  = json.load(loadInfo)
        return info

def getUrl(residentialQuarters):
    url = "https://restapi.amap.com/v3/place/text?key=4b86820a7590de60e4f81f53e59ae17f&citylimit=true&output=json&keywords=" +residentialQuarters+ "&city=武汉"
    return url

def generator():
    info = loadJson()
    for item in info:
        url = getUrl(item["name"])
        getId(url, item["name"])

def getId(url, name):
    r = requests.get(url)
    info = r.json()["pois"] #以后记得做错误处理

    infoList = []
    for item in info:
        infoDict = {}
        infoDict["id"] = item["id"]
        infoDict["name"] = item["name"]
        infoList.append(infoDict)

    jstr = json.dumps(infoList, indent=2,sort_keys=True, ensure_ascii=False)

    saveUrl = "./小区名称ID对应表/" + name  + ".json"
    with open(saveUrl, "w", encoding='utf8') as f:
        f.write(jstr)

generator()