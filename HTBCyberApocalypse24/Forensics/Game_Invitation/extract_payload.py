def xor_function_dec(given_string, length):
    xor_key = 45
    result = bytearray()
    for i in range(length):
        result.append(given_string[i] ^ xor_key)
        xor_key = ((xor_key ^ 99) ^ (i % 254))
    return bytes(result)

def regexexp(file_content):

    pattern = b'sWcDWp36x5oIe2hJGnRy1iC92AcdQgO8RLioVZWlhCKJXHRSqO450AiqLZyLFeXYilCtorg0p3RdaoPa'
    index = file_content.find(pattern)

    index = index + len(pattern)
    return index

def main():

    file_content = open("./invitation.docm", "rb").read()
    index = regexexp(file_content)

    payload = file_content[index:index + 13082]
    
    payload = xor_function_dec(payload, len(payload))
    print(payload)


if __name__ == "__main__":
    main()
