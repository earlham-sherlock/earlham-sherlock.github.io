#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh

SERVICE_NAME="sherlock-yanagishima"

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
  --network sherlock-overlay \
  --publish published=8090,target=8080 \
  --env PRESTO_COORDINATOR_URL="http://sherlock-presto-coordinator:8080" \
  --env CATALOG=sherloch \
  --env SCHEMA=default \
  dkim010/yanagishima
