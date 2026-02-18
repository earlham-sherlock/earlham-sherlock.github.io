#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

echo -e "\n======="
echo -e "======= restoring metastore from S3"
echo -e "=======\n"


SERVICE_ID=`docker service ls --filter name=sherlock-postgres -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock postgres docker service is not running yet!"
    echo "please start postgres before restoring a backup"
    exit 1
fi

if [[ "$#" -ne 1 ]]; then
    echo "ERROR! please provide name for the metastore backup file!"
    echo ""
    echo "Usage: metastore_restore.sh <name of the backup file>"
    echo ""
    exit 1
fi

source "${SCRIPT_DIR}/prepare_config_variables.sh"
"${SCRIPT_DIR}/init_docker.sh"


docker run \
  --rm  \
  --network sherlock-overlay \
  --entrypoint bash \
  --volume "${SCRIPT_DIR}/docker_images/metastore-backup/entrypoint.sh:/entrypoint.sh:ro" \
  --volume "${SCRIPT_DIR}/docker_images/metastore-backup/s3cfg_template:/s3cfg_template:ro" \
    --volume "${SCRIPT_DIR}/docker_images/metastore-backup/restore.sh:/restore.sh:ro" \
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
  --env S3_SSL_VALIDATION_DISABLE="${SHERLOCK_S3_SSL_VALIDATION_DISABLE}" \
  --env S3_REGION="${SHERLOCK_S3_REGION:-}" \
  --env S3_PATH_STYLE_ACCESS="${SHERLOCK_S3_PATH_STYLE_ACCESS}" \
  --env BACKUP_PATH="${1}" \
  sherlockdatalake/metastore-backup:9_6 /entrypoint.sh bash /restore.sh