from cryptography.fernet import Fernet

key=Fernet.generate_key()
f=Fernet(key)
##print(f"{key}, {f}")
a="Hello world!"
encrypt=f.encrypt(a.encode())
print(f" Frase cryptata: {encrypt}")
decrypt=f.decrypt(encrypt)
print(f" Frase decryptata: {decrypt.decode()}")

## encode() serve a convertire la stringa a in bytes
## decode() converte i bytes in stringa
