import os

# Generate a symmetric key
symmetric_key = os.urandom(32)

# Encrypt symmetric key with RSA public key
encrypted_key = public_key.encrypt(
    symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypt symmetric key with RSA private key
decrypted_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Original Key:", symmetric_key)
print("Decrypted Key:", decrypted_key)
print("Keys match:", symmetric_key == decrypted_key)
