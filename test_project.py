import pytest
import string
from project import calculate_entropy, find_patterns, is_common, score_password, get_strength_label, generate_password

def test_calculate_entropy():
    assert calculate_entropy("") == 0.0
    assert calculate_entropy("rehan") == pytest.approx(23.502, abs=0.01)
    assert calculate_entropy("Rehan@01") == pytest.approx(52.437, abs=0.01)

def test_find_patterns():
    assert find_patterns("xkac") == []
    assert find_patterns("aaay") == ["Repeated characters."]
    assert find_patterns("yaxyz") == ["Sequential characters."]
    assert find_patterns("ya123") == ["Sequential characters."]

def test_is_common():
    assert is_common("123456") == True
    assert is_common("1as56") == False
    assert is_common("qwerty") == True

def test_score_password():
    assert score_password("") == 0
    assert score_password("abcd") == pytest.approx(16.336, abs=0.01)
    assert score_password("acdx12@") == pytest.approx(71.020, abs=0.01)
    assert score_password("1234") == 10

def test_get_strength_label():
    assert get_strength_label(0) == "Weak"
    assert get_strength_label(23) == "Weak"
    assert get_strength_label(78) == "Strong"
    assert get_strength_label(17) == "Weak"
    assert get_strength_label(54) == "Medium"

def test_generate_password():
    pwd = generate_password(12)
    assert len(pwd) == 12
    assert any(c.islower() for c in pwd)
    assert any(c.isupper() for c in pwd)
    assert any(c.isdigit() for c in pwd)
    assert any(c in string.punctuation for c in pwd)
