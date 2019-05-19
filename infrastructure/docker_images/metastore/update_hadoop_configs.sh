#!/usr/bin/env bash


echo "creating hdfs-site.xml..."
mv /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml_bak
envsubst < /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml_bak > /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml
#cat /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml

echo "creating hive-site.xml..."
mv /opt/apache-hive-3.1.1-bin/conf/hive-site.xml /opt/apache-hive-3.1.1-bin/conf/hive-site.xml_bak
envsubst < /opt/apache-hive-3.1.1-bin/conf/hive-site.xml_bak > /opt/apache-hive-3.1.1-bin/conf/hive-site.xml
#cat /opt/apache-hive-3.1.1-bin/conf/hive-site.xml
