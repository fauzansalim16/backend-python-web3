import hashlib
import json

def generate_record_hash(record):
    """
    Membuat hash dari sebuah record.
    :param record: Dictionary berisi data record.
    :return: String hash SHA-256.
    """
    record_string = json.dumps(record, sort_keys=True)
    return hashlib.sha256(record_string.encode('utf-8')).hexdigest()
