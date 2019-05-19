#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh

SERVICE_NAME="sherlock-local-s3"

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

# initialize local S3 bucket
DATA_LAKE_ABS_PATH="$(cd "$(dirname "${SHERLOCK_LOCAL_S3_PATH}")"; pwd -P)/$(basename "${SHERLOCK_LOCAL_S3_PATH}")"
BUCKET_PATH="${DATA_LAKE_ABS_PATH}/${SHERLOCK_BUCKET_NAME}"
mkdir -p ${BUCKET_PATH%/}

docker service create  \
  --with-registry-auth  \
  --name ${SERVICE_NAME}  \
  --container-label ${SERVICE_NAME}  \
  --replicas 1 \
  --reserve-memory 512mb \
  --limit-memory 512mb \
  --network sherlock-overlay \
  --publish published=${SHERLOCK_LOCAL_S3_PORT},target=9000 \
  --env MINIO_ACCESS_KEY="${SHERLOCK_S3_ACCESS_KEY}" \
  --env MINIO_SECRET_KEY="${SHERLOCK_S3_SECRET_KEY}" \
  --mount type=bind,source=${DATA_LAKE_ABS_PATH},destination=/data \
  minio/minio:RELEASE.2019-05-14T23-57-45Z server /data


