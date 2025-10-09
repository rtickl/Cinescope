from api.api_manager import ApiManager
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from models.base_models import RegisterUserResponse


class TestAuthAPI:
    """Набор тестов для проверки Auth API (регистрация и логин)."""
    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"


    def test_register_and_login_user(self, requester, test_user):
        """
        Тест на регистрацию и последующий логин пользователя.
        """

        response = requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=test_user,
            expected_status=None
        )

        assert response.status_code in [200, 201], \
            f"Unexpected status {response.status_code}: {response.text}"

        login_data = {
            "email": test_user.email,
            "password": test_user.password
        }

        login_response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=201
        )

        json_resp = login_response.json()

        assert "accessToken" in json_resp
        assert isinstance(json_resp["accessToken"], str)