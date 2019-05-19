#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh


SERVICE_NAME="sherlock-postgres"

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



docker service create  \
  --with-registry-auth  \
  --name ${SERVICE_NAME}  \
  --container-label ${SERVICE_NAME}  \
  --replicas 1 \
  --reserve-memory 512mb \
  --limit-memory 512mb \
  --network sherlock-overlay \
  --publish published=${SHERLOCK_POSTGRES_PORT},target=5432 \
  --env POSTGRES_USER=hive \
  --env POSTGRES_PASSWORD=hive \
  --env POSTGRES_DB=hive \
  --health-cmd "pg_isready -U hive" \
  --health-interval 5s \
  --health-timeout 5s \
  --health-retries 5 \
  --health-start-period 30s \
  postgres:9.6.10