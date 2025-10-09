from constants import BASE_URL_AUTH
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """Класс для работы с API пользователей."""

    def __init__(self, session, base_url=BASE_URL_AUTH):
        super().__init__(session=session, base_url=base_url, headers={"Content-Type": "application/json"})
        self.session = session

    def get_user_info(self, user_id, expected_status=200):
        """Получение информации о пользователе."""
        return self.send_request(
            method="GET",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """Удаление пользователя."""
        return self.send_request(
            method="DELETE",
            endpoint=f"user/{user_id}",
            expected_status=expected_status
        )

    def delete_user_by_email(self, email, expected_status=204):
        """Удаление пользователя по email."""
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/by-email/{email}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def get_user(self, user_locator, expected_status=200):
        return self.send_request("GET", f"user/{user_locator}", expected_status=expected_status)
