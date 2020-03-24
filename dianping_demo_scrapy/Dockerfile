FROM python
MAINTAINER best.oneself@foxmail.com
COPY ["dianping_demo_scrapy/","/"]
WORKDIR /dianping_demo_scrapy
CMD pip -r requirements.txt -i http://pypi.douban.com/simple
RUN scrapy crawl shop_parse |tee scrapy.log