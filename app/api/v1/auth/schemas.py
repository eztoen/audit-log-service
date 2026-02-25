from pydantic import BaseModel, Field, EmailStr, field_validator

class RegisterSchema(BaseModel):
    username: str = Field(..., min_length=5, max_length=30, pattern=r"^[a-zA-Z0-9_]")
    name:     str = Field(..., min_length=2, max_length=50, pattern=r"\p{L}+")
    surname:  str = Field(..., min_length=2, max_length=50, pattern=r"\p{L}+")
    email:    EmailStr
    password: str
    
    @field_validator('password')
    def validate_password(cls, v):
        ...
    
class LoginSchema(BaseModel):
    email:    EmailStr = Field()
    password: str = Field()