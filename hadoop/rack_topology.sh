#!/bin/bash
nodeIp=$(echo $1 | tr . -)
echo -n "/rack-$nodeIp"
