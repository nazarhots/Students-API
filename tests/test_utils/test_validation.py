from utils.validation import validate_empty_values

def test_validate_empty_values():
    text, status_code = validate_empty_values("test", "")
    
    assert text == "Values can't be empty"
    assert status_code == 400