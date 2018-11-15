FROM sherlockdatalake/base:8u191

ENV HADOOP_HOME /opt/hadoop-3.1.1
ENV HADOOP_USER_CLASSPATH_FIRST true

EXPOSE 9083

RUN cd /opt && \
    wget http://xenia.sote.hu/ftp/mirrors/www.apache.org/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz && \
    tar xzf hadoop-3.1.1.tar.gz && \
    rm hadoop-3.1.1.tar.gz && \
    wget http://xenia.sote.hu/ftp/mirrors/www.apache.org/hive/hive-3.1.0/apache-hive-3.1.0-bin.tar.gz && \
    tar xzf apache-hive-3.1.0-bin.tar.gz && \
    rm apache-hive-3.1.0-bin.tar.gz && \
    wget https://jdbc.postgresql.org/download/postgresql-42.2.5.jar && \
    mv /opt/postgresql-42.2.5.jar /opt/apache-hive-3.1.0-bin/lib/. && \
    cp ./hadoop-3.1.1/share/hadoop/tools/lib/hadoop-aws-3.1.1.jar ./apache-hive-3.1.0-bin/lib/ && \
    cp ./hadoop-3.1.1/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.271.jar ./apache-hive-3.1.0-bin/lib/

ADD conf/* /opt/apache-hive-3.1.0-bin/conf/

COPY cmd.sh /cmd.sh
RUN chmod +x /cmd.sh

CMD /cmd.sh