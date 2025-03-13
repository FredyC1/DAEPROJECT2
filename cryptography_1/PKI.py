from cryptography.x509 import Name, NameAttribute
from cryptography import x509
from cryptography.hazmat.primitives import hashes
import datetime

# Certificate details
subject = issuer = x509.Name([
    x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(x509.NameOID.LOCALITY_NAME, "Los Angeles"),
    x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "MyOrg"),
    x509.NameAttribute(x509.NameOID.COMMON_NAME, "myorg.com"),
])

# Create certificate
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    public_key
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).sign(private_key, hashes.SHA256())

# Save certificate
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Self-signed certificate created.")
