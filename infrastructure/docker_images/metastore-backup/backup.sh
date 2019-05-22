#!/usr/bin/env bash

set -e

echo "Creating dump of DB '${POSTGRES_DB}' from '${POSTGRES_HOST}'..."

export PGPASSWORD=${POSTGRES_PASSWORD}
pg_dump -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${POSTGRES_EXTRA_OPTS} ${POSTGRES_DB} | gzip > /dump.sql.gz


echo "Uploading to S3... s3://${S3_BUCKET}/${BACKUP_PATH}"
s3cmd put /dump.sql.gz s3://${S3_BUCKET}/${BACKUP_PATH} &> /dev/null

echo "Backup successfully created in S3."