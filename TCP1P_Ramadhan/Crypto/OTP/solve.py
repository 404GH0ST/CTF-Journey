from pwn import xor

data = open("./pesan.txt", "r").read().strip().split("\n")

key = xor(
    b"dengan menyelesaikan tantangan keamanan dalam tim atau individu",
    bytes.fromhex(data[1]),
)[:32]


for enc in data:
    print(xor(bytes.fromhex(enc), key).decode())
