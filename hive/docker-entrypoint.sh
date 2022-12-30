#!/usr/bin/env bash

if [[ ! -e $HIVE_HOME/hive-metastore-initialization.out ]]; then
    $HADOOP_HOME/bin/hadoop fs -mkdir -p /tmp
    $HADOOP_HOME/bin/hadoop fs -mkdir -p hdfs://hdfs-master.hadoop:9000/user/hive/warehouse
    $HADOOP_HOME/bin/hadoop fs -chmod g+w /tmp
    $HADOOP_HOME/bin/hadoop fs -chmod g+w hdfs://hdfs-master.hadoop:9000/user/hive/warehouse

    $HIVE_HOME/bin/schematool -dbType mysql -initSchema --verbose &> $HIVE_HOME/hive-metastore-initialization.out
fi

if [ $NODE_TYPE = "hiveserver2" ]; then
    hiveserver2
elif [ $NODE_TYPE = "metastore" ]; then
    hive --service metastore -p 9083
fi

#sleep infinity
