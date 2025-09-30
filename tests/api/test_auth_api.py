from api.api_manager import ApiManager
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPI:
    """Набор тестов для проверки Auth API (регистрация и логин)."""
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Проверка успешной регистрации пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        assert response.status_code in [200, 201], \
            f"Unexpected status {response.status_code}: {response.text}"

        data = response.json()
        assert data["email"] == test_user["email"]
        assert "id" in data
        assert "roles" in data
        assert "USER" in data["roles"]

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
            "email": test_user["email"],
            "password": test_user["password"]
        }

        login_response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=200
        )

        json_resp = login_response.json()

        assert "accessToken" in json_resp
        assert isinstance(json_resp["accessToken"], str)