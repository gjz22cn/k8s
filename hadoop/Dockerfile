FROM openjdk:8-jdk
#RUN apt-get update;
#RUN apt-get install -y net-tools vim git;
#RUN sed -i -r 's/^\s*UseDNS\s+\w+/#\0/; s/^\s*PasswordAuthentication\s+\w+/#\0/; s/^\s*ClientAliveInterval\s+\w+/#\0/' /etc/ssh/sshd_config;
#RUN echo 'UseDNS no \nPermitRootLogin yes \nPasswordAuthentication yes \nClientAliveInterval 30' >> /etc/ssh/sshd_config;
#RUN cat /etc/ssh/sshd_config
#RUN su root bash -c 'cd;mkdir .ssh;chmod 700 .ssh;echo ${SSH_PUB} > .ssh/authorized_keys;chmod 644 .ssh/authorized_keys'
#RUN su root bash -c 'cd;ssh-keygen -t rsa -f ~/.ssh/id_rsa; cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys'
# hadoop
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH
RUN mkdir -p $HADOOP_HOME
COPY hadoop-3.3.4.tar.gz $HADOOP_HOME/src.tgz
RUN set -ex; \
    tar -xf $HADOOP_HOME/src.tgz --strip-components=1 -C $HADOOP_HOME; \
    rm $HADOOP_HOME/src.tgz; \
    chown -R root:root $HADOOP_HOME
RUN mkdir -p $HADOOP_HOME/hdfs/name/ && mkdir -p $HADOOP_HOME/hdfs/data/
COPY rack_topology.sh $HADOOP_HOME/etc/hadoop/
RUN chmod +x $HADOOP_HOME/etc/hadoop/rack_topology.sh
# clean trash file or dir
RUN rm -rf $HADOOP_HOME/share/doc/;
COPY docker-entrypoint.sh /
EXPOSE 9870 9000
ENTRYPOINT ["/docker-entrypoint.sh"]
