#!/bin/bash

echo "hdfs-site.xml:"
mv /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml_bak
envsubst < /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml_bak > /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml
cat /opt/apache-hive-3.1.1-bin/conf/hdfs-site.xml

echo "hive-site.xml:"
mv /opt/apache-hive-3.1.1-bin/conf/hive-site.xml /opt/apache-hive-3.1.1-bin/conf/hive-site.xml_bak
envsubst < /opt/apache-hive-3.1.1-bin/conf/hive-site.xml_bak > /opt/apache-hive-3.1.1-bin/conf/hive-site.xml
cat /opt/apache-hive-3.1.1-bin/conf/hive-site.xml

V=$(/opt/apache-hive-3.1.1-bin/bin/schematool -info -dbType postgres |  grep version | cut -d: -f2)
NV=$(echo $V | tr ' ' '\n' | wc -l)
SAME=$(echo $V | tr ' ' '\n'  | uniq | wc -l)
if [[ -z "${V}" || "${NV}" != "2" ||  "${SAME}" != "1" ]];
then
    /opt/apache-hive-3.1.1-bin/bin/schematool  --dbType postgres --initSchema
fi
/opt/apache-hive-3.1.1-bin/bin/hive  --service metastore