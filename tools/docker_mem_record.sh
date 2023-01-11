#!/bin/bash

save_dir=/root/docker_stats
if [ ! -d "$save_dir" ];then
    mkdir $save_dir
fi

while true; do
    DATE=`date '+%Y%m%d%H%M%S'`
    docker ps -q | xargs  docker stats --no-stream > $save_dir/docker_sts_$DATE
    sleep 1h
done
