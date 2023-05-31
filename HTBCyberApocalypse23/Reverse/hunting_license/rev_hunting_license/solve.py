from pwn import *
import time
exe = './license'
elf = context.binary = ELF(exe, checksec=False)
io = remote('138.68.158.112',32418)

check1 = "PasswordNumeroUno"

check2_cands = [0x30,0x77,0x54,0x64,0x72,0x30,0x77,0x73,0x73,0x34,0x50]

check2_list = [chr(c) for c in check2_cands]
check2 = ''.join(check2_list[::-1])

check3_cands = [0x47,0x7b,0x7a,0x61,0x77,0x52,0x7d,0x77,0x55,0x7a,0x7d,0x72,0x7f,0x32,0x32,0x32,0x13]

check3 = ''.join(chr(c ^ 0x13) for c in check3_cands)

io.sendline(b'elf')
time.sleep(1)
io.sendline(b'amd64')
time.sleep(1)
io.sendline(b'readline')
time.sleep(1)
io.sendline(b'0x401172')
time.sleep(1)
io.sendline(b'5')
time.sleep(1)
io.sendline(check1)
time.sleep(1)
io.sendline(check2[::-1])
time.sleep(1)
io.sendline(check2)
time.sleep(1)
io.sendline(b'0x13')
time.sleep(1)
io.sendline(b'ThirdAndFinal!!!')
time.sleep(1)
io.interactive()
