import bcrypt
from cryptography.fernet import Fernet
import json
import os

# Generate or load encryption key
KEY_FILE = os.path.join(os.path.dirname(__file__), '../database/encryption.key')

def get_encryption_key():
    """Get or generate encryption key for data protection."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key

# Initialize Fernet cipher
cipher = Fernet(get_encryption_key())

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def encrypt_data(data):
    """Encrypt sensitive data."""
    if isinstance(data, dict):
        data = json.dumps(data)
    encrypted = cipher.encrypt(data.encode('utf-8'))
    return encrypted.decode('utf-8')

def decrypt_data(encrypted_data):
    """Decrypt sensitive data."""
    if not encrypted_data:
        return None
    decrypted = cipher.decrypt(encrypted_data.encode('utf-8'))
    try:
        return json.loads(decrypted.decode('utf-8'))
    except json.JSONDecodeError:
        return decrypted.decode('utf-8')
