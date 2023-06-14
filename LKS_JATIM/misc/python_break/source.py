import os

try:
	while True:
		try:
			print("-----------   CAN YOU BREAK ~|~~|~|~(> 3 <) FROM HERE?   -------------")
			usr_inp = input("> ")
			if '?' in usr_inp or '.' in usr_inp or '/' in usr_inp or '\\' in usr_inp or '*' in usr_inp or '"' in usr_inp or '\'' in usr_inp or '`' in usr_inp or ' ' in usr_inp:
				print("Bahaya, tidak boleh!")
			else:
				ll = [inp.isalpha() for inp in usr_inp]
				if sum(ll) > 0:
					print("Banned!")
					#exit(-1337)
				else:
					try:
						os.system(usr_inp)
					except Exception as e:
						print("Wah untung masih ketahuan satpam. Kamu tetap di banned!")
						#exit(-1)
		except Exception as e:
			print("Ada sesuatu yang salah!")
			exit(-1)
except Exception as e:
	print("No info.")
	pass
