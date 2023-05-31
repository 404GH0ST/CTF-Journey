import hashlib

for i in range(999999):
    m = hashlib.md5(str(i).encode()).hexdigest()
    if m.startswith("0e"):
        print(i)
        break
