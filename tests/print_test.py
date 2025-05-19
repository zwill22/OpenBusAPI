import pytest
from tools.printer import print_config


@pytest.mark.parametrize("newline", (True, False))
def test_print_config(newline):
    with pytest.raises(ValueError):
        print_config(
            "This is a long string and hopefully too long for this function",
            200,
            newline=newline,
        )
