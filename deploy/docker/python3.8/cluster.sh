# ./build.sh tensorflow
# should we just use     command: ["push_server", "/opt/pushpy/conf/push.conf.yml"]

#docker run -d -it eismcc/pushpy-start-python3.8:latest /opt/pushpy/monitor.py start
docker run -d -it -p 10000:10000 -p 11000:11000 -p 50000:50000 eismcc/pushpy-start-python3.8:latest push_server /opt/pushpy/push.conf
docker run -d -it -p 10001:10000 -p 11001:11000 -p 50001:50000 eismcc/pushpy-start-python3.8:latest push_server /opt/pushpy/push.conf
docker run -d -it -p 10002:10000 -p 11002:11000 -p 50002:50000 eismcc/pushpy-start-python3.8:latest push_server /opt/pushpy/push.conf
docker run -d -it -p 10003:10000 -p 11003:11000 -p 50003:50000 eismcc/pushpy-start-python3.8:latest push_server /opt/pushpy/push.conf
