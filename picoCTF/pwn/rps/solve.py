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


def play():
    io.sendline(b"1")
    io.sendline(b"rockpaperscissors")


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

context.log_level = "info"
# context.terminal = "kitty"

io = start()

play()
play()
play()
play()
play()

io.interactive()
