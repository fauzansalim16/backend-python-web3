import unittest
from app.utils.bcrypt_utils import hash_password
import bcrypt
#python -m unittest discover tests
#python -m unittest tests.test_bcrypt_utils
class TestBcryptUtils(unittest.TestCase):

    def test_hash_password_valid(self):
        # Password untuk diuji
        password = "secure_password123"

        # Generate hash menggunakan fungsi yang diujikan
        hashed_password = hash_password(password)

        # Periksa apakah hasil hash adalah string
        self.assertIsInstance(hashed_password, str)

        # Verifikasi bahwa hash cocok dengan password asli
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')))

    def test_hash_password_different_hashes(self):
        # Password yang sama harus menghasilkan hash yang berbeda (karena salt)
        password = "secure_password123"
        hashed_password1 = hash_password(password)
        hashed_password2 = hash_password(password)

        # Hash yang dihasilkan harus berbeda
        self.assertNotEqual(hashed_password1, hashed_password2)

if __name__ == "__main__":
    unittest.main()
