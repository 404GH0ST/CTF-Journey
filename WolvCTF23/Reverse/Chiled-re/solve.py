
data = [    b'\x5e\x1b\x62\x51\x4c\x5e\x49\x5d',    b'\x1f\x58\x19\x41\x1b\x42\x42\x49',    b'\x5e\x75\x19\x4e\x1b\x5f\x6d\x75',    b'\x1e\x6d\x75\x19\x42\x5e\x75\x1a',    b'\x1e\x75\x0b\x0b\x53\x52\x1e\x46',    b'\x57\x18']

ct = b''.join(data)

flag = []

for i, c in enumerate(ct):
    flag.append(chr(c ^ 42))

b = ''.join(flag)

a = []
for i in range(40, 0, -8):
    a.extend(b[i-8:i])

# Because the script only do 40 chars we need add the rest
a = ''.join(a[::-1])
a += b[41] + b[40]
print(a)
