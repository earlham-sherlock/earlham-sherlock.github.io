#!/usr/bin/env bash

if [[ -z "$SHERLOCK_CONF" ]]; then
    echo "ERROR: SHERLOCK_CONF environment variable is not set! Please specify a sherlock config to use!"
    exit 1
fi

if [[ ! -f "$SHERLOCK_CONF" ]]; then
    echo "Config file set in SHERLOCK_CONF environment variable is not found! (SHERLOCK_CONF=\"${SHERLOCK_CONF}\")"
    exit 1
fi

. "$SHERLOCK_CONF"



assert_config () {
  if [[ -z "${!1}" ]]; then
    echo "ERROR: ${!1} config parameter is not set! Please specify it in the sherlock config you use!"
    echo "your current sherlock config is: ${SHERLOCK_CONF}"
    exit 1
  fi
}

assert_config SHERLOCK_USE_LOCAL_S3
assert_config SHERLOCK_BUCKET_NAME
assert_config SHERLOCK_S3_ACCESS_KEY
assert_config SHERLOCK_S3_SECRET_KEY
assert_config SHERLOCK_NUMBER_OF_WORKERS
assert_config SHERLOCK_PRESTO_CPU_CORES
assert_config SHERLOCK_MAX_PRESTO_PROCESS_MEMORY_GB
assert_config SHERLOCK_PRESTO_PORT
assert_config SHERLOCK_METASTORE_PORT
assert_config SHERLOCK_POSTGRES_PORT


# ======= S3 settings (setting local minio S3 settings if needed) =======

shopt -s nocasematch
if [[ "$SHERLOCK_USE_LOCAL_S3" == "true" ]]; then
    export SHERLOCK_S3_END_POINT="http://sherlock-local-s3:9000"
    assert_config SHERLOCK_LOCAL_S3_PATH
    assert_config SHERLOCK_LOCAL_S3_PORT
else
    assert_config SHERLOCK_S3_END_POINT

fi

if [[ "$SHERLOCK_S3_END_POINT" == "http://"* ]]; then
    export SHERLOCK_S3_SSL_ENABLED=false
else
    export SHERLOCK_S3_SSL_ENABLED=true
fi

export SHERLOCK_S3_PATH_STYLE_ACCESS=true

# ======= calculate presto memory settings =======

# the following memory settings are calculated based on SHERLOCK_MAX_PRESTO_PROCESS_MEMORY_GB
#
# before you would fine-tune these settings, check:
# https://prestodb.github.io/docs/current/admin/properties.html#memory-management-properties


PRESTO_PROCESS_MEMORY_MB=`echo "$SHERLOCK_MAX_PRESTO_PROCESS_MEMORY_GB * 1024" | bc`
PRESTO_PROCESS_MEMORY_UPPER_LIMIT_MB=`echo "$PRESTO_PROCESS_MEMORY_MB * 1.1" | bc`

HEAP_HEADROOM_PER_NODE=`echo "$PRESTO_PROCESS_MEMORY_MB * 0.2" | bc`
MAX_QUERY_TOTAL_MEMORY_PER_NODE=`echo "$PRESTO_PROCESS_MEMORY_MB * 0.7" | bc`
MAX_QUERY_TOTAL_MEMORY=`echo "$MAX_QUERY_TOTAL_MEMORY_PER_NODE * $SHERLOCK_NUMBER_OF_WORKERS" | bc`
MAX_QUERY_MEMORY_PER_NODE=`echo "$MAX_QUERY_TOTAL_MEMORY_PER_NODE * 0.8" | bc`
MAX_QUERY_MEMORY=`echo "$MAX_QUERY_MEMORY_PER_NODE * $SHERLOCK_NUMBER_OF_WORKERS" | bc`

export SHERLOCK_QUERY_MAX_MEMORY=$( printf "%.0fMB" $MAX_QUERY_MEMORY )
export SHERLOCK_QUERY_MAX_MEMORY_PER_NODE=$( printf "%.0fMB" $MAX_QUERY_MEMORY_PER_NODE )
export SHERLOCK_QUERY_MAX_TOTAL_MEMORY=$( printf "%.0fMB" $MAX_QUERY_TOTAL_MEMORY )
export SHERLOCK_QUERY_MAX_TOTAL_MEMORY_PER_NODE=$( printf "%.0fMB" $MAX_QUERY_TOTAL_MEMORY_PER_NODE )
export SHERLOCK_MEMORY_HEAP_HEADROOM_PER_NODE=$( printf "%.0fMB" $HEAP_HEADROOM_PER_NODE )

export SHERLOCK_PRESTO_PROCESS_XMX=$( printf " -Xmx%dG" $SHERLOCK_MAX_PRESTO_PROCESS_MEMORY_GB )

export SHERLOCK_PRESTO_MEMORY_RESERVATION=$( printf "%.0fM" $PRESTO_PROCESS_MEMORY_MB )
export SHERLOCK_PRESTO_MEMORY_LIMIT=$( printf "%.0fM" $PRESTO_PROCESS_MEMORY_UPPER_LIMIT_MB )

