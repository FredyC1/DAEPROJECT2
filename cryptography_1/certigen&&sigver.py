from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta
import os

# Generate RSA Key Pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Generate a Self-Signed Certificate
def generate_self_signed_cert(private_key, public_key, common_name):
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name)
    ])
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key, hashes.SHA256())
    )
    return certificate

# Save Key and Certificate to Files
def save_key_cert(private_key, certificate, key_filename, cert_filename):
    with open(key_filename, "wb") as f:
        f.write(private_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption()
        ))
    with open(cert_filename, "wb") as f:
        f.write(certificate.public_bytes(Encoding.PEM))

# Sign a Message
def sign_message(private_key, message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Verify a Signature
def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False

# Main Execution
if __name__ == "__main__":
    private_key, public_key = generate_key_pair()
    certificate = generate_self_signed_cert(private_key, public_key, "MyCertificate")
    save_key_cert(private_key, certificate, "private_key.pem", "certificate.pem")
    
    message = b"This is a secure message."
    signature = sign_message(private_key, message)
    
    verification = verify_signature(public_key, message, signature)
    print("Signature valid:", verification)
