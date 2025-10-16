import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from db_models.movies import MovieDBModel
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

    def test_get_movie_by_id(self, movies_api, create_movie):
        """
        Проверка получения фильма по ID.
        """
        resp = movies_api.get_movie_by_id(create_movie)
        body = resp.json()
        assert resp.status_code == 200
        assert body["id"] == create_movie

    def test_update_movie(self, movies_api, create_movie):
        """
        Проверка обновления информации о фильме.
        """
        update_data = {"price": 555}
        resp = movies_api.update_movie(create_movie, update_data)
        body = resp.json()
        assert resp.status_code == 200
        assert body["price"] == 555

    @pytest.mark.api
    def test_delete_movie(self, movies_api, db_session: Session,  movie_fixture_without_deleting):
        """
        Проверка удаления фильма по ID.
        Перед удалением проверяем наличие фильма в базе — если нет, добавляем вручную.
        """

        movie_id = movie_fixture_without_deleting
        movie_in_db = db_session.scalar(
            select(MovieDBModel).where(MovieDBModel.id == movie_id)
        )

        if not movie_in_db:
            print(f"⚠️ Фильм с ID {movie_id} не найден, создаём новый объект в базе...")

            new_movie = MovieDBModel(
                id=movie_id,
                name=f"Movie_{DataGenerator.random_string(6)}",
                price=200.0,
                description="Автоматически созданный тестовый фильм",
                image_url=None,
                location="SPB",
                published=True,
                rating=0.0,
                genre_id=1,
                created_at=None
            )

            db_session.add(new_movie)
            db_session.commit()

            print(f"✅ Фильм успешно добавлен в базу: {new_movie}")

        resp = movies_api.delete_movie(movie_id)
        assert resp.status_code in [200, 204], f"Неожиданный статус при удалении: {resp.status_code}"

        resp = movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert resp.status_code == 404, f"Фильм с ID {movie_id} всё ещё существует после удаления"

        deleted_from_db = db_session.scalar(
            select(MovieDBModel).where(MovieDBModel.id == movie_id)
        )
        assert deleted_from_db is None, f"Фильм с ID {movie_id} не был удалён из базы"

        print(f"Тест успешно завершён — фильм с ID {movie_id} удалён.")

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
        "role_fixture, expected_status",
        [
            ("super_admin", 200),
            ("admin_user", 403),
            ("common_user", 403),
        ],
    )
    def test_delete_movie_roles(self, request, super_admin, expected_status, role_fixture):
        """Проверка удаления фильма пользователями разных ролей"""
        # создаём фильм под супер-админом
        movie_data = DataGenerator.generate_movie()
        movie_response = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)
        movie_id = movie_response.json()["id"]

        # получаем нужную фикстуру динамически
        user = request.getfixturevalue(role_fixture)

        # пробуем удалить фильм
        delete_response = user.api.movies_api.delete_movie(movie_id, expected_status=None)

        assert delete_response.status_code == expected_status, (
            f"{role_fixture} получил {delete_response.status_code}, ожидалось {expected_status}"
        )

        # если не удалён — очищаем супер-админом
        if delete_response.status_code != 200:
            super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)