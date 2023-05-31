#!/usr/bin/python3 -u

import random
import os

max_retries = 100
for _ in range(max_retries):
    print("Hints:")
    for i in range(9):
        print(random.getrandbits(32))

    real = random.getrandbits(32)
    print("Guess:")
    resp = input()
    if int(resp) == real:
        print("FLAG", os.getenv("FLAG"))

print("No tries left, sorry!")
