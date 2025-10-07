import pytest

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

    def test_create_movie_without_required_field(self, super_admin):
        """
        Проверка ошибки при создании фильма без обязательного поля.
        """
        movie = DataGenerator.generate_movie()
        response = super_admin.api.movies_api.create_movie(movie, expected_status=201)

        body = response.json()
        assert body["name"] == movie["name"]
        assert response.status_code == 201


    def test_get_movie_invalid_id(self, movies_api):
        """
        Проверка ошибки при запросе фильма с несуществующим ID.
        """
        resp = movies_api.get_movie_by_id(999999, expected_status=404)
        assert resp.status_code == 404

    def test_get_movies_list_as_super_admin(self, super_admin):

        response = super_admin.api.movies_api.get_movies(expected_status=200)
        assert response.status_code == 200

    def test_user_cannot_create_movie(self, common_user):

        movie = DataGenerator.generate_movie()

        response = common_user.api.movies_api.create_movie(movie, expected_status=403)

        assert response.status_code == 403, f"Должен получить 403, но получил {response.status_code}"

    @pytest.mark.parametrize(
        "params",
        [
            {"minPrice": 1, "maxPrice": 500, "locations": ["MSK"], "genreId": 1},
            {"minPrice": 100, "maxPrice": 1000, "locations": ["SPB"], "genreId": 2},
            {"minPrice": 10, "maxPrice": 200, "locations": ["MSK", "SPB"], "genreId": 3},
        ],
        ids=["msk_cheap_genre1", "spb_expensive_genre2", "both_cities_mid_genre3"]
    )
    def test_get_movies_filtered(self, movies_api, params):
        """Проверка фильтрации фильмов по диапазону цен, локациям и жанру"""
        response = movies_api.get_movies(params=params)
        response_data = response.json()

        movies = response_data.get("movies", [])
        assert isinstance(movies, list), "Поле 'movies' должно содержать список фильмов"
        assert len(movies) > 0, "Ответ не должен быть пустым"

        for movie in movies:
            price = movie.get("price")
            location = movie.get("location")
            genre_id = movie.get("genreId")
            assert params["minPrice"] <= price <= params["maxPrice"], (
                f"Фильм '{movie.get('name')}' имеет цену вне диапазона: {price}"
            )
            assert location in params["locations"], (
                f"Фильм '{movie.get('name')}' имеет неподходящую локацию: {location}"
            )
            assert genre_id == params["genreId"], (
                f"Фильм '{movie.get('name')}' имеет жанр {genre_id}, ожидался {params['genreId']}"
            )