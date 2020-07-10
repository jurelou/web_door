import sys
import httpx
import colored
from colored import stylize
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes


key_file = open("./key.private","r")
key = key_file.read()

base_url = f"http://{sys.argv[1]}:6969/{key[:5]}"

if len(sys.argv) < 2:
    sys.exit(print("Give me a domain name or IP."))

def exec_cmd(cmd):
    with httpx.Client() as client:
        r = client.delete(f'{base_url}/challenge')
        challenge = r.content
        cipher = ChaCha20.new(key=key.encode())
        ciphertext = cipher.encrypt(challenge)
        nonce = b64encode(cipher.nonce).decode('utf-8')
        ct = b64encode(ciphertext).decode('utf-8')
        data = {
            'nonce': nonce,
            'ciphertext': ct
        }
        r = client.post(f'{base_url}/{challenge.decode()}/validate', data=data)
        r = client.patch(f'{base_url}/{challenge.decode()}/exec', data=cmd)
        res = r.json()
        print(res["stdout"])
        print(stylize(res["stderr"], colored.fg("red")))

while 42:
    exec_cmd(input("$"))
