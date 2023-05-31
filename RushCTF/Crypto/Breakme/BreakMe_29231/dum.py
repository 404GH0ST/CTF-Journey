from Crypto.Util.number import *
from Crypto.PublicKey import RSA

# Load the public key and ciphertext from files
with open("key.pem", "rb") as f:
    key = RSA.importKey(f.read())

with open("ciphertext.txt", "r") as f:
    ciphertext = bytes.fromhex(f.read().strip())

# Extract the modulus and public exponent from the public key
N = key.n
e = key.e

# Factorize N into its prime factors p and q
p = 0
q = 0
phi = (p-1)*(q-1) # Compute the totient of N

# Use Pollard's p-1 algorithm to find a factor of N
B = 1000000  # set bound to 1 million
a = 2  # set integer a
while p == 0 or q == 0:
    a = pow(a, 2, N)
    p_prime = gcd(a-1, N)
    if p_prime != 1 and p_prime != N:
        q_prime = N // p_prime
        p = p_prime
        q = q_prime

# Compute the private key exponent d
d = inverse(e, (p-1)*(q-1))

# Decrypt the ciphertext using the private key exponent d
plaintext = pow(bytes_to_long(ciphertext), d, N)

# Convert the plaintext back to bytes and print the flag
flag = long_to_bytes(plaintext)
print(flag)

