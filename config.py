import os

# Create Aiven CA certificate file
ca_cert = os.getenv("AIVEN_CA_CERT")

if ca_cert:
    with open("/tmp/ca.pem", "w") as f:
        f.write(ca_cert)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "defaultdb"),
    "port": int(os.getenv("DB_PORT", "13334")),
    "ssl": {
        "ca": "/tmp/ca.pem"
    }
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")