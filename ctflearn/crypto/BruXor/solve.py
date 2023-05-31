
def xor(val1,val2):
    return bytes(ord(x) ^ val2 for x in val1).decode() 

flag_enc = "q{vpln'bH_varHuebcrqxetrHOXEj"

flag = ""
for i in range(100):
    flag = xor(flag_enc,i)
    if "flag" in flag:
        print(flag)
        break
