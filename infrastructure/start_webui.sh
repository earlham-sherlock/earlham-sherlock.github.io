#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh

SERVICE_NAME="sherlock-webui"

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


SERVICE_ID=`docker service ls --filter name=sherlock-presto-coordinator -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock presto coordinator docker service is not running yet!"
    echo "please start the presto coordinator before starting the presto workers"
    exit 1
fi


docker service create  \
  --with-registry-auth  \
  --name ${SERVICE_NAME}  \
  --container-label ${SERVICE_NAME}  \
  --reserve-memory ${SHERLOCK_WEBUI_MEMORY_RESERVATION} \
  --limit-memory ${SHERLOCK_WEBUI_MEMORY_LIMIT} \
  --reserve-cpu ${SHERLOCK_WEBUI_CPU_CORES} \
  --limit-cpu ${SHERLOCK_WEBUI_CPU_CORES} \
  --network sherlock-overlay \
  --publish published=${SHERLOCK_PRESTO_PORT},target=8080 \
  --env WEBUI_YANAGISHIMA_PORT="8080" \
  --env WEBUI_YANAGISHIMA_MAX_QUERY_TIME="1800" \
  --env WEBUI_YANAGISHIMA_MAX_FILE_SIZE="1073741824" \
  --env WEBUI_PRESTO_DATASOURCE_NAME="sherlock" \
  --env WEBUI_PRESTO_COORDINATOR_URL="http://sherlock-presto-coordinator:8080" \
  --env WEBUI_PRESTO_WEBUI_URL="http://sherlock-presto-coordinator:8080" \
  --env WEBUI_PRESTO_CATALOGUE="sherlock" \
  --env WEBUI_PRESTO_SCHEMA="default" \
  sherlockdatalake/webui:21.0
