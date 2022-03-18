from pushpy.push_manager import PushManager
from pushpy.push_server_utils import host_to_address


class ExamplePushManager(PushManager):

    def __init__(self, *args, host=None, auth_key=None, **kwargs):
        host = host or "localhost:50000"
        auth_key = auth_key or b'password'
        print(f"using: {host} {auth_key}")
        super().__init__(*args, address=host_to_address(host), authkey=auth_key, **kwargs)

