FROM python
MAINTAINER best.oneself@foxmail.com
COPY ["dianping_demo_scrapy/","/dianping_demo_scrapy"]
WORKDIR /dianping_demo_scrapy
RUN pip  install  -r requirements.txt -i https://pypi.douban.com/simple
CMD scrapy crawl shop_parse |tee scrapy.log