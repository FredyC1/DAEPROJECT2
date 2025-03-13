from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from argon2 import PasswordHasher
import hmac
import hashlib

class AESCipher:
    def __init__(self, key: bytes):
        self.key = key
    
    def encrypt_ecb(self, plaintext: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_plaintext = self._pad(plaintext.encode())
        ciphertext = cipher.encrypt(padded_plaintext)
        return base64.b64encode(ciphertext).decode()
    
    def decrypt_ecb(self, ciphertext: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        return self._unpad(decrypted_data).decode()
    
    def encrypt_cbc(self, plaintext: str) -> str:
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_plaintext = self._pad(plaintext.encode())
        ciphertext = iv + cipher.encrypt(padded_plaintext)
        return base64.b64encode(ciphertext).decode()
    
    def decrypt_cbc(self, ciphertext: str) -> str:
        raw_data = base64.b64decode(ciphertext)
        iv = raw_data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(raw_data[AES.block_size:])
        return self._unpad(decrypted_data).decode()
    
    def _pad(self, data: bytes) -> bytes:
        pad_length = AES.block_size - len(data) % AES.block_size
        return data + bytes([pad_length] * pad_length)
    
    def _unpad(self, data: bytes) -> bytes:
        return data[:-data[-1]]

# Secure Password Hashing using Argon2
ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except:
        return False

# HMAC for Message Authentication
def generate_hmac(key: bytes, message: str) -> str:
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def verify_hmac(key: bytes, message: str, mac: str) -> bool:
    return hmac.compare_digest(mac, generate_hmac(key, message))

# File Integrity Verification using HMAC
def generate_file_hmac(key: bytes, file_path: str) -> str:
    with open(file_path, 'rb') as f:
        file_data = f.read()
    return hmac.new(key, file_data, hashlib.sha256).hexdigest()

def verify_file_hmac(key: bytes, file_path: str, expected_hmac: str) -> bool:
    return hmac.compare_digest(expected_hmac, generate_file_hmac(key, file_path))

# Example Usage
key = get_random_bytes(16)  # AES-128
cipher = AESCipher(key)
plaintext = "This is a secret message."

ecipher = cipher.encrypt_ecb(plaintext)
dcipher = cipher.decrypt_ecb(ecipher)
print("ECB Encrypted:", ecipher)
print("ECB Decrypted:", dcipher)

ccipher = cipher.encrypt_cbc(plaintext)
dcipher = cipher.decrypt_cbc(ccipher)
print("CBC Encrypted:", ccipher)
print("CBC Decrypted:", dcipher)

# Password Hashing Example
password = "securepassword123"
hashed_pw = hash_password(password)
print("Hashed Password:", hashed_pw)
print("Password Verified:", verify_password(password, hashed_pw))

# HMAC Example
hmac_key = get_random_bytes(16)
message = "Authenticate this message"
mac = generate_hmac(hmac_key, message)
print("Generated HMAC:", mac)
print("HMAC Verified:", verify_hmac(hmac_key, message, mac))

# File Integrity Verification Example
file_path = "example.txt"
with open(file_path, "w") as f:
    f.write("Sensitive data in a file.")
file_mac = generate_file_hmac(hmac_key, file_path)
print("Generated File HMAC:", file_mac)
print("File HMAC Verified:", verify_file_hmac(hmac_key, file_path, file_mac))
# Stream Cipher Example
stream_key = get_random_bytes(32)
nonce = get_random_bytes(8)
stream_cipher = ChaCha20Cipher(stream_key, nonce)
ciphertext = stream_cipher.encrypt(plaintext)
decrypted_text = stream_cipher.decrypt(ciphertext)
print("ChaCha20 Encrypted:", ciphertext)
print("ChaCha20 Decrypted:", decrypted_text)
