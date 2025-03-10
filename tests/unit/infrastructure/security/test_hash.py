from src.infrastructure.security.hash import hash_password, verify_password

def test_hash_password():
    password = "securepassword"
    hashed_password = hash_password(password)

    assert password != hashed_password
    assert verify_password(password, hashed_password)

def test_verify_password():
    password = "mypassword"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)
