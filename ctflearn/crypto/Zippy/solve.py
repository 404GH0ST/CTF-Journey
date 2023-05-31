# unzip to file ./zippy directory
import binascii
import base64
import string
import itertools
import struct

alph = 'abcdefghijklmnopqrstuvwxyzCTF0123456789_@{}-/!$%=^:;+.,?#&*<>'
#alph = string.ascii_letters + string.digits + "_@{}-/!\"$%=^[]:;+.,?"

crcdict = {}
print("computing all possible CRCs...")
for x in itertools.product(list(alph), repeat=4):
    st = ''.join(x)
    testcrc = binascii.crc32(st)
    crcdict[struct.pack('<i', testcrc)] = st
print("Done!")


flag = ""

for i in range(0, 9):
    f = open("./flag0{}.zip".format(i))
    data = f.read()
    f.close()
    crc = ''.join(data[14:18])
    if crc in crcdict:
        print("Got plain for crc hash flag0{}".format(i))
        flag += crcdict[crc]
    else:
        print("FAILED!")

for i in range(10, 14):
    f = open("./flag{}.zip".format(i))
    data = f.read()
    f.close()
    crc = ''.join(data[14:18])
    if crc in crcdict:
        print("Got plain for crc hash flag{}".format(i))
        flag += crcdict[crc]
    else:
        print("FAILED!")

print("Flag : {}".format(flag))

