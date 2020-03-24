#!/bin/bash
image_run_id=` docker ps -a |awk '/dianping/{print $1}'`
image_id=` docker images |awk '/dianping/{print $3}'`
image_stop_id=`docker ps|awk '/scrapy:dianping/{print $1}'`
[ $image_stop_id ] && docker stop $image_stop_id
[ $image_run_id ] && docker rm $image_run_id
[ $image_id ] && docker rmi $image_id
docker build -t scrapy:dianping .
if [ $? == 0 ];then
	echo "build successful,begin run new image"
	docker run scrapy:dianping
fi
