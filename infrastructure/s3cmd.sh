#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

if [[ -z "${SHERLOCK_CONF:-}" ]]; then
  echo "ERROR: SHERLOCK_CONF environment variable is not set." >&2
  echo "Example: export SHERLOCK_CONF=\"${SCRIPT_DIR}/conf/config-example_sandbox_external-s3.conf\"" >&2
  exit 1
fi

# Load config + computed vars (S3_SSL_ENABLED, S3_REGION, etc.)
source "${SCRIPT_DIR}/prepare_config_variables.sh"
"${SCRIPT_DIR}/init_docker.sh"

IMAGE=${SHERLOCK_METASTORE_BACKUP_IMAGE:-bbazsi41/metastore-backup:9_6}

docker run \
  --rm \
  --network sherlock-overlay \
  --entrypoint bash \
  --volume "${SCRIPT_DIR}/docker_images/metastore-backup/entrypoint.sh:/entrypoint.sh:ro" \
  --volume "${SCRIPT_DIR}/docker_images/metastore-backup/s3cfg_template:/s3cfg_template:ro" \
  --env S3_END_POINT="${SHERLOCK_S3_END_POINT}" \
  --env S3_ACCESS_KEY="${SHERLOCK_S3_ACCESS_KEY}" \
  --env S3_SECRET_KEY="${SHERLOCK_S3_SECRET_KEY}" \
  --env S3_BUCKET="${SHERLOCK_BUCKET_NAME}" \
  --env S3_SSL_ENABLED="${SHERLOCK_S3_SSL_ENABLED}" \
  --env S3_SSL_VALIDATION_DISABLE="${SHERLOCK_S3_SSL_VALIDATION_DISABLE}" \
  --env S3_REGION="${SHERLOCK_S3_REGION:-}" \
  --env S3_PATH_STYLE_ACCESS="${SHERLOCK_S3_PATH_STYLE_ACCESS}" \
  "${IMAGE}" /entrypoint.sh s3cmd "$@"
