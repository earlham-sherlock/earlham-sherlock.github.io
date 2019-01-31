#!/bin/bash

echo "config.properties:"
mv /opt/presto/etc/config.properties /opt/presto/etc/config.properties_bak
envsubst < /opt/presto/etc/config.properties_bak > /opt/presto/etc/config.properties
cat /opt/presto/etc/config.properties

echo "node.properties"
mv /opt/presto/etc/node.properties /opt/presto/etc/node.properties_bak
envsubst < /opt/presto/etc/node.properties_bak > /opt/presto/etc/node.properties
cat /opt/presto/etc/node.properties

echo "catalog/sherlock.properties"
mv /opt/presto/etc/catalog/sherlock.properties /opt/presto/etc/catalog/sherlock.properties_bak
envsubst < /opt/presto/etc/catalog/sherlock.properties_bak > /opt/presto/etc/catalog/sherlock.properties
cat /opt/presto/etc/catalog/sherlock.properties

/opt/presto/bin/launcher run