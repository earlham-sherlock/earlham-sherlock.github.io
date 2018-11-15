#!/bin/bash

V=$(/opt/apache-hive-3.1.0-bin/bin/schematool -info -dbType postgres |  grep version | cut -d: -f2)
NV=$(echo $V | tr ' ' '\n' | wc -l)
SAME=$(echo $V | tr ' ' '\n'  | uniq | wc -l)
if [[ -z "${V}" || "${NV}" != "2" ||  "${SAME}" != "1" ]];
then
    /opt/apache-hive-3.1.0-bin/bin/schematool  --dbType postgres --initSchema
fi
/opt/apache-hive-3.1.0-bin/bin/hive  --service metastore