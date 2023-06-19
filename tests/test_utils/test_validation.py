from utils.validation import validate_values


def test_validate_values():
    text, status_code = validate_values(1, "test", "")
    
    assert text == "Values can't be empty"
    assert status_code == 400
