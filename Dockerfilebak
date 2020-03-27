FROM python/scrapy
COPY ["dianping_demo_scrapy/","/"]
WORKDIR /dianping_demo_scrapy
CMD  scrapy crawl shop_parse |tee scrapy.log 


