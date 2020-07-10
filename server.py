from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse
import subprocess
import random 
import string

from base64 import b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

app = FastAPI()
router = APIRouter()

key_file = open("./key.private","r")
key = key_file.read()
prefix = key[:5]


print("prefix:", prefix)
AUTH = None

@router.delete("/challenge")
def challenge():
    chall = ''.join(random.choices(string.ascii_uppercase + string.digits, k=23))
    return PlainTextResponse(chall)


@router.post("/{chall}/validate")
async def validate_chall(chall, request: Request):
    global AUTH
    data = await request.form()

    try:
        nonce = b64decode(data['nonce'])
        ciphertext = b64decode(data['ciphertext'])
        cipher = ChaCha20.new(key=key.encode(), nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        print(plaintext.decode() == chall)
        AUTH = chall
    except:
        AUTH = None

@router.patch("/{chall}/exec")
async def exec(chall, request: Request):
    global AUTH
    if AUTH != chall:
        AUTH = None
        raise HTTPException(status_code=69, detail="Go away")
    AUTH = None
    body = await request.body()
    process = subprocess.Popen(
        [body.decode()],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True)
    stdout, stderr = process.communicate()
    return JSONResponse({
        "rc": process.returncode,
        "pid": process.pid,
        "stdout": stdout.decode("utf-8"),
        "stderr": stderr.decode("utf-8")
    })

app.include_router(router, prefix=f"/{prefix}")
