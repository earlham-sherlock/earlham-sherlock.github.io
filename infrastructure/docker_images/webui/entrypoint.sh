#!/bin/bash
set -e

echo "generating yanagishima.properties..."
mv /app/conf/yanagishima.properties /app/conf/yanagishima.properties_bak
envsubst < /app/conf/yanagishima.properties_bak > /app/conf/yanagishima.properties
rm  /app/conf/yanagishima.properties_bak
#cat /app/conf/yanagishima.properties

yanagishima_dir=/app/yanagishima

for file in $yanagishima_dir/lib/*.jar;
do
  CLASSPATH=$CLASSPATH:$file
done

executorport=`cat $yanagishima_dir/conf/yanagishima.properties | grep executor.port | cut -d = -f 2`
serverpath=`pwd`

if [ -z $YANAGISHIMA_OPTS ]; then
  YANAGISHIMA_OPTS=-Xmx3G
fi

java $YANAGISHIMA_OPTS \
    -cp $CLASSPATH yanagishima.server.YanagishimaServer \
    -conf $yanagishima_dir/conf \
    $@