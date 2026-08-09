import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "defaultdb"),
    "port": int(os.getenv("DB_PORT", "13334")),
    "ssl": {
        "ca": "/etc/secrets/ca.pem"
}
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")