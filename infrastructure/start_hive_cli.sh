#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh


echo -e "\n======="
echo -e "======= starting a local hive-cli"
echo -e "=======\n"


SERVICE_ID=`docker service ls --filter name=sherlock-metastore -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock metastore docker service is not running yet!"
    echo "please start the metastore before starting a command line hive client"
    exit 1
fi

IMAGE=`docker service ps sherlock-metastore | grep Running | grep sherlock-metastore |  awk '{print $3}'`

docker run \
   --rm \
   -it \
  --env HIVE_DEFAULT_FS="s3a://${SHERLOCK_BUCKET_NAME}/" \
  --env S3_ACCESS_KEY="${SHERLOCK_S3_ACCESS_KEY}" \
  --env S3_SECRET_KEY="${SHERLOCK_S3_SECRET_KEY}" \
  --env S3_END_POINT="${SHERLOCK_S3_END_POINT}" \
  --env S3_PATH_STYLE_ACCESS="${SHERLOCK_S3_PATH_STYLE_ACCESS}" \
  --env HIVE_METASTORE_URI="thrift://sherlock-metastore:9083" \
  --network sherlock-overlay \
   $IMAGE \
   /bin/bash -c "/update_hadoop_configs.sh && /opt/apache-hive-3.1.1-bin/bin/hive"

# to enable debug logging, add:
# -hiveconf hive.root.logger=DEBUG,console

# to execute single HQL command:
# -e "show databases;"

# to overwrite hive configs:
# -hiveconf hive.metastore.uris=thrift://sherlock-metastore:9083