import requests

target = "http://178.62.9.10:31734/flag"

request = requests.get(target)

while "HTB" not in request.text:
    request = requests.get(target)
    print(request.text)

print(request.text)
