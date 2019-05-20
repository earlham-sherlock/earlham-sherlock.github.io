#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh

SERVICE_NAME="sherlock-metastore"

echo -e "\n======="
echo -e "======= starting service: ${SERVICE_NAME}"
echo -e "=======\n"


SERVICE_ID=`docker service ls --filter name=${SERVICE_NAME} -q`
if [[ -n "${SERVICE_ID}" ]]
then
    echo "ERROR! docker service ${SERVICE_NAME} is already running!"
    echo "if you want to restart it, then please stop it first (e.g. using command: docker service rm ${SERVICE_NAME})"
    exit 1
fi


SERVICE_ID=`docker service ls --filter name=sherlock-postgres -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock postgres docker service is not running yet!"
    echo "please start sherlock postgres before starting the metastore"
    exit 1
fi


docker service create  \
  --with-registry-auth  \
  --name ${SERVICE_NAME}  \
  --container-label ${SERVICE_NAME}  \
  --replicas 1 \
  --reserve-memory 1gb \
  --limit-memory 1gb \
  --network sherlock-overlay \
  --publish published=${SHERLOCK_METASTORE_PORT},target=9083 \
  --env HIVE_DEFAULT_FS="s3a://${SHERLOCK_BUCKET_NAME}/" \
  --env S3_ACCESS_KEY="${SHERLOCK_S3_ACCESS_KEY}" \
  --env S3_SECRET_KEY="${SHERLOCK_S3_SECRET_KEY}" \
  --env S3_END_POINT="${SHERLOCK_S3_END_POINT}" \
  --env S3_PATH_STYLE_ACCESS="${SHERLOCK_S3_PATH_STYLE_ACCESS}" \
  --env DB_JDBC="jdbc:postgresql://sherlock-postgres:5432/hive?createDatabaseIfNotExist=true" \
  --env DB_PASSWD="hive" \
  --env DB_USER="hive" \
  --env HIVE_METASTORE_URI="thrift://sherlock-metastore:9083" \
  sherlockdatalake/metastore:3_1_1


