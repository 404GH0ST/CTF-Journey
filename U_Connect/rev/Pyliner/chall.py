#!/usr/bin/env python3

from hashlib import md5

flag = 'fake_flag'
cipher = lambda c: ''.join(list(map(lambda i, j: md5(str(j+i).encode()).hexdigest() if i % 2 == 0 else md5(str(j^i).encode()).hexdigest(), range(len(c)), [ord(j) ^ ord(c[i+1]) if i % 2 == 0 else ord(j) ^ 0xbf for i,j in enumerate(c)])))
print(f"uconnect{{{cipher(flag)}}}")
