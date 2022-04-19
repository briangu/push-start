#!/bin/bash
export PUSHPY_NODE_TYPE=primary
docker-compose -p "push" -f $1/primary.yml ${@:2}
