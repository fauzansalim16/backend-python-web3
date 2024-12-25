import unittest
from app.utils.crypto_utils import generate_ethereum_key_pair, encrypt_aes, decrypt_aes
from app.config import Config
import secrets

class TestCryptoUtils(unittest.TestCase):
    
    def test_generate_ethereum_key_pair(self):
        # Generate key pair
        private_key, public_key = generate_ethereum_key_pair()

        # Private key harus berupa hex string dengan panjang 64 karakter (32 bytes dalam hex)
        self.assertEqual(len(private_key), 66)
        self.assertIsInstance(private_key, str)

        # Public key harus berupa hex string
        self.assertIsInstance(public_key, str)
        self.assertGreater(len(public_key), 0)  # Panjang public key tergantung library

    def test_encrypt_aes_and_decrypt_aes(self):
        # Plain text untuk diuji
        plain_text = "This is a secret message."

        # Enkripsi
        encrypted_data = encrypt_aes(plain_text)

        # Pastikan hasil enkripsi bukan None atau kosong
        self.assertIsNotNone(encrypted_data)
        self.assertGreater(len(encrypted_data), 16)  # Minimal ada IV + data

        # Dekripsi
        decrypted_text = decrypt_aes(encrypted_data)

        # Hasil dekripsi harus sama dengan plain text awal
        self.assertEqual(decrypted_text, plain_text)

    def test_aes_encryption_key_size(self):
        # Pastikan panjang key sesuai dengan konfigurasi AES_KEY_SIZE
        encryption_key = Config.ENCRYPTION_KEY
        aes_key_size = Config.AES_KEY_SIZE

        # Key dikonversi ke bytes
        key_bytes = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
        key_bytes = key_bytes[:aes_key_size]

        self.assertEqual(len(key_bytes), aes_key_size)

    def test_encrypt_aes_different_outputs(self):
        # Pastikan hasil enkripsi berbeda untuk teks yang sama (karena IV unik)
        plain_text = "This is a secret message."

        encrypted_data_1 = encrypt_aes(plain_text)
        encrypted_data_2 = encrypt_aes(plain_text)

        # Hasil enkripsi tidak boleh sama
        self.assertNotEqual(encrypted_data_1, encrypted_data_2)

if __name__ == "__main__":
    unittest.main()
