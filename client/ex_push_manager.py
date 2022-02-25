from pushpy.push_manager import PushManager
from pushpy.push_server_utils import host_to_address


class ExamplePushManager(PushManager):

    def __init__(self, *args, **kwargs):
        host = "localhost:50000"
        auth_key = b'password'
        super().__init__(*args, address=host_to_address(host), authkey=auth_key, **kwargs)

