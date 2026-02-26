import re
import regex

from pydantic import BaseModel, Field, EmailStr, field_validator

NAME_PATTERN = regex.compile(r"^[\p{L}]+(?:[\p{L}\s'-]*[\p{L}])?$")

class RegisterSchema(BaseModel):
    username:   str = Field(..., min_length=5, max_length=30, pattern=r'^[a-zA-Z0-9_]')
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name:  str = Field(..., min_length=2, max_length=50)
    email:      EmailStr
    password:   str = Field(..., min_length=8, max_length=128)
    
    @field_validator('first_name', 'last_name')
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not NAME_PATTERN.fullmatch(v):
            raise ValueError("Name must contain only letters")
        return v    
    
    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('The password must contain Latin characters.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('The password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', v):
            raise ValueError('The password must contain at least one lowercase letter.')
        if not re.search(r'\d', v):
            raise ValueError('The password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?\':{}|<>]', v):
            raise ValueError('The password must contain at least one special character.')
        if ' ' in v:
            raise ValueError('The password cannot contain spaces.')
        return v
    
class LoginSchema(BaseModel):
    email:    EmailStr
    password: str = Field(..., min_length=8, max_length=128)