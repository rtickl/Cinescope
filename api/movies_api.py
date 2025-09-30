from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    """Класс для работы с API фильмов."""

    def __init__(self, session, base_url, headers=None):
        super().__init__(session=session, base_url=base_url, headers=headers)

    def get_movies(self, params=None, expected_status=200):
        """
        Получить список фильмов с фильтрацией.

        :param params: query-параметры (например, {"locations": ["MSK"], "minPrice": 100})
        :param expected_status: ожидаемый HTTP-статус
        :return: объект Response
        """
        return self.send_request("GET", "movies", params=params, expected_status=expected_status)

    def get_movie_by_id(self, movie_id: int, expected_status=200):
        """
        Получить фильм по ID.

        :param movie_id: ID фильма
        :param expected_status: ожидаемый HTTP-статус
        :return: объект Response
        """
        return self.send_request("GET", f"movies/{movie_id}", expected_status=expected_status)

    def create_movie(self, data: dict, expected_status=201):
        """
        Создать новый фильм.

        :param data: тело запроса (dict)
        :param expected_status: ожидаемый HTTP-статус (по умолчанию 201)
        :return: объект Response
        """
        return self.send_request("POST", "movies", data=data, expected_status=expected_status)

    def update_movie(self, movie_id: int, data: dict, expected_status=200):
        """
        Обновить фильм.

        :param movie_id: ID фильма
        :param data: тело запроса (dict)
        :param expected_status: ожидаемый HTTP-статус
        :return: объект Response
        """
        return self.send_request("PATCH", f"movies/{movie_id}", data=data, expected_status=expected_status)

    def delete_movie(self, movie_id: int, expected_status=200):
        """
        Удалить фильм.

        :param movie_id: ID фильма
        :param expected_status: ожидаемый HTTP-статус
        :return: объект Response
        """
        return self.send_request("DELETE", f"movies/{movie_id}", expected_status=expected_status)
