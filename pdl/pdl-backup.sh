#!/bin/bash

kubectl get pv -A -o yaml > pv.yaml
kubectl get pvc -A -o yaml > pvc.yaml

declare -a nss=("default" "dubbo" "flink" "hadoop" "hive" "kafka" "mysql" "presto" "redis" "xxl-job" "zookeeper")

for ns in "${nss[@]}"
do
    if [ ! -d "$ns" ];then
        mkdir $ns
    fi
    kubectl get cm -n $ns -o yaml > $ns/$ns-cm.yaml
    #kubectl get pods -n $ns -o yaml > $ns/$ns-pods.yaml
    kubectl get deploy -n $ns -o yaml > $ns/$ns-deploy.yaml
    kubectl get svc -n $ns -o yaml > $ns/$ns-svc.yaml
done
