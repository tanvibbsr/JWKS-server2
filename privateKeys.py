from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import time

# Generate RSA key
def generate_rsa_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,   # or PKCS1
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem, private_key

# Save key to DB
def save_key_to_db(pem_key, exp_timestamp):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_key, exp_timestamp))
    conn.commit()
    conn.close()

# Example: create expired and valid key
store_key(*generate_key(-10))   # expired
store_key(*generate_key(3600)) # valid