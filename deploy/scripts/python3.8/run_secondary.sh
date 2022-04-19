# ./build.sh tensorflow
# should we just use     command: ["push_server", "/opt/pushpy/conf/push.conf.yml"]

#docker run -d -it eismcc/pushpy-start-python3.8:latest /opt/pushpy/monitor.py start
docker run -it --network host -p $((10000+$1)):10000 -p $((11000+$1)):11000 -p $((50000+$1)):50000 eismcc/pushpy-start-python3.8:latest push_server /opt/pushpy/conf/secondary.yml

