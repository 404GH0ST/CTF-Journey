import os,hashlib,base64,binascii
from Crypto.Util.number import *

default_role = b"averageusr"
kunci_rahasia = os.urandom(20)

def verifikasi_digital(kc,data):
	return hashlib.sha1(kc + data).hexdigest().encode()

def validasi(data):
	tes = [b"pw", b"role", b"nama"]
	for i in tes:
		if data.count(i) != 1:
			print("Tidak boleh mengandung kata dan/atau menambahkan atribut komponen secara langsung!")
			exit()


def check(data):
	parse_sign = data.rfind(b'|hashsign=')
	signed_hash = data[parse_sign+10:]
	parsed_data = data[:parse_sign]
	if verifikasi_digital(kunci_rahasia,parsed_data) != signed_hash:
		print("Integritas telah rusak. Tolong input kembali username dan password Anda.")
		return

	role_check = data.rfind(b'|role=')
	role = data[role_check+6:role_check+16].decode()
	if role == "superuserz":
		print("Halo Super User, berikut kami serahkan FLAG untuk anda!")
		try:
			content = open("flag.txt","rb").read()
			print(content)
		except Exception as e:
			print(e)
			print("Hubungi problem-setter karena ada kendala.")
		return
	else:
		print("Halo Normal User, aplikasi sedang dalam maintainance.")
		return

def banner():
	print('''
 _      _   __ _____  _   _           _     _             
| |    | | / //  ___|| | | |         (_)   (_)            
| |    | |/ / \ `--. | | | | ___ _ __ _ ___ _  __ _ _ __  
| |    |    \  `--. \| | | |/ _ \ '__| / __| |/ _` | '_ \ 
| |____| |\  \/\__/ /\ \_/ /  __/ |  | \__ \ | (_| | | | |
\_____/\_| \_/\____/  \___/ \___|_|  |_|___/_|\__, |_| |_|
                                               __/ |      
                                              |___/       
==========================================================

Selamat datang di aplikasi LKSVerisign.
Karena masih beta, aplikasi ini hanya bisa digunakan oleh user biasa untuk login.

Fitur Normal User:
-

Fitur Super User:
- Mendapatkan Flag

		''')

def main():
	banner()
	username = input("Nama kamu > ").encode()
	password = input("Password kamu > ").encode()
	
	wrapper = b"pw="+hashlib.sha512(password).hexdigest().encode()+b"|role="+default_role+b"|nama="+username
	hash_sign = verifikasi_digital(kunci_rahasia,wrapper)
	wrapper += b"|hashsign="+hash_sign
	validasi(wrapper)


	print("Terima kasih, berikut Tiket ID kamu:")
	print(binascii.hexlify(wrapper).decode())
	hexa_ticket = input("\nJangan sampai hilang ya, selanjutnya adalah proses verifikasi Tiket ID, mohon masukkan Tiket ID sebelumnya >> ")
	try:
		check(binascii.unhexlify(hexa_ticket))
	except Exception as e:
		pass

if __name__ == "__main__":
	while True:
		main()