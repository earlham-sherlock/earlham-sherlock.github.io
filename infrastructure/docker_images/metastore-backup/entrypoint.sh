#!/usr/bin/env bash


# removing the optional 's3a://', 's3://', BUCKET_NAME, or '/' from the beginning of the BACKUP NAME
BACKUP_PATH=${BACKUP_PATH#"s3a://"}
BACKUP_PATH=${BACKUP_PATH#"s3://"}
BACKUP_PATH=${BACKUP_PATH#"${S3_BUCKET}/"}
BACKUP_PATH=${BACKUP_PATH#"/"}

# remove protocol prefix from endpoint url
S3_END_POINT=${S3_END_POINT#"http://"}
S3_END_POINT=${S3_END_POINT#"https://"}

echo "generating ~/.s3cfg"
envsubst < /s3cfg_template > ~/.s3cfg


$@