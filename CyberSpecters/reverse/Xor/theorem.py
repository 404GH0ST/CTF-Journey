from z3 import *

char_1 = BitVec("char_1", 16)
char_2 = BitVec("char_2", 16)
char_3 = BitVec("char_3", 16)
char_4 = BitVec("char_4", 16)
char_5 = BitVec("char_5", 16)
char_6 = BitVec("char_6", 16)
char_7 = BitVec("char_7", 16)
char_8 = BitVec("char_8", 16)
char_9 = BitVec("char_9", 16)

s = Solver()

flag_enc = [0x5D, 0x32, 0x70, 0x3D, 0x34, 0x6D, 0x6D]

s.add(char_1 ^ 0x5D ^ char_2 == 0x53)
s.add(char_2 ^ 0x32 ^ char_3 == 0x50)
s.add(char_3 ^ 0x70 ^ char_4 == 0x45)
s.add(char_4 ^ 0x3D ^ char_5 == 0x43)
s.add(char_5 ^ 0x34 ^ char_6 == 0x54)
s.add(char_6 ^ 0x6D ^ char_7 == 0x45)
s.add(char_7 ^ 0x6D ^ char_8 == 0x52)
# s.add(char_8 ^ 0x31 ^ char_9 )

print(s.check())
print(s.model())
m = s.model()
key_tuple = sorted([(d, m[d]) for d in m], key=lambda x: str(x[0]))
key = []
for x, v in key_tuple:
    key.append(v)

print(key)

for i in range(0, len(flag_enc)):
    print(chr(flag_enc[i] ^ key[i] ^ key[i + 1]))
