from cryptography.fernet import Fernet
import base64
import hashlib


def generate_encryption_key(shopify_store_id, name):
    combined_key = f"{shopify_store_id}{name}".encode()
    return base64.urlsafe_b64encode(hashlib.sha256(combined_key).digest())


def encrypt_secret_key(secret_key, shopify_store_id, name):
    encryption_key = generate_encryption_key(shopify_store_id, name)
    fernet = Fernet(encryption_key)
    return fernet.encrypt(secret_key.encode()).decode()


def decrypt_secret_key(encrypted_secret_key, shopify_store_id, name):
    encryption_key = generate_encryption_key(shopify_store_id, name)
    fernet = Fernet(encryption_key)
    return fernet.decrypt(encrypted_secret_key.encode()).decode()
