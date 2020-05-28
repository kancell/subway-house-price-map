#根据小区id抓取轮廓信息
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
import asyncio
import time
import re
import json

url = "https://www.amap.com/detail/get/detail?id"

def loadId():
    with open("./数据资源/高德信息.json",'r',encoding='utf8') as loadInfo:
        idInfo  = json.load(loadInfo)
        return idInfo

def loadName():
    with open("./数据资源/链家信息.json",'r',encoding='utf8') as loadInfo:
        NameInfo  = json.load(loadInfo)
        return NameInfo


allInfo = []

def generator():
    idInfo = loadId()
    NameInfo = loadName()
    for name in NameInfo: 
        cache = []
        for id1 in idInfo:
            if "住宅区" in id1["type"]:
                if name["name"] in id1["name"].replace("·",""):                   
                    cache.append(id1)
        name["gaodeInfo"] = cache
        allInfo.append(name)
        print(name["name"],"匹配")
    jstr = json.dumps(allInfo, indent=4, sort_keys=True, ensure_ascii=False)
    saveUrl = "./数据资源/" + "小区信息聚合" + ".json"
    with open(saveUrl, "w", encoding='utf8') as f:
        f.write(jstr)

generator()