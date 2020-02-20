
from selenium import webdriver
import os
import time
from scrapy.http import HtmlResponse



    
def parse(c):
    if c:
        print("*"*50)
        for cookie in c:
            print(cookie["name"] , ":" ,cookie["value"])

        

driver_path = "D:\gitProject\scrapyDemo\demo_selemium\chromedriver80.0.3987.16.exe"

driver = webdriver.Chrome(executable_path=driver_path)
driver.implicitly_wait(10)  # 隐性等待，最长等10秒
driver.get('http://www.dianping.com/')

#driver.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")
#driver.find_element_by_id("su").click()

source = driver.page_source       #获取到页面源码数据
#response = HtmlResponse(url=driver.current_url,body=source,encoding='utf-8')

a1 = driver.get_cookies()

driver.get("http://www.dianping.com/guangzhou/ch50/g157")
a2 = driver.get_cookies()

driver.get("http://www.dianping.com/shop/22740302")
a3 = driver.get_cookies()
driver.delete_all_cookies()

time.sleep(5)
driver.get("http://www.dianping.com/shop/22740302")
driver.delete_all_cookies()
print("add cookie renew get shop")
time.sleep(5)
for i in a1:
    del i["expiry"]
    driver.add_cookie(cookie_dict=i)
driver.get("http://www.dianping.com/shop/22740302")
a4 = driver.get_cookies()


for i in a1,a2,a3,a4:
    parse(c=i)
       


