FROM hadoop:3.3.4

ADD apache-hive-3.1.3-bin.tar.gz /opt

RUN mv /opt/apache-hive-3.1.3-bin /opt/hive

ADD mysql-connector-java-8.0.22.jar /opt/hive/lib
ADD iceberg-hive-runtime-0.13.2.jar /opt/hive/lib
ADD libfb303-0.9.3.jar /opt/hive/lib

ENV HADOOP_HOME /opt/hadoop
ENV HIVE_HOME /opt/hive

ENV HADOOP_COMMON_HOME=${HADOOP_HOME} \
    HADOOP_HDFS_HOME=${HADOOP_HOME} \
    HADOOP_MAPRED_HOME=${HADOOP_HOME} \
    HADOOP_YARN_HOME=${HADOOP_HOME} \
    HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop \
    PATH=${PATH}:${HADOOP_HOME}/bin:${HIVE_HOME}/bin


COPY docker-entrypoint.sh /
EXPOSE 9083
ENTRYPOINT ["/docker-entrypoint.sh"]
