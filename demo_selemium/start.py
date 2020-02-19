
from selenium import webdriver
import os
import time
from scrapy.http import HtmlResponse

driver_path = "D:\gitProject\scrapyDemo\demo_selemium\chromedriver80.0.3987.16.exe"

browser = webdriver.Chrome(driver_path)
browser.implicitly_wait(30)  # 隐性等待，最长等30秒
browser.get('http://www.dianping.com/')
#browser.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")

#browser.find_element_by_id("su").click()

source = browser.page_source       #获取到页面源码数据
response = HtmlResponse(url=browser.current_url,body=source,encoding='utf-8')

print(response.headers)
print(response.url)



