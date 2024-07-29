import random
import string


def generate_random_text(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


MESSAGE = generate_random_text(10)

VALID_EMAIL = ''
VALID_PASSWORD = ''

NEW_USER_PASSWORD = '87654321'
