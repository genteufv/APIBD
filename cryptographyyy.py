from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def encrypt(file_path, public_key_path, encrypted_file_path):
    # Carregar a chave pública
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    # Ler o conteúdo do arquivo
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Criptografar os dados com a chave pública
    encrypted_data = public_key.encrypt(
        file_data,
        padding.PKCS1v15()  # Mesma forma de padding utilizada na descriptografia
    )

    # Salvar os dados criptografados em um arquivo .enc
    with open(encrypted_file_path, "wb") as enc_file:
        enc_file.write(encrypted_data)

# Exemplo de uso
encrypt("credentials.txt", "public.pem", "credentials_PostgreSQL.enc")
