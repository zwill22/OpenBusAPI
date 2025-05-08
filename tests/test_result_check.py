import pytest
from tools.location_reader import analyse_response

check_inputs = [
    ("", False),
    ("<Siri></Siri>", True),
    ("<Siri></Siri><Siri></Siri>", False),
    ("<ServiceDelivery></ServiceDelivery>", True),
]


@pytest.mark.parametrize("input_str, valid", check_inputs)
def test_response(input_str: str, valid: bool, schema):
    with pytest.raises(ValueError) as e:
        analyse_response(input_str, schema=schema)
    assert str(e.value) == "XML is not valid"
