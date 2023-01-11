FROM hadoop:3.3.4

ADD apache-hive-3.1.3-bin.tar.gz /opt

RUN mv /opt/apache-hive-3.1.3-bin /opt/apache-hive-3.1.3

ADD mysql-connector-java-8.0.27.jar /opt/apache-hive-3.1.3/lib
ADD iceberg-hive-runtime-0.13.2.jar /opt/apache-hive-3.1.3/lib
ADD libfb303-0.9.3.jar /opt/apache-hive-3.1.3/lib

ENV HADOOP_HOME /opt/hadoop
ENV HIVE_HOME /opt/apache-hive-3.1.3

ENV PATH $HIVE_HOME/bin:$HADOOP_HOME/bin:$PATH

COPY docker-entrypoint.sh /
EXPOSE 9083
ENTRYPOINT ["/docker-entrypoint.sh"]
