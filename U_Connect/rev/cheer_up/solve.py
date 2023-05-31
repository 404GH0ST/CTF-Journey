import string
flag_enc = open('./real_encrypted.txt', 'rb').read()
# if flag_enc[-1] == :
#     print("True")
print(flag_enc.find(124))
flag = ''
know_flag = 'uconnect{}'
key = ''
flag = ''
counter = 0
for i in range(0, len(know_flag)-1):
    key += chr(ord(know_flag[i]) ^ flag_enc[i])
    
print(f"Got key? : {key}")
key += chr(ord('}') ^ flag_enc[-1])
print(f"Tuning the key : {key}")

for c in flag_enc:
    key_len = len(key)
    flag += chr(c ^ ord(key[counter % key_len]))
    counter += 1

print(f"Flag : {flag}")
# print(f"Dapat key? : {key}")

# # Tuning the key
# key += 'a'
# i_len = len(key)
# flag += chr(enc_flag[counter] ^ ord(key[counter % i_len]))
# counter += 1
# print(f"Tuning key : {key}")

# # Decrypting
# for c in enc_flag[len(flag):]:
#     i_len = len(key)
#     flag += chr(c ^ ord(key[counter % i_len]))
#     counter += 1

# print(f"Flag: {flag}")