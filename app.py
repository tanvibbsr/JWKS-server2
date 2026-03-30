from flask import Flask, request, jsonify
import sqlite3
import time
import base64
from cryptography.hazmat.primitives import serialization
import jwt
from database import DB_FILE 

app = Flask(__name__)

# -----------------------------
# Database helpers
# -----------------------------
def get_key(expired=False):
    """Retrieve a key from the DB based on expiration"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = int(time.time())
    if expired:
        cursor.execute("SELECT kid, key FROM keys WHERE exp <= ?", (now,))
    else:
        cursor.execute("SELECT kid, key FROM keys WHERE exp > ?", (now,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_valid_keys():
    """Retrieve all non-expired keys"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = int(time.time())
    cursor.execute("SELECT kid, key FROM keys WHERE exp > ?", (now,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -----------------------------
# PEM → JWKS conversion
# -----------------------------
def pem_to_jwk(kid, pem):
    key = serialization.load_pem_private_key(pem, password=None)
    public_key = key.public_key()
    numbers = public_key.public_numbers()

    def b64(n):
        return base64.urlsafe_b64encode(n.to_bytes((n.bit_length()+7)//8, 'big')).rstrip(b'=').decode()

    return {
        "kty": "RSA",
        "use": "sig",
        "kid": str(kid),
        "alg": "RS256",
        "n": b64(numbers.n),
        "e": b64(numbers.e)
    }

# -----------------------------
# POST /auth (also allow GET for browser testing)
# -----------------------------
@app.route("/auth", methods=["POST", "GET"])
def auth():
    expired = "expired" in request.args
    row = get_key(expired)
    if not row:
        return jsonify({"error": "No key found"}), 500

    kid, pem = row
    token = jwt.encode(
        {"user": "userABC", "exp": int(time.time()) + 300},
        pem,
        algorithm="RS256",
        headers={"kid": str(kid)}
    )
    return jsonify({"token": token})

# -----------------------------
# GET /.well-known/jwks.json
# -----------------------------
@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    rows = get_valid_keys()
    keys = [pem_to_jwk(kid, pem) for kid, pem in rows]
    return jsonify({"keys": keys})

# -----------------------------
# Home page
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return "<h2>JWKS Server is running. Use /auth or /.well-known/jwks.json</h2>"

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)