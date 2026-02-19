from pydantic import BaseModel, Field, EmailStr

class RegisterSchema(BaseModel):
    username: str = Field()
    name:     str = Field()
    surname:  str = Field()
    email:    EmailStr = Field()
    password: str = Field()