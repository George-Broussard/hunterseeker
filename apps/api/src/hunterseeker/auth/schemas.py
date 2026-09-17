"""Pydantic models for the auth endpoints — the contract ``apps/web`` codes against."""

import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from hunterseeker.auth.models import Role

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128  # argon2 has no practical limit; this bounds hashing cost.


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)
    name: str = Field(min_length=1, max_length=200)
    role: Role

    @field_validator("name")
    @classmethod
    def _strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value


class VerifyCredentialsRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=PASSWORD_MAX_LENGTH)


class UserOut(BaseModel):
    """Public shape of an account. Never includes the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str
    role: Role
