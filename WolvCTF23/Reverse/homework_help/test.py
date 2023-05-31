from z3 import *

x = BitVec('x', 8)
y = BitVec('y', 8)

solve(119^y==99,show=True)
solve(99^y==116,show=True)
solve(116^y==102,show=True)
solve(102^y==123,show=True)
# solve(x^y==119, show=True)
# if s.check() == sat:
#         m = s.model()
#         print(m)
