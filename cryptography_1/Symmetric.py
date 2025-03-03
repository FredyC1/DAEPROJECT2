# Symmetric Encryption
from cryptography.fernet import Fernet
message = input("Enter a message: ")
key = Fernet.generate_key() # generate key

enc_obj = Fernet(key)
print(f"Encrypting message: {message}")

encrypted_message = enc_obj.encrypt(message.encode())
print(f"Encryption result: {encrypted_message}")

original_message = enc_obj.decrypt(encrypted_message).decode()

print(f"Original message : {original_message}")

if original_message == message:
    print("Encryption Success")
else:
    print("Encryption Failure")