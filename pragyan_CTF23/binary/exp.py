import string 
import random
def calculate_desc(msg):
    c = 0
    r = 0
    for i in msg:
        r = r + (c + ord(i))
        c += 1
    return r

length = 10
character = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
char2 = 'z'

for i in range(99999):
    random_string = ''.join(random.choice(char2) for i in range(length))
    result = calculate_desc(random_string)
    print(result)
    if result == 1265:
        print(random_string)
        break

# lenght = len(inp)
# print(calculate_desc(inp))
