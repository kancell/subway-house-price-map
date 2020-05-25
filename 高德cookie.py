import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import json
from selenium.webdriver import ActionChains
import time
import random
opt = webdriver.ChromeOptions()
opt.add_experimental_option('excludeSwitches', ['enable-automation'])
opt.add_argument('--log-level=3')
#opt.set_headless() #使用chrome的headless模式以减少资源消耗
driver = webdriver.Chrome(options=opt)



def dargBlock():
    
    url = "https://www.amap.com/place/B001B0IO3B"
    driver.get(url)
    driver.switch_to_frame("sufei-dialog-content")
    dargBlock = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    move_to_gap(dargBlock, get_track(340))

    l = driver.find_elements_by_xpath("//a[@href='javascript:noCaptcha.reset(1)']")
    while(len(l) != 0):
        l[0].click()
        dargBlock = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        move_to_gap(dargBlock, get_track(340))
        l = driver.find_elements_by_xpath("//a[@href='javascript:noCaptcha.reset(1)']")
    

def move_to_gap(slider,tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()

def get_track(distance):      # distance为传入的总距离
    rand1 = random.uniform(0.7,1.1)
    
    # 移动轨迹
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5 * rand1
    # 计算间隔
    t=0.2 * rand1
    # 初速度
    v=1 *rand1

    

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
    return track
    

def getCookie():
    cookies = driver.get_cookies() # 获取浏览器cookies
    cookieDict = []
    for item in cookies:
        info = item['name'] + ":" + item['value']
        cookieDict.append(info)
    print(cookieDict)


def getShape():
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
        "id": "B001B0IZEG"
    }
    url = "https://www.amap.com/detail/get/detail"
    r = requests.get(url, headers = header,verify=False,params=data).json()

    if ('data' in r):
        getCookie()
        print(r["data"]["spec"]["mining_shape"]["shape"])
    else:
        dargBlock()

getShape()