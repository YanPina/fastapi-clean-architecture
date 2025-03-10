import pytest
from fastapi import HTTPException
from src.core.exceptions import DuplicatedError, AuthError, NotFoundError, ValidationError


def test_duplicated_error():
    """Test that DuplicatedError raises the correct HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        raise DuplicatedError("User already exists")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User already exists"


def test_auth_error():
    """Test that AuthError raises the correct HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        raise AuthError("Unauthorized access")
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Unauthorized access"


def test_not_found_error():
    """Test that NotFoundError raises the correct HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        raise NotFoundError("User not found")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_validation_error():
    """Test that ValidationError raises the correct HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        raise ValidationError("Invalid data format")
    
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid data format"
