# Hash Function 
import hashlib

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

hash = input("Hash this: ")
hash2 = input("What about this: ")

hashed1 = hash_pass(hash)
hashed2 = hash_pass(hash2)

print(f"Original Password: {hash}")
print(f"Hashed: {hashed1}")
print(f"\nModified password: {hash2}")
print(f"hashed: {hashed2}")
