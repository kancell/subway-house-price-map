import requests
from selenium import webdriver
import json
from selenium.webdriver import ActionChains

opt = webdriver.ChromeOptions()
opt.add_argument('--log-level=3')
#opt.set_headless() #使用chrome的headless模式以减少资源消耗
driver = webdriver.Chrome(options=opt)


url = "https://www.amap.com"

driver.get(url)
cookies = driver.get_cookies() # 获取浏览器cookies

cookieDict = []
#jsonCookies = json.dumps(cookies)
for item in cookies:
    info = item['name'] + ":" + item['value']
    cookieDict.append(info)

print(cookieDict)
#with open('qqhomepage.json', 'w') as f:
#    f.write(jsonCookies)
