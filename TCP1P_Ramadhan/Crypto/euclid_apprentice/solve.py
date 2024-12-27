import math


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


# Extended euclidean algorithm
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


c_list = open("./output.txt", "r").read().split("\n")[:-1]

c1 = int(c_list[0].split(" = ")[-1])
c2 = int(c_list[1].split(" = ")[-1])
c3 = int(c_list[2].split(" = ")[-1])

m1 = math.isqrt(c1 - 23)
flag_1 = bytes.fromhex(f"{m1:x}").decode()

x = egcd(c1, c2)[1]
y = egcd(c1, c2)[2]
# c3 = m2*x*y
m2 = c3 // (x * y)
flag_2 = bytes.fromhex(f"{m2:x}").decode()

print(flag_1 + flag_2)
