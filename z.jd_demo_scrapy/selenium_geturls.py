from lxml import etree
from selenium import webdriver
import os
import csv
import time


class GetUrls(object):
    def __init__(self):
        self.driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
        self.browser = webdriver.Chrome(self.driver_path)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
        self.browser.set_window_size(700, 1000)
        fileName = 'url.csv'
        self.file = open(fileName, 'a+', newline='')
        self.writer = csv.writer(self.file,dialect='excel')
    def start_requests(self,url):
        self.browser.get(url)
        time.sleep(3)
        for i in range(2,10):
            self.browser.find_element_by_xpath(f"//ul[@class='l-list clearfix fl']/li[@class='fl'][{i}]/a[@id='parentId']").click()
            time.sleep(3)
            html = etree.HTML(self.browser.page_source)
            while True:
                zc_urls = html.xpath('//div[@class="i-tits  no-color-choose"]/a/@href')
                for url in zc_urls:
                    print(url)
                    self.writer.writerow([url])
                if html.xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']/text()"):
                    try:
                        self.browser.find_element_by_xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']").click()
                        html = etree.HTML(self.browser.page_source)
                        print("this try click")
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                else:
                    break
        self.file.close()
if __name__ == "__main__":
    geturl = GetUrls()
    root_url = "https://z.jd.com/bigger/search.html"
    geturl.start_requests(root_url)

