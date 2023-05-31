from pwn import *

def start(argv=[], *a, **kw):
    if args.DEBUG:
        return gdb.debug([exe] + argv,gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)
 
