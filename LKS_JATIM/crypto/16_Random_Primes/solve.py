from  Crypto.Util.number  import  *

e =  65537

with  open ( 'output.txt' ,  'r' )  as  f:
    n =  int(f.readline()[4:].rstrip())
    c =  int(f.readline()[4:].rstrip())

primes = [4076280259,3468273229,4264770803,2968229111,3010828267,2963163041,3368813909,3760110227,2520734081,3671092039,4012932073,3256290119,3170708137,3679173373,4135959361,3356156009]
phi =  1
for  p  in  primes:
    phi *= p -  1

d = inverse(e, phi)
m =  pow (c, d, n)
flag = long_to_bytes(m)
print(flag)

