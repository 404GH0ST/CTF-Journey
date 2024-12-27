from z3 import *

a = BitVec("a", 32)
b = BitVec("b", 32)
c = BitVec("c", 32)
d = BitVec("d", 32)

s = Solver()

s.add(a ^ 0xAD == 0x74)
s.add(b ^ 0x9D == 0x65)
s.add(c ^ 0x5B == 0x73)
s.add(d ^ 0x57 == 0x74)

s.check()
print(s.model())
