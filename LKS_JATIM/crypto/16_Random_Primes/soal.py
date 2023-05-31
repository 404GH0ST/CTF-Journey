from Crypto.Util.number import *
import math

FLAG = b"ini_flag_palsu_ya_teman-teman"
def mendapatkan_bilangan_prima():
	prima = []
	for i in range(16):
		prima.append(getPrime(32))
	return prima

semua_prima = mendapatkan_bilangan_prima()
n = math.prod(semua_prima)
BFLAG = bytes_to_long(FLAG)
e = 65537
ct = pow(BFLAG,e,n)

print("n = "+str(n))
print("ct = "+str(ct))