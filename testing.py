from app.utils.crypto_utils import encrypt_aes,decrypt_aes, hex_to_bytes

#print(encrypt_aes("hello"))
text = hex_to_bytes('\xfa(>\x0b\x1eI\xa7\xf6v\x88\x97\xaa|.k\xc2\x99\xb6\x8a@-/~9\xe9\xa3\x07\xac\xf5k^\x85')
print(decrypt_aes(text))