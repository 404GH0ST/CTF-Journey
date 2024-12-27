from PIL import Image

image = Image.open("chall4.png")
pixels = image.load()

flag = ""
i = 0
while True:
    r, g, b = pixels[i * 3, 0]
    g = g ^ b
    flag += chr(r ^ g)
    print(flag)
    i += 1
