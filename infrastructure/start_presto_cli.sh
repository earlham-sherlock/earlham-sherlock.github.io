#!/usr/bin/env bash

set -e

source ./prepare_config_variables.sh
./init_docker.sh


echo -e "\n======="
echo -e "======= starting a local presto-cli"
echo -e "=======\n"


SERVICE_ID=`docker service ls --filter name=sherlock-presto-coordinator -q`
if [[ -z "${SERVICE_ID}" ]]
then
    echo "ERROR! sherlock presto coordinator docker service is not running yet!"
    echo "please start the presto cluster before starting a command line client"
    exit 1
fi

IMAGE=`docker service ps sherlock-presto-coordinator | grep sherlock-presto-coordinator |  awk '{print $3}'`

docker run \
   --rm \
   -it \
   --entrypoint='' \
   --network sherlock-overlay \
   $IMAGE \
   /bin/bash -c "presto-cli --server sherlock-presto-coordinator:8080 --catalog sherlock"
