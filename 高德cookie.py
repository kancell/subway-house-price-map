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

gaodeCookie = {}
# 获取cookie中的name和value,转化成requests可以使用的形式


def dargBlock(id):
    url = "https://www.amap.com/place/" + id
    driver.get(url)
    """ 
    if (driver.find_element_by_xpath('//*[@class="sufei-dialog-content"]').is_displayed()):
        driver.switch_to_frame("sufei-dialog-content")
        dargBlock = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        move_to_gap(dargBlock, get_track(340))
        time.sleep(1)
        verify = driver.find_elements_by_xpath("//a[@href='javascript:noCaptcha.reset(1)']")
        while(len(verify) != 0):
            verify[0].click()
            dargBlock = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            move_to_gap(dargBlock, get_track(340))
            time.sleep(1)
            verify = driver.find_elements_by_xpath("//a[@href='javascript:noCaptcha.reset(1)']")
    """ 
    time.sleep(10) #学会回调之后优化
""" 
def dargBlock(id):    
    url = "https://www.amap.com/place/" + id
    driver.get(url)
    time.sleep(10)

    if (driver.find_element_by_xpath('//*[@class="sufei-dialog-content"]').is_displayed()):
        driver.switch_to_frame("sufei-dialog-content")
        print(driver.find_element_by_class_name('nc-lang-cnt').text)
        verf = (driver.find_element_by_class_name('nc-lang-cnt').text == '验证通过')
        while (verf == False):  
            print("d等待") 
            verf = driver.find_element_by_class_name('nc-lang-cnt').text == '验证通过'    


    verify1 = driver.find_elements_by_xpath('//*[@class="sufei-dialog-content"]')



    verify1 = driver.find_elements_by_xpath('//*[@class="sufei-dialog-content"]')
    
    if (len(verify1) != 0):
        driver.switch_to_frame("sufei-dialog-content")
        dargBlock = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        move_to_gap(dargBlock, get_track(340))
        time.sleep(1)
        verify = driver.find_elements_by_xpath("//a[@href='javascript:noCaptcha.reset(1)']")
        while(len(verify) != 0):
            verify[0].click()
            dargBlock = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            move_to_gap(dargBlock, get_track(335))
            time.sleep(1)
            verify = driver.find_elements_by_xpath("//a[@href='javascript:noCaptcha.reset(1)']")
"""    

def move_to_gap(slider,tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()

def get_track(distance):      # distance为传入的总距离
    rand1 = random.uniform(0.7,1.0)  
    # 移动轨迹
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5 * rand1
    # 计算间隔
    t=0.2 * rand1
    # 初速度
    v=1 * rand1  
    while current<distance:
        if current<mid:
            # 加速度为2
            a=4
        else:
            # 加速度为-2
            a=-3
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
        print(track)
    return track


def getCookie():
    cookies = driver.get_cookies()
    driver.close()
    return cookies

def getShape(id):
    print("开始抓取")
    data = {"id": id}
    url = "https://www.amap.com/detail/get/detail"
    r = requests.get(url, headers = header, cookies=gaodeCookie, params=data).json()

    if ('data' in r):   
        print('利用gaodeCookie抓取成功')
        print(r)
    else:      
        print('抓取失败，开始使用headless验证，获取gaodeCookie')
        dargBlock(id)

        for cookie in getCookie():
            gaodeCookie[cookie['name']] = cookie['value']
        time.sleep(1)
        print(requests.get(url, headers=header, cookies=gaodeCookie, params=data).json())

getShape("B001B0IZEG")
getShape("B001B0IZEH")
getShape("B0FFGZB2SK")