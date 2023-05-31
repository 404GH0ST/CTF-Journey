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


# This function serves as the main logic of the solver script. It calls
# `choiceE()` to retrieve the public key and encrypted flag and prints them.
def pwn():
    N1, e1, encrypted_flag1 = choiceE()
    N2, e2, encrypted_flag2 = choiceE()
    N3, e3, encrypted_flag3 = choiceE()
    
    e = 3
    mod=[N1,N2,N3]
    rem=[encrypted_flag1,encrypted_flag2,encrypted_flag3]

    res=libnum.solve_crt(rem,mod)
    print("\n\nAnswer:")
    print(f"\nCipher 1: {encrypted_flag1}, N1={N1}")
    print(f"Cipher 2: {encrypted_flag2}, N2={N2}")
    print(f"Cipher 3: {encrypted_flag3}, N3={N3}")
    print(f"\nWe can solve M^e with CRT to get {res}")

    val=libnum.nroot(res, e)
    print(f"\nIf we assume e: {e}, we take the third root to get: {val}")
    print("Next we convert this integer to bytes, and display as a string.")
    print(f"\nDecipher: {long_to_bytes(val).decode()}")




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
