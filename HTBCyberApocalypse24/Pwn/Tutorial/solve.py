from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def send_answer(answer: str):
    io.sendlineafter(b">> ", answer.encode())

gdbscript='''
init-pwndbg
continue
'''.format(**locals())

exe = './test'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context.terminal = 'kitty'

io = start()

send_answer("y")
send_answer("2147483647")
send_answer("-2147483648")
send_answer("-2")
send_answer("integer overflow")
send_answer("-2147483648")
send_answer("1337")

io.interactive()
