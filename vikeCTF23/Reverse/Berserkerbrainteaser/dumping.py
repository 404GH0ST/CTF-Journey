import re

pattern = r"^(v(i(k(e(C(T(F?)?)?)?)?)?)?)?$"

text = input("Enter a string: ")

if re.match(pattern, text):
    print("Passed")
else:
    print("Failed")