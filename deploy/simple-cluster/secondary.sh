#!/bin/bash
docker-compose -p "push" -f $1/secondary-1.yml ${@:2}
