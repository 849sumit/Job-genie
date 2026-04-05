from __future__ import annotations

from pydantic import BaseModel, EmailStr, constr


class UserSignup(BaseModel):
    name: constr(min_length=1, max_length=255)
    contactNo: constr(min_length=10, max_length=15)
    address: constr(min_length=1, max_length=255)
    email: EmailStr
    password: constr(min_length=6, max_length=128)
    



class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        orm_mode = True
