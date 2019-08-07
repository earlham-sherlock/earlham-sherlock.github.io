#!/usr/bin/env bash

set -e

if [[ "$S3_SSL_VALIDATION_DISABLE" == "true" ]]; then
    export S3CMD_ARGS=" --no-check-certificate"
else
    export S3CMD_ARGS=""
fi

echo "Creating dump of DB '${POSTGRES_DB}' from '${POSTGRES_HOST}'..."

export PGPASSWORD=${POSTGRES_PASSWORD}
pg_dump -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${POSTGRES_EXTRA_OPTS} ${POSTGRES_DB} | gzip > /dump.sql.gz


echo "Uploading to S3... s3://${S3_BUCKET}/${BACKUP_PATH}"
s3cmd put /dump.sql.gz s3://${S3_BUCKET}/${BACKUP_PATH} ${S3CMD_ARGS} &> /dev/null

echo "Backup successfully created in S3."