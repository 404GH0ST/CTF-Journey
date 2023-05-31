from pwn import *
from math import floor

io = remote("178.128.101.5", 64896)

nums = [i for i in range(100)]
low = 0
high = len(nums) - 1
point = 0
while True:
    if point == 100:
        io.interactive()
    middle = floor((low+high) // 2)
    io.sendlineafter(b"mana?", str(nums[middle]))
    response = io.recvline().strip()
    if response == b"apah?":
        low = middle + 1
    elif response == b"huh?":
        high = middle - 1
    else:
        print(f"Got the {nums[middle]}")
        print(f"Success with point: {point}")
        low = 0
        high = len(nums) - 1
        point+=1

