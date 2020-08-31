import random

from vk_auth_project.settings import SECRET_FILE


def secret_key_generator():

    secret_key = ''.join(
        [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]
    )
    with open(SECRET_FILE, 'w') as fw:
        fw.write(secret_key)
