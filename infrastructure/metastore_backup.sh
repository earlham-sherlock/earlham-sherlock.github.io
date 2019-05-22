#!/usr/bin/env bash

set -e

echo -e "\n======="
echo -e "======= backup metastore state to S3"
echo -e "=======\n"


SERVICE_ID=`docker service ls --filter name=sherlock-postgres -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock postgres docker service is not running yet!"
    echo "please start postgres before creating a backup"
    exit 1
fi

if [[ "$#" -ne 1 ]]; then
    echo "ERROR! please provide name for the metastore backup file!"
    echo ""
    echo "Usage: metastore_bakcup.sh <name of the backup file>"
    echo ""
    exit 1
fi

source ./prepare_config_variables.sh
./init_docker.sh

docker run \
  --rm  \
  --network sherlock-overlay \
  --env POSTGRES_HOST="sherlock-postgres" \
  --env POSTGRES_PORT=5432 \
  --env POSTGRES_USER=hive \
  --env POSTGRES_PASSWORD=hive \
  --env POSTGRES_DB=hive \
  --env S3_END_POINT="${SHERLOCK_S3_END_POINT}" \
  --env S3_ACCESS_KEY="${SHERLOCK_S3_ACCESS_KEY}" \
  --env S3_SECRET_KEY="${SHERLOCK_S3_SECRET_KEY}" \
  --env S3_BUCKET="${SHERLOCK_BUCKET_NAME}" \
  --env S3_SSL_ENABLED="${SHERLOCK_S3_SSL_ENABLED}" \
  --env BACKUP_PATH="${1}" \
  sherlockdatalake/metastore-backup:9_6 /backup.sh


