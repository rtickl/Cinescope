from constants import BASE_URL_AUTH
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session, base_url=BASE_URL_AUTH):
        super().__init__(session=session, base_url=base_url, headers={"Content-Type": "application/json"})
        self.session = session

    def get_user_info(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def delete_user_by_email(self, email, expected_status=204):
        """
        Удаление пользователя по email.
        (Эндпоинт может отличаться! Подставь тот, который реально есть на бэке.)
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/by-email/{email}",
            expected_status=expected_status
        )