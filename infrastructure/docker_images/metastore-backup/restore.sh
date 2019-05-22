#!/usr/bin/env bash

echo "Downloading from S3... s3://${S3_BUCKET}/${BACKUP_PATH}"

s3cmd get s3://${S3_BUCKET}/${BACKUP_PATH} /dump.sql.gz
gunzip /dump.sql.gz


echo "Restoring dump to DB '${POSTGRES_DB}' on '${POSTGRES_HOST}'..."

export PGPASSWORD=${POSTGRES_PASSWORD}
psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB} --quiet -c "drop schema public cascade; create schema public;" &> /dev/null
psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB} --quiet  < dump.sql &> /dev/null

echo "Backup successfully restored."