from Crypto.Util.number import long_to_bytes
def cube_root(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**3 <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo
# Actual values of N and ciphertext
N = 5902009463207829412078094281372588437782103889489896121745951837357070722362125387685839915481298323911442853230211143537203557457039436285154499842549413
ciphertext = 70407336677212734512904417790364996209303505181058921964048492612496322624631305529219622545852704619786282073843859755376774478843366150337125
# Calculate cube root and convert to plaintext
plaintext = long_to_bytes(cube_root(ciphertext)).decode('utf-8')
print(plaintext)
