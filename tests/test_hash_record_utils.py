import unittest
from app.utils.hash_record_utils import generate_record_hash
import hashlib
from flask import json

class TestHashRecordUtils(unittest.TestCase):

    def test_generate_record_hash_consistency(self):
        # Input record yang sama harus menghasilkan hash yang sama
        record = {"id": 1, "name": "John Doe", "age": 30}
        hash1 = generate_record_hash(record)
        hash2 = generate_record_hash(record)

        # Hash harus sama
        self.assertEqual(hash1, hash2)

    def test_generate_record_hash_uniqueness(self):
        # Input record yang berbeda harus menghasilkan hash yang berbeda
        record1 = {"id": 1, "name": "John Doe", "age": 30}
        record2 = {"id": 1, "name": "Jane Doe", "age": 25}

        hash1 = generate_record_hash(record1)
        hash2 = generate_record_hash(record2)

        # Hash harus berbeda
        self.assertNotEqual(hash1, hash2)

    def test_generate_record_hash_algorithm(self):
        # Periksa apakah hash dihasilkan dengan SHA-256
        record = {"id": 1, "name": "John Doe", "age": 30}
        expected_hash = hashlib.sha256(
            json.dumps(record, sort_keys=True).encode('utf-8')
        ).hexdigest()

        # Hash yang dihasilkan harus sesuai dengan implementasi SHA-256
        self.assertEqual(generate_record_hash(record), expected_hash)

    def test_generate_record_hash_sorting(self):
        # Record dengan urutan field berbeda harus menghasilkan hash yang sama
        record1 = {"name": "John Doe", "id": 1, "age": 30}
        record2 = {"id": 1, "age": 30, "name": "John Doe"}

        hash1 = generate_record_hash(record1)
        hash2 = generate_record_hash(record2)

        # Hash harus sama meskipun urutan field berbeda
        self.assertEqual(hash1, hash2)

if __name__ == "__main__":
    unittest.main()
