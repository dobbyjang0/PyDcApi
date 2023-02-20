import random

def add_blank(title):
    idx = 0
    while True:
        if idx > len(title):
            idx = 0

        yield title[:idx] + chr(0x200B) + title[idx:]
        idx += 1

def random_unicode():
    return chr(random.randrange(0x400, 0x500))