from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List
from constants import Roles


class RegistrationUserModel(BaseModel):
    """Модель данных для регистрации нового пользователя."""

    email: EmailStr = Field(..., description="Email пользователя")
    fullName: str = Field(..., description="Полное имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")
    passwordRepeat: str = Field(..., min_length=6, description="Повтор пароля")
    roles: List[str] = Field(default_factory=lambda: [Roles.USER.value])

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "fullName": "John Doe",
                "password": "Secure123!",
                "passwordRepeat": "Secure123!",
                "roles": ["USER"],
            }
        },
    )