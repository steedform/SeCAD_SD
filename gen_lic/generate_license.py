from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime, timedelta
import base64

def generate_license(private_key_path="private_key.pem", output="license.lic"):
    # License expiry date: 3 months from today
    expiry_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    print(f"License expiry date: {expiry_date}")

    # Load Private Key
    with open(private_key_path, "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)
    
    # Sign the expiry date
    signature = private_key.sign(
        expiry_date.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Save License File: expiry_date + signature
    with open(output, "w") as license_file:
        license_file.write(expiry_date + "\n")
        license_file.write(base64.b64encode(signature).decode())
    
    print(f"License file '{output}' created successfully.")

if __name__ == "__main__":
    generate_license()
