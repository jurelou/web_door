# Simple WEB backdoor.

Includes a stupid implementation of a challenge response ( based on ChaCha20 )

# Generate a 32 bit key

```bash
./gen_secret.sh
```


# Server

```bash
pip install -r requirements.txt

gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker server:app -b 0.0.0.0:6969 --daemon
```

# client

```bash
pip install -r requirements.txt

./client <server IP>
```
