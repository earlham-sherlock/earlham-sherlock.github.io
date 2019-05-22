#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh

SERVICE_NAME="sherlock-presto-coordinator"

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


SERVICE_ID=`docker service ls --filter name=sherlock-metastore -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock metastore docker service is not running yet!"
    echo "please start the metastore before starting the presto coordinator"
    exit 1
fi


docker service create  \
  --with-registry-auth  \
  --name ${SERVICE_NAME}  \
  --container-label ${SERVICE_NAME}  \
  --replicas 1 \
  --reserve-memory ${SHERLOCK_PRESTO_MEMORY_RESERVATION} \
  --limit-memory ${SHERLOCK_PRESTO_MEMORY_LIMIT} \
  --reserve-cpu ${SHERLOCK_PRESTO_CPU_CORES} \
  --limit-cpu ${SHERLOCK_PRESTO_CPU_CORES} \
  --network sherlock-overlay \
  --publish published=${SHERLOCK_PRESTO_PORT},target=8080 \
  --env IS_COORDINATOR="true" \
  --env DISCOVERY_CONFIG="discovery-server.enabled=true" \
  --env DISCOVERY_URI="http://sherlock-presto-coordinator:8080" \
  --env METASTORE_URI="thrift://sherlock-metastore:9083" \
  --env S3_ACCESS_KEY="${SHERLOCK_S3_ACCESS_KEY}" \
  --env S3_SECRET_KEY="${SHERLOCK_S3_SECRET_KEY}" \
  --env S3_END_POINT="${SHERLOCK_S3_END_POINT}" \
  --env S3_SSL_ENABLED="${SHERLOCK_S3_SSL_ENABLED}" \
  --env S3_PATH_STYLE_ACCESS="${SHERLOCK_S3_PATH_STYLE_ACCESS}" \
  --env QUERY_MAX_MEMORY="${SHERLOCK_QUERY_MAX_MEMORY}" \
  --env QUERY_MAX_MEMORY_PER_NODE="${SHERLOCK_QUERY_MAX_MEMORY_PER_NODE}" \
  --env QUERY_MAX_TOTAL_MEMORY="${SHERLOCK_QUERY_MAX_TOTAL_MEMORY}" \
  --env QUERY_MAX_TOTAL_MEMORY_PER_NODE="${SHERLOCK_QUERY_MAX_TOTAL_MEMORY_PER_NODE}" \
  --env MEMORY_HEAP_HEADROOM_PER_NODE="${SHERLOCK_MEMORY_HEAP_HEADROOM_PER_NODE}" \
  --env MAX_WORKER_THREADS="${SHERLOCK_MAX_WORKER_THREADS}" \
  --env JVM_XMX="${SHERLOCK_PRESTO_PROCESS_XMX}" \
  sherlockdatalake/presto:0_219a

