#!/bin/bash

echo "config.properties:"
mv /opt/presto/etc/config.properties /opt/presto/etc/config.properties_bak
envsubst < /opt/presto/etc/config.properties_bak > /opt/presto/etc/config.properties
rm  /opt/presto/etc/config.properties_bak
cat /opt/presto/etc/config.properties

echo "node.properties"
mv /opt/presto/etc/node.properties /opt/presto/etc/node.properties_bak
envsubst < /opt/presto/etc/node.properties_bak > /opt/presto/etc/node.properties
rm /opt/presto/etc/node.properties_bak
cat /opt/presto/etc/node.properties

echo "catalog/sherlock.properties"
mv /opt/presto/etc/catalog/sherlock.properties /opt/presto/etc/catalog/sherlock.properties_bak
envsubst < /opt/presto/etc/catalog/sherlock.properties_bak > /opt/presto/etc/catalog/sherlock.properties
rm  /opt/presto/etc/catalog/sherlock.properties_bak
cat /opt/presto/etc/catalog/sherlock.properties

echo "jvm.config"
mv /opt/presto/etc/jvm.config /opt/presto/etc/jvm.config_bak
envsubst < /opt/presto/etc/jvm.config_bak > /opt/presto/etc/jvm.config
rm  /opt/presto/etc/jvm.config_bak
cat /opt/presto/etc/jvm.config

/opt/presto/bin/launcher run