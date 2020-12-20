from django.conf import settings


def encode_custom_base(number: int, alphabet: str = settings.ALPHABET) -> str:
    """
    Encodes a positive base10 integer using a custom alphabet.
    E.g. int_to_custom_base(100, 'abc') -> 'bacab'
    """
    if number < 1:
        raise ValueError(
            f"Unsupported value for argument 'number': {number} . "
            "Encoding is only supported for positive integers greater than 0"
        )

    base = len(alphabet)
    result = ""

    while number > 0:
        number, idx = divmod(number, base)
        result = f"{alphabet[idx]}{result}"

    return result


def decode_custom_base(encoded_number: str, alphabet: str = settings.ALPHABET) -> int:
    """
    Decodes a number that was encoded with the given alphabet back to base 10
    E.g. int_to_custom_base(100, 'abc') -> 'bacab'
    """
    base = len(alphabet)
    result = 0

    # add padding to the encoded string so the math works out
    while len(encoded_number) < len(alphabet):
        encoded_number = f"{alphabet[0]}{encoded_number}"

    for idx, char in enumerate(encoded_number):
        char_val = alphabet.index(char)
        power = len(encoded_number) - idx - 1
        result += (base ** power) * char_val

    return result
