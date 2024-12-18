from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    # Generate RSA Private Key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # Save Private Key
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print("Private key saved as 'private_key.pem'.")

    # Save Public Key
    public_key = private_key.public_key()
    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("Public key saved as 'public_key.pem'.")

if __name__ == "__main__":
    generate_keys()
