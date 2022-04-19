#!/bin/bash
export PUSH_NODE_TYPE=bootstrap
docker-compose -p "push" -f $1/secondary-2.yml ${@:2}
