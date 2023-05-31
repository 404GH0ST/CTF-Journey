

flag_enc = int(open("result.txt",'r').read())
flag = list(map(lambda x,y: x ^ (x >> 2 ** y), [flag_enc], [0]))[0]
print(flag.to_bytes(flag.bit_length()+7 // 8).decode())