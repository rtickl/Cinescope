from datetime import datetime
from typing import List, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationInfo, field_serializer

from constants import Roles


class UserModel(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: List[Union[str, Roles]] = Field(default_factory=lambda: [Roles.USER.value])
    verified: bool = True
    banned: bool = False

    model_config = ConfigDict(extra="forbid")

    @field_validator("passwordRepeat")
    @classmethod
    def validate_password_repeat(cls, v: str, info: ValidationInfo):
        password = info.data.get("password")
        if v != password:
            raise ValueError("Пароли не совпадают")
        return v

    @field_validator("roles", mode="before")
    @classmethod
    def normalize_roles(cls, v):
        if not v:
            return [Roles.USER.value]
        return [r.value if isinstance(r, Roles) else r for r in v]

    @field_serializer("roles")
    def serialize_roles(self, v):
        return [r.value if isinstance(r, Roles) else r for r in v]

class RegisterUserResponse(BaseModel):
    id: str
    email: str
    fullName: str
    createdAt: datetime
    banned: bool | None = None
    roles: list[str] | None = None
    verified: bool | None = None

    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v