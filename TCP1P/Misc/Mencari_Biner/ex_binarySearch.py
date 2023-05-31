from math import floor
import random

nums = [i for i in range(1000)]
target = random.choice([i for i in range(1000)])

low = 0
high = len(nums) - 1
while True:
    middle = floor((low+high) // 2)
    if target > nums[middle]:
        print(f"Current middle: {middle}")
        low = middle + 1
    elif target < nums[middle]:
        print(f"Current middle: {middle}")
        high = middle - 1
    else:
        print(f"Found {nums[middle]} at element: {middle}")
        break
    


