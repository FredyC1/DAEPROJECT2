from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import Certificate, Name, NameAttribute
from cryptography.x509.oid import NameOID
from cryptography import x509
import datetime
import os

# Generate RSA Key Pair
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Save private key
def save_private_key(private_key, filename="private_key.pem"):
    with open(filename, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

# Save public key
def save_public_key(public_key, filename="public_key.pem"):
    with open(filename, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# Sign a message
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

# Verify a signature
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
    except:
        return False

# Generate a self-signed certificate
def generate_certificate(private_key, public_key, common_name="Test Cert", days_valid=365):
    subject = issuer = Name([
        NameAttribute(NameOID.COMMON_NAME, common_name)
    ])
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)
    cert = cert.public_key(public_key)
    cert = cert.serial_number(x509.random_serial_number())
    cert = cert.not_valid_before(datetime.datetime.utcnow())
    cert = cert.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days_valid))
    cert = cert.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True
    )
    cert = cert.sign(private_key, hashes.SHA256())
    return cert

# Save certificate
def save_certificate(cert, filename="certificate.pem"):
    with open(filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

# Validate a certificate against a CA certificate
def validate_certificate(cert_pem, ca_cert_pem):
    try:
        cert = x509.load_pem_x509_certificate(cert_pem)
        ca_cert = x509.load_pem_x509_certificate(ca_cert_pem)
        ca_cert.public_key().verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm
        )
        return True
    except:
        return False

# Example Usage
if __name__ == "__main__":
    # Key Pair Generation
    priv_key, pub_key = generate_rsa_key_pair()
    save_private_key(priv_key)
    save_public_key(pub_key)

    # Message Signing & Verification
    msg = b"This is a signed message."
    sig = sign_message(priv_key, msg)
    print("Signature Verified:", verify_signature(pub_key, msg, sig))

    # Certificate Generation
    cert = generate_certificate(priv_key, pub_key)
    save_certificate(cert)
    print("Certificate generated and saved.")

    # Trust Model Documentation
    print("\nTrust Model:\n")
    print("1. A Root Certificate Authority (CA) generates a self-signed root certificate.")
    print("2. The CA signs client certificates, ensuring authenticity.")
    print("3. End-users verify certificates using the CA’s public key.")
    print("4. Trust is established through hierarchical validation.")
