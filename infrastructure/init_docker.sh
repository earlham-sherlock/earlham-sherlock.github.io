#!/usr/bin/env bash


if ! docker ps > /dev/null 2>&1; then
    echo "ERROR! docker daemon can not be reached, please fix docker before starting Sherlock!"
    exit 1
fi

if ! docker node ls > /dev/null 2>&1; then
  echo "WARNING! this node is not in swarm mode, initializing new swarm cluster now"
  docker swarm init
fi


NET_ID=`docker network ls --filter name=sherlock-overlay -q`
if [[ -z "$NET_ID" ]]
then
    echo "sherlock overlay network not exists! creating it now..."
    docker network create --attachable -d overlay sherlock-overlay
fi

