def to_identity_map(a):
    return ord(a) - 0x41

def from_identity_map(a):
    return chr(a % 26 + 0x41)

def decrypt(m):
    c = ''
    for i in range(len(m)):
        ch = m[i]
        if not ch.isalpha():
            ech = ch
        else:
            chi = to_identity_map(ch)
            ech = from_identity_map(chi - i)
        c += ech
    return c

with open('output.txt', 'r') as f:
    f.readline()
    flag_enc = f.readline()
    print(decrypt(flag_enc))
    
