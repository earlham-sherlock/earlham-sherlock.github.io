#!/usr/bin/env bash

docker service scale sherlock-presto-workers=0
docker service scale sherlock-presto-coordinator=0
docker service scale sherlock-metastore=0
docker service scale sherlock-postgres=0
docker service scale sherlock-local-s3=0

docker service rm sherlock-presto-workers
docker service rm sherlock-presto-coordinator
docker service rm sherlock-metastore
docker service rm sherlock-postgres
docker service rm sherlock-local-s3


# TODO: remove all services and waits until all containers exited