
python3 c_manage_hosts.py localhost:50000 add 127.0.0.1:10001
python3 c_manage_hosts.py localhost:50000 add 127.0.0.1:10002
python3 c_manage_hosts.py localhost:50000 add 127.0.0.1:10003
python3 c_manage_hosts.py localhost:50001 add 127.0.0.1:10000

echo 50000
python3 c_manage_hosts.py localhost:50000 status | grep partner_node_status

echo 50001
python3 c_manage_hosts.py localhost:50001 status | grep partner_node_status
