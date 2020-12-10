import random
import string

# We shuffle our alphabet to make it a bit harder to guess the short url reference that
# will be created next. We use a random seed to shuffle our alphabet in a reproducible
# fashion, so a number translates to the same encoded string even after the webserver
# restarts.
random.seed(42)

ALPHABET_LIST = list(string.ascii_letters + string.digits)
random.shuffle(ALPHABET_LIST)

ALPHABET = "".join(ALPHABET_LIST)


def int_to_custom_base(number: int, alphabet: str = ALPHABET) -> str:
    """
    Encodes a given a positive integer in a custom alphabet.
    The base is will be the length of the provided alphabet.
    E.g. int_to_custom_base(100, 'abc') -> 'bacab'
    """
    base = len(alphabet)
    result = ""

    while number > 0:
        number, idx = divmod(number, base)
        result = f"{alphabet[idx]}{result}"

    return result or "0"
