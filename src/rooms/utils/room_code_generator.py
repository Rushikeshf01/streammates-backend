import random
import time

# from ..models import Room
from .constants import ADJECTIVES, NOUNS

def base36_encode(number):
    """Encodes an integer into base36 (0-9 + a-z)."""
    
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'

    base36 = ''
    while number > 0:
        number, rem = divmod(number, 36)
        base36 = chars[rem] + base36
    
    return base36 or '0'


def generate_room_code():
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    rand_num = random.randint(1000, 999999)
    tail = base36_encode(rand_num)
    return f'{adjective}-{noun}-{tail}'

# print(generate_room_code())