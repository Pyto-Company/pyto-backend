import hashlib

class PasswordConfig():
    def hash(password: str):
        return hashlib.sha256(password.encode()).hexdigest()