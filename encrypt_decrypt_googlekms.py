from google.cloud import kms_v1
import base64
import sys
import os

project_id = os.getenv('PROJECT_ID')
location_id = os.getenv('LOCATION_ID')
key_ring_id = os.getenv('KEY_RING_ID')
crypto_key_id = os.getenv('CRYPTO_KEY_ID')



def encrypt(plaintext):
    """Encrypts input plaintext data using the provided symmetric CryptoKey."""

    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)
    response = client.encrypt(name, plaintext)
    return base64.b64encode(response.ciphertext)

def decrypt(ciphertext):
    """Decrypts input ciphertext using the provided symmetric CryptoKey."""

    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)
    ciphertext = base64.b64decode(ciphertext)
    response = client.decrypt(name, ciphertext)
    return response.plaintext

if __name__ == '__main__':
    action = str(sys.argv[1]).encode('utf-8')
    if action == b'encrypt':
        try:
            with open(sys.argv[2]) as file:
                data = file.read()
            secret_encrypted = encrypt(bytes(data, encoding="utf-8"))
            with open(sys.argv[2]+'.encrypted', 'wb') as file:
                file.write(secret_encrypted)
            print("File encrypted")
        except Exception as e:
            print(e)
    elif action == b'decrypt':
        try:
            with open(sys.argv[2]) as file:
                data = file.read()
            filename = sys.argv[2].replace('.encrypted','')
            secret = decrypt(bytes(data, encoding="utf-8"))
            with open(filename, 'wb') as file:
                file.write(secret)
            print("File done")
        except Exception as e:
            print(e)

# ciphertext = base64.b64encode(encrypt(b'Hola Mundo'))
# print(decrypt(ciphertext))