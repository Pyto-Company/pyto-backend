import secrets

def generate_secret_key(length=32):
    return secrets.token_hex(length)

secret_key = generate_secret_key()  # Default 64-character key
print(f"Generated Secret Key: {secret_key}")
