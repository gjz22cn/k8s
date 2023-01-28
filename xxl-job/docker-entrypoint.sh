#!/usr/bin/env bash

if [ $EXEC_MODE = "admin" ]; then
    java -jar /xxl-job-admin.jar --spring.config.location=/data/java/config/application-admin.properties
elif [ $EXEC_MODE = "executor" ]; then
    java -jar /xxl-job-executor-sample-springboot.jar --spring.config.location=/data/java/config/application-executor.properties
elif [ $EXEC_MODE = "all" ]; then
    java -jar /xxl-job-admin.jar --spring.config.location=/data/java/config/application-admin.properties &
    java -jar /xxl-job-executor-sample-springboot.jar --spring.config.location=/data/java/config/application-executor.properties
fi

