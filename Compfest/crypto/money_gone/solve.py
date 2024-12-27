import string
import hashlib

sha512_charset = {}

methods = [
    "md5",
    "sha256",
    "sha3_256",
    "sha3_512",
    "sha3_384",
    "sha1",
    "sha384",
    "sha3_224",
    "sha512",
    "sha224",
]


for char in string.printable:
    x = (ord(char) + 20) % 130
    hash = hashlib.sha512(str(x).encode()).hexdigest()
    sha512_charset[char] = hash

hashes = {}
for method in methods:
    current_hashes = []
    for y in sha512_charset.values():
        hash_obj = hashlib.new(method)
        hash_obj.update(y.encode())
        current_hashes.append(hash_obj.hexdigest())
    hashes[method] = current_hashes

with open("./encrypted_memory.txt", "r") as f:
    encrypted_memory = eval(f.read())

flag = ""

for i in encrypted_memory:
    for method in methods:
        if i in hashes[method]:
            flag += string.printable[hashes[method].index(i)]
            break

print(flag)
