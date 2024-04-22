from cryptography.fernet import Fernet

key = Fernet.generate_key()

key_file_path = 'secret.key'
with open(key_file_path, 'wb') as f:
    f.write(key)

print(f"Key has been generated and saved to {key_file_path}")
