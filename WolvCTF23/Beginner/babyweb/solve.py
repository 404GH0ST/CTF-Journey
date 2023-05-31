import requests

target = "https://charlotte-tlejfksioa-ul.a.run.app//super-secret-route-nobody-will-guess"

request = requests.put(target)

print(request.text)
