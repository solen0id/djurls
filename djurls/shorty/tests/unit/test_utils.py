import pytest

from djurls.shorty.utils import decode_custom_base, encode_custom_base


@pytest.mark.parametrize(("number"), ((0), (-1)))
def test_encode_custom_base_raises_on_invalid_input(number):
    with pytest.raises(
        ValueError, match=(f"Unsupported value for argument 'number': {number} .")
    ):
        encode_custom_base(number)


@pytest.mark.parametrize(
    ("number", "alphabet", "expected_result"),
    (
        (1, "01", "1"),
        (2, "01", "10"),
        (10, "0123456789", "10"),
        (16777215, "0123456789ABCDEF", "FFFFFF"),
    ),
)
def test_encode_custom_base(number, alphabet, expected_result):
    assert encode_custom_base(number=number, alphabet=alphabet) == expected_result


@pytest.mark.parametrize(
    ("encoded_number", "alphabet", "expected_result"),
    (
        ("1", "01", 1),
        ("10", "01", 2),
        ("10", "0123456789", 10),
        ("FFFFFF", "0123456789ABCDEF", 16777215),
    ),
)
def test_decode_custom_base(encoded_number, alphabet, expected_result):
    assert (
        decode_custom_base(encoded_number=encoded_number, alphabet=alphabet)
        == expected_result
    )


@pytest.mark.parametrize(("number"), ((1), (2), (42), (16777215)))
def test_encode_then_decode_returns_original_number(number):
    encoded = encode_custom_base(number)
    decoded = decode_custom_base(encoded)
    print(f"{number=}")
    print(f"{encoded=}")
    print(f"{decoded=}")

    assert decoded == number
