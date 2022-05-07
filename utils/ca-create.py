import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=default_backend()
)

public_key = private_key.public_key()

pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
)

pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

with open("/tmp/ca.key", "wb") as out:
    out.write(pem_private)

with open("/tmp/ca.pub", "wb") as out:
    out.write(pem_public)

print("Created files in /tmp/ca.key /tmp/ca.pub /tmp/ca.cert")

subject = issuer = x509.Name(
    [
        x509.NameAttribute(NameOID.COUNTRY_NAME, "MOR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "M"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Morocco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Athena by Yezz123"),
        x509.NameAttribute(NameOID.COMMON_NAME, "https://yezz123.github.io/"),
    ]
)

cert = x509.CertificateBuilder().subject_name(subject)
cert = cert.issuer_name(issuer)
cert = cert.public_key(public_key)
cert = cert.serial_number(x509.random_serial_number())
cert = cert.not_valid_before(datetime.datetime.utcnow())
cert = cert.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=30))
cert = cert.sign(private_key, hashes.SHA256(), default_backend())

# Write our certificate out to disk.
with open("/tmp/ca.cert", "wb") as out:
    out.write(cert.public_bytes(serialization.Encoding.PEM))
