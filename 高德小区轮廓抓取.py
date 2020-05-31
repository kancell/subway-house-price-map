import requests
requests.packages.urllib3.disable_warnings()
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import json
from selenium.webdriver import ActionChains
import time
import random
opt = webdriver.ChromeOptions()
opt.add_experimental_option('excludeSwitches', ['enable-automation']) #较早版本的chrome跳过window.navigator.webdriver检测
opt.add_experimental_option('useAutomationExtension', False) #较早版本的chrome跳过window.navigator.webdriver检测
opt.add_argument('--log-level=3') #消除控制台报错
#opt.add_argument('blink-settings=imagesEnabled=false') #浏览器无图模式
#opt.set_headless() #使用chrome的headless模式以减少资源消耗
driver = webdriver.Chrome(options=opt)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
}) #新版chrome跳过window.navigator.webdriver检测
header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "amapuuid": "b8c17e6b-0ba1-4b80-bad2-bb8fa4a3ab68",
    "Connection": "keep-alive",
    "Host": "www.amap.com", 
    "Referer": "https://www.amap.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0",
    "x-csrf-token": "null",
    "X-Requested-With": "XMLHttpRequest"
}

allInfo = []
gaodeCookie = {}
# 获取cookie中的name和value,转化成requests可以使用的形式

def dargBlock(id):
    url = "https://www.amap.com/place/" + id
    driver.get(url)
    time.sleep(12) #学会回调之后优化

def getCookie():
    cookies = driver.get_cookies()
    return cookies

def getShape(id):
    print("开始抓取")
    data = {"id": id}
    url = "https://www.amap.com/detail/get/detail"
    r = requests.get(url, headers = header, cookies=gaodeCookie, params=data).json()
    cache = {}
    cache["id"] = id

    if ('data' in r):   
        print('利用gaodeCookie抓取成功')
        cache["data"] = r
    else:      
        print('抓取失败，开始使用headless验证，获取gaodeCookie')
        dargBlock(id)
        for cookie in getCookie():
            gaodeCookie[cookie['name']] = cookie['value']
        time.sleep(1)
        cache["data"] = requests.get(url, headers=header, cookies=gaodeCookie, params=data).json()
        print('利用dargBlock抓取成功')
    allInfo.append(cache)

def loadId():
    with open("./数据资源/高德信息.json",'r',encoding='utf8') as loadInfo:
        idInfo  = json.load(loadInfo)
        return idInfo

def generator():
    info = loadId()
    for item in info:
        if ("id" in item):
            time.sleep(random.randint(1, 10))
            getShape(item["id"])
            print(item["id"])
    jstr = json.dumps(allInfo, indent=4, sort_keys=True, ensure_ascii=False)
    saveUrl = "./数据资源/" + "小区轮廓信息" + ".json"
    with open(saveUrl, "w", encoding='utf8') as f:
        f.write(jstr)

generator()            
