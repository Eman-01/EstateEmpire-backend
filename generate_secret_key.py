import secrets

app_secret_key = secrets.token_hex(32)
jwt_secret_key = secrets.token_urlsafe(16)

with open('.env', 'a') as f:
    f.write(f"SECRET_KEY={app_secret_key}")
    f.write(f"JWT_SECRET_KEY={jwt_secret_key}")
    