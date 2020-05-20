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
        for item in info:
            print(item["allSell"])
        return info

def getUrl(residentialQuarters):
    url = "https://restapi.amap.com/v3/place/text?key=4b86820a7590de60e4f81f53e59ae17f&citylimit=true&output=json&keywords=" +residentialQuarters+ "&city=武汉"
    return url

def generator():
    info = loadJson()
    for item in info:
        url = getUrl(item["name"])
        getId(url)

def getId(url):
    print(url)

generator()