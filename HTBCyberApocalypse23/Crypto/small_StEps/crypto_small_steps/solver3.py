# This script is not necessary for the challenge but may be useful in the
# future.
from pwn import *
from Crypto.Util.number import long_to_bytes
import libnum

# This function takes in binary data and converts it to ASCII.
def toAscii(data):
    return data.decode().strip()


# This function sends the string "E" to the server and retrieves the public key
# and encrypted flag that are returned. The public key consists of two parts:
# N and e.
def choiceE():
    r.sendlineafter(b"> ", b"E")
    r.recvuntil(b"N: ")
    N = eval(toAscii(r.recvline()))
    r.recvuntil(b"e: ")
    e = eval(toAscii(r.recvline()))
    r.recvuntil(b"The encrypted flag is: ")
    encrypted_flag = eval(toAscii(r.recvline()))
    return N, e, encrypted_flag

def vuln_check(n, c, e):
    info("Checking if nroot of m is less than or greater than n")
    m = libnum.nroot(c, e)
    if m < n:
        success("It's indeed less than, the decrypt process will be easier")
    else:
        critical("You might need to change to decrypt process because it's greater than")

# This function serves as the main logic of the solver script. It calls
# `choiceE()` to retrieve the public key and encrypted flag and prints them.
def pwn():
    N1, e1, encrypted_flag1 = choiceE()

    print(f"\nCipher 1: {encrypted_flag1}, \nN1={N1}, \ne={e1}")
    vuln_check(N1, encrypted_flag1, e1)

    m = libnum.nroot(encrypted_flag1, e1)

    print(f"\nDecipher: {long_to_bytes(m).decode()}")

# This block handles the command-line flags when running `solver.py`. If the
# `REMOTE` flag is set, the script connects to the remote host specified by the
# `HOST` flag. Otherwise, it starts the server locally using `process()`.
if __name__ == "__main__":
    if args.REMOTE:
        ip, port = args.HOST.split(":")
        r = remote(ip, int(port))
    else:
        r = process(["python3", "server.py"])

    pwn()
