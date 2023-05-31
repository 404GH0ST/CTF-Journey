
flag = 'uconnect{fake_flag}'
key = 'fake'
a = lambda n : 35 - (int(n,36) % 36)
b = lambda n, nn: hex(sum(list(map(lambda i: (((n >> i & 1) + (nn >> i & 1)) % 2) << i,range(8)))))[2:].rjust(2,'0')
c = lambda n, nn : [b(nn[i%len(nn)],j) for i,j in enumerate(n)]
d = [a(n) for n in flag.replace("{", "xx").replace('_','yy').replace('}','zz')]
e = [a(n) for n in key]

with open('cipher_test','wb') as f:
    print(d)
    print(e)
    print(int(''.join(str(n) for n in c(d,e)),16))
    f.write(int(''.join(str(n) for n in c(d,e)),16).to_bytes(len(d),'little'))
    f.close()
