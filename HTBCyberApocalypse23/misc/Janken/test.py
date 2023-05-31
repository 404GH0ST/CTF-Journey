from pwn import *
from ctypes import CDLL
from math import floor
import time

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''
init-pwndbg
continue
'''.format(**locals())

exe = './janken'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
libc = CDLL('./.glibc/libc.so.6')


choices = ['rock', 'paper', 'scissors']


io = start()
io.sendlineafter(b'>>', b'1')

for i in range(99):
    # sleep(1)
    now = libc.srand(floor(int(time.time())))
    choice = libc.rand() % 3
    comp = choices[choice]
    if comp == 'rock':
        player = 'paper'
    elif comp == 'paper':
        player = 'scissors'
    elif comp == 'scissors':
        player = 'rock'

    io.recvuntil(b'>>')
    io.sendline(player.encode())

io.interactive()