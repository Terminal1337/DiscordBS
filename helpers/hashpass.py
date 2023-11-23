import hashlib
import random
import string
def md5_hash_password(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))

    hashed_password = md5_hash.hexdigest()

    return hashed_password

def generate_random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


print(md5_hash_password('9668385700'))