import pytest
from sqlalchemy import create_engine, text
from resources.db_creds import MoviesDbCreds
from utils.data_generator import DataGenerator


class TestMoviesDB:
    def setup_method(self):
        # Настраиваем подключение к PostgreSQL через SQLAlchemy
        self.engine = create_engine(
            f"postgresql://{MoviesDbCreds.USERNAME}:{MoviesDbCreds.PASSWORD}@{MoviesDbCreds.HOST}:{MoviesDbCreds.PORT}/{MoviesDbCreds.DATABASE_NAME}"
        )

    def test_movie_creation_and_deletion_reflects_in_db(self, super_admin):
        """Проверяет, что фильм создаётся и удаляется корректно в БД."""

        # 1️⃣ Создаём фильм через API с помощью super_admin
        movie_data = DataGenerator.generate_movie()
        response = super_admin.api.movies_api.create_movie(movie_data)
        movie_id = response.json()["id"]

        # 2️⃣ Проверяем, что фильм появился в БД
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT name, price, location FROM movies WHERE id = :id"),
                {"id": movie_id},
            ).fetchone()
            assert result is not None, "❌ Фильм не найден в БД после создания"
            print(f"✅ Фильм найден в БД: {result}")

        # 3️⃣ Удаляем фильм через API
        super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)

        # 4️⃣ Проверяем, что запись удалена из БД
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT id FROM movies WHERE id = :id"),
                {"id": movie_id},
            ).fetchone()
            assert result is None, "❌ Фильм всё ещё существует в БД после удаления"
            print(f"✅ Фильм успешно удалён из БД: {movie_id}")
