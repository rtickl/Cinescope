import allure
import pytest_check as check
from datetime import datetime


from api.api_manager import ApiManager
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, Roles
from models.base_models import RegisterUserResponse
from tests.api.test_user import TestUser


class TestAuthAPI:
    """Набор тестов для проверки Auth API (регистрация и логин)."""

    def test_register_and_login_user(self, api_manager, test_user):
        resp = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**resp.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        """
        Тест на регистрацию и последующий логин пользователя.
        """

        assert response.status_code in [200, 201], \
            f"Unexpected status {response.status_code}: {response.text}"

        login_data = {
            "email": test_user.email,
            "password": test_user.password
        }
        response = api_manager.auth_api.login_user(login_data)
        json_resp = response.json()

        assert "accessToken" in json_resp
        assert isinstance(json_resp["accessToken"], str)

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
        with allure.step("Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(
                id="id",
                email="email@email.com",
                fullName="fullName",
                verified=True,
                banned=False,
                roles=[Roles.SUPER_ADMIN],
                createdAt=str(datetime.now())
            )

            mocker.patch.object(
                api_manager.auth_api,
                'register_user',
                return_value=mock_response
            )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(test_user)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка поля персональных данных"):
                with check.check():
                    check.equal(register_user_response.fullName, mock_response.fullName, "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email, mock_response.email)

            with allure.step("Проверка поля banned"):
                with check.check("Проверка поля banned"):
                    check.equal(register_user_response.banned, mock_response.banned)