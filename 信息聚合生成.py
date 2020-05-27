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
            if id1["type"] == "商务住宅;住宅区;住宅小区":
                if name["name"] in id1["name"]:                   
                    cache.append(id1)
        name["gaodeInfo"] = cache
        allInfo.append(name)
        print(name["name"],"匹配")
    jstr = json.dumps(allInfo, indent=4, sort_keys=True, ensure_ascii=False)
    saveUrl = "./数据资源/" + "小区信息聚合" + ".json"
    with open(saveUrl, "w", encoding='utf8') as f:
        f.write(jstr)
'''
def getInfo(url, id):
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "amapuuid": "c92be022-7609-484b-9692-5f9254d78cb2",
        "Connection": "keep-alive",
        "Cookie": "cna=tDiXFloW2RICAd3oLTaJ7Jqt; UM_distinctid=172094915761b1-0007eb1b7e65-c7d6957-1fa400-172094915771cf; passport_login=NDI3NjMyNjMxLGFtYXBBalBKUkE1MEcsNmI2eGdxazJkZXU0cGkzZjNxd3hqNnF3M2RhcXY2eHYsMTU4OTI5NDkwNyxZV1JtWmpNek1XWTRaVE5pWWpRNVpXRTJZMll5TlRnd1l6Tm1aalJqWmpBPQ%3D%3D; dev_help=SIcdWg%2FpX3uhMT34PIBOKjdjOGM4MzIyZDIzMGM2MTJkMWU5NWZhYjA1NWZhYmM0ZmRjNTA0NWEyMTYyOGI2N2RmN2Q4NmEwMDIzNmEyNjX5l9ZDgBR71%2FrcU2BHHQs43%2BtpuvZvsZfdZc7rY4Wjjy8Yw1onDQd7eIrT80qx7yzoZuSNwxwGC0aVVvXUSQwpkUQUx1cUmhvl5JV79GhnUgdYiRL3TeVb4o4Bdspy6Kg%3D; _uab_collina=158998832822468132723203; CNZZDATA1255626299=730330766-1589988259-https%253A%252F%252Fwww.baidu.com%252F%7C1590319756; guid=eead-c8f5-4cf0-3554; x5sec=7b22617365727665723b32223a226661313136323261326162363338396438383430323063303931306237326239434b2f6a71665946454b374b36397233304d32764d513d3d227d; l=eB_QCqogQlmehfuvBO5CFurza779qBAhCkPzaNbMiInca66l3pacaNQD_N0H4dtjgtf0fetrs9cQBREX7qzU-A_euqhzS8Xtp2p9-; isg=BImJwAAAM_ImyM92KdqO0neHlrXj1n0IkV5Lqyv4TXCvcqyEcyUT2aPstNZEMRVA",
        "Host": "www.amap.com",
        "Referer": "https://www.amap.com/place/B001B0BCHS",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0",
        "x-csrf-token": "null",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "id": id
    }
    r = requests.get(url, headers = header,verify=False,params=data).json()
    info = r["data"]["spec"]["mining_shape"]["shape"]
    print(info)
'''
generator()