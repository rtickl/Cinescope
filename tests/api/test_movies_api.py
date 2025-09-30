from utils.data_generator import DataGenerator

class TestMoviesAPI:
    """Набор тестов для проверки работы Movies API."""

    def test_create_movie(self, movies_api):
        """
        Проверка успешного создания фильма.
        """
        movie = DataGenerator.generate_movie()
        resp = movies_api.create_movie(movie)
        body = resp.json()
        assert resp.status_code == 201
        assert body["name"] == movie["name"]

    def test_get_movie_by_id(self, movies_api, movie_fixture):
        """
        Проверка получения фильма по ID.
        """
        resp = movies_api.get_movie_by_id(movie_fixture)
        body = resp.json()
        assert resp.status_code == 200
        assert body["id"] == movie_fixture

    def test_update_movie(self, movies_api, movie_fixture):
        """
        Проверка обновления информации о фильме.
        """
        update_data = {"price": 555}
        resp = movies_api.update_movie(movie_fixture, update_data)
        body = resp.json()
        assert resp.status_code == 200
        assert body["price"] == 555

    def test_delete_movie(self, movies_api, movie_fixture_without_deleting):
        """
        Проверка удаления фильма по ID.
        """
        resp = movies_api.delete_movie(movie_fixture_without_deleting)
        assert resp.status_code == 200

        resp = movies_api.get_movie_by_id(movie_fixture_without_deleting, expected_status=404)
        assert resp.status_code == 404

    def test_filter_movies(self, movies_api):
        """
        Проверка фильтрации фильмов.
        """
        resp = movies_api.get_movies(params={"locations": ["MSK"], "minPrice": 100})
        body = resp.json()
        assert resp.status_code == 200
        assert "movies" in body
        assert all(movie["location"] == "MSK" for movie in body["movies"])

    def test_create_movie_without_required_field(self, movies_api):
        """
        Проверка ошибки при создании фильма без обязательного поля.
        """
        movie = DataGenerator.generate_movie()
        del movie["name"]
        resp = movies_api.create_movie(movie, expected_status=400)
        assert resp.status_code == 400

    def test_get_movie_invalid_id(self, movies_api):
        """
        Проверка ошибки при запросе фильма с несуществующим ID.
        """
        resp = movies_api.get_movie_by_id(999999, expected_status=404)
        assert resp.status_code == 404
