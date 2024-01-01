import sys

# First part
def sum(a, b):
    return int(a) + int(b) + 1

# Second part
# def sum(a, b):
#     return int(a) + int(b)

if __name__ == "__main__":
    numbers = input("")
    num1 = numbers[0]
    num2 = numbers[-1]
    result = sum(num1, num2)
    # Third part
    # print("Result: %s" % result)
    print(result)