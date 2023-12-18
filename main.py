from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
import os

class FileEncryptor:
    def __init__(self, key=None, algorithm="fernet"):
        self.algorithm = algorithm.lower()
        if self.algorithm == "rsa":
            self.private_key, self.public_key = self.generate_rsa_key_pair()
        elif self.algorithm == "fernet":
            self.key = key or Fernet.generate_key()
        else:
            raise ValueError("Unsupported encryption algorithm")

    def generate_rsa_key_pair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def save_rsa_key_to_file(self, key, file_path):
        with open(file_path, 'wb') as file:
            pem = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            file.write(pem)

    def load_rsa_key_from_file(self, file_path):
        with open(file_path, 'rb') as file:
            key_data = file.read()
        return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            data = file.read()

        if self.algorithm == "rsa":
            ciphertext = self.public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        elif self.algorithm == "fernet":
            cipher_suite = Fernet(self.key)
            ciphertext = cipher_suite.encrypt(data)
        else:
            raise ValueError("Unsupported encryption algorithm")

        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, 'wb') as file:
            file.write(ciphertext)

        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path):
        with open(encrypted_file_path, 'rb') as file:
            ciphertext = file.read()

        if self.algorithm == "rsa":
            plaintext = self.private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        elif self.algorithm == "fernet":
            cipher_suite = Fernet(self.key)
            plaintext = cipher_suite.decrypt(ciphertext)
        else:
            raise ValueError("Unsupported encryption algorithm")

        decrypted_file_path = encrypted_file_path[:-10]
        with open(decrypted_file_path, 'wb') as file:
            file.write(plaintext)

        return decrypted_file_path

def main():
    try:
        # For Fernet encryption
        file_encryptor = FileEncryptor(algorithm="fernet")
        key = file_encryptor.key

        

        original_file_path = "example.txt"
        encrypted_file_path = file_encryptor.encrypt_file(original_file_path)
        print(f"File encrypted: {encrypted_file_path}")

        decrypted_file_path = file_encryptor.decrypt_file(encrypted_file_path)
        print(f"File decrypted: {decrypted_file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
