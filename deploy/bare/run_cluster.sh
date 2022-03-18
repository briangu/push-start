#/bin/bash

./run_server.sh $PUSH_START_HOME/deploy/bare/conf/push.conf.1.yml > /tmp/push.10000.txt 2> /tmp/push.10000.err &
./run_server.sh $PUSH_START_HOME/deploy/bare/conf/push.conf.2.yml > /tmp/push.10001.txt 2> /tmp/push.10001.err &
./run_server.sh $PUSH_START_HOME/deploy/bare/conf/push.conf.3.yml > /tmp/push.10002.txt 2> /tmp/push.10002.err &

push_repl 50000

pkill -f push_server
