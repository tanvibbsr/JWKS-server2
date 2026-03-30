import sqlite3
import time
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

DB_FILE = "totally_not_my_privateKeys.db"

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS keys(
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            key BLOB NOT NULL,
            exp INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Generate RSA private key and return PEM
def generate_key(exp_offset):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    exp_timestamp = int(time.time()) + exp_offset
    return pem, exp_timestamp

# Insert key into DB
def insert_key(pem, exp):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem, exp))
    conn.commit()
    conn.close()

# Seed DB with one expired and one valid key
def seed_keys():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM keys")
    count = cursor.fetchone()[0]
    conn.close()
    if count == 0:
        insert_key(*generate_key(-10))   # expired
        insert_key(*generate_key(3600))  # valid
        print("✅ Database seeded with keys")

# Run on import
init_db()
seed_keys()