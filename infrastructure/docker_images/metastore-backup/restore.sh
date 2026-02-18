#!/usr/bin/env bash

set -euo pipefail

S3_URI="s3://${S3_BUCKET}/${BACKUP_PATH}"

echo "Downloading from S3... ${S3_URI}"

if [[ "${S3_SSL_VALIDATION_DISABLE:-false}" == "true" ]]; then
    S3CMD_ARGS=(--no-check-certificate)
else
    S3CMD_ARGS=()
fi

# Fail fast with a helpful message instead of continuing with missing files.
if ! s3cmd ls "${S3_URI}" "${S3CMD_ARGS[@]}" >/dev/null 2>&1; then
    echo "ERROR: S3 object not found (or not accessible): ${S3_URI}" >&2
    PARENT_PREFIX="$(dirname -- "${BACKUP_PATH}")"
    if [[ -n "${PARENT_PREFIX}" && "${PARENT_PREFIX}" != "." ]]; then
        echo "Tip: listing the parent prefix to find the exact key:" >&2
        s3cmd ls "s3://${S3_BUCKET}/${PARENT_PREFIX}/" "${S3CMD_ARGS[@]}" >&2 || true
    else
        echo "Tip: listing bucket root to find the exact key:" >&2
        s3cmd ls "s3://${S3_BUCKET}/" "${S3CMD_ARGS[@]}" >&2 || true
    fi
    exit 2
fi

DOWNLOAD_PATH=/dump.input
s3cmd get "${S3_URI}" "${DOWNLOAD_PATH}" "${S3CMD_ARGS[@]}"

echo "Restoring dump to DB '${POSTGRES_DB}' on '${POSTGRES_HOST}'..."

export PGPASSWORD="${POSTGRES_PASSWORD}"

# Reset the public schema to avoid conflicts between old/new metastore.
psql -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" --quiet \
  -c "drop schema public cascade; create schema public;" \
  &> /dev/null

# Handle either:
# - gzip-compressed plain SQL (what backup.sh produces)
# - plain SQL
# - pg_dump custom format (e.g., .dump)
if gzip -t "${DOWNLOAD_PATH}" >/dev/null 2>&1; then
    mv "${DOWNLOAD_PATH}" /dump.sql.gz
    gunzip -f /dump.sql.gz
    psql -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" --quiet < /dump.sql \
      &> /dev/null
else
    if pg_restore --list "${DOWNLOAD_PATH}" >/dev/null 2>&1; then
        pg_restore -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" \
          --no-owner --no-privileges "${DOWNLOAD_PATH}" \
          &> /dev/null
    else
        psql -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" --quiet < "${DOWNLOAD_PATH}" \
          &> /dev/null
    fi
fi

echo "Backup successfully restored."