from cryptography.fernet import Fernet

key = Fernet.generate_key()

f = Fernet(key)

encrypted = f.encrypt(b"SuperSecretPassword")
print(encrypted)

decrypted = f.decrypt(encrypted)
print(decrypted) # .decode() for str conversion