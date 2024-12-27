image = open("./awv.jpg", "rb").read()

image = bytearray(image)

for i, v in enumerate(image):
    image[i] = v ^ 4

fin = open("./flag.jpg", "wb")
fin.write(image)
fin.close()
