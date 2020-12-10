from django.conf import settings


def int_to_custom_base(number: int, alphabet: str = settings.ALPHABET) -> str:
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
