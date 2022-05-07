import hashlib
import random
import secrets

OTPNUM = 50
ALGORITHM = "sha1"

key = secrets.token_bytes(2048)
key = str(random.getrandbits(2048)).encode()

lastkey = hashlib.new(ALGORITHM, key).hexdigest()

otps = []

for _ in range(OTPNUM):
    lastkey = hashlib.new(ALGORITHM, lastkey.encode()).hexdigest()
    otps.append(lastkey)

for i, otp in enumerate(reversed(otps)):
    print(f"{i:>4} {otp}")

while True:
    while True:
        response = input("Enter the hash that follows " + lastkey + ": ")
        result = hashlib.new(ALGORITHM, response.encode()).hexdigest()
        if result == lastkey:
            print("OK!")
            lastkey = response
            break
        else:
            print("Error. Try again")
