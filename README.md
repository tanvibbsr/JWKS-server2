# JWKS-server2

Overview: 

This project implements a JSON Web Key Set (JWKS) server with JWT authentication, backed by a SQLite database for storing private keys.

--------------------------------------------------------------------------------------------------------------------------------

Key features:

- Issues JWTs for users via /auth
- Supports expired and valid keys
- Serves public keys in JWKS format: /.well-known/jwks.json
- Keys are persisted in SQLite

----------------------------------------------------------------------------------------------------------------------------------

Prerequisites:

- Python 3.10+
- Required Python packages: pip install flask cryptography pyjwt

----------------------------------------------------------------------------------------------------------------------------------

Endpoints:

Home Page: GET /
- Displays a friendly message about available endpoints

Authenticate User:

POST /auth 
- simulates issuing a JWT for a user

GET /.well-known/jwks.json
- Returns all non-expired public keys in JWKS format.

----------------------------------------------------------------------------------------------------------------------------------

Test Coverage(>80%):
- pytest --cov=app test_app.py
 