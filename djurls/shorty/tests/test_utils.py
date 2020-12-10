import pytest

from djurls.shorty.utils import int_to_custom_base


@pytest.mark.parametrize(
    ("number", "alphabet", "expected_result"),
    (
        (0, "01", "0"),
        (1, "01", "1"),
        (10, "0123456789", "10"),
        (16777215, "0123456789ABCDEF", "FFFFFF"),
    ),
)
def test_int_to_custom_base(number, alphabet, expected_result):
    assert int_to_custom_base(number=number, alphabet=alphabet) == expected_result
