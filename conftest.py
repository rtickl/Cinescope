from faker import Faker
import pytest
import requests
from api.api_manager import ApiManager
from constants import BASE_URL_AUTH, REGISTER_ENDPOINT, ADMIN_CREDENTIALS, Roles
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from resources.user_cred import SuperAdminCreds, AdminCreds
from utils.data_generator import DataGenerator
from requests import Session
faker = Faker()

@pytest.fixture(scope="session")
def api_manager():
    """Фикстура для инициализации ApiManager с авторизацией"""
    session = Session()

    requester = CustomRequester(session=session, base_url=BASE_URL_AUTH)
    resp = requester.send_request(
        "POST",
        "/login",
        data=ADMIN_CREDENTIALS,
        expected_status=201
    )
    token = resp.json()["accessToken"]

    return ApiManager(session=session, token=token)


@pytest.fixture
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status= 201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL_AUTH)


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def movies_api(api_manager):
    """
      Фикстура для API фильмов.

      Возвращает объект MoviesAPI, созданный в ApiManager.
      """
    return api_manager.movies_api

@pytest.fixture
def movie_fixture(movies_api):
    """Фикстура: создаёт фильм перед тестом и удаляет после"""
    movie = DataGenerator.generate_movie()
    resp = movies_api.create_movie(movie)
    movie_id = resp.json()["id"]
    print(f'slfjlkjflksd {movie_id}')

    yield movie_id
    movies_api.delete_movie(movie_id, expected_status=200)

@pytest.fixture
def movie_fixture_without_deleting(movies_api):
    """Фикстура: создаёт фильм перед тестом и удаляет после"""
    movie = DataGenerator.generate_movie()
    resp = movies_api.create_movie(movie)
    movie_id = resp.json()["id"]
    print(f'slfjlkjflksd {movie_id}')

    yield movie_id

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture(scope="session")
def admin_user(user_session):
    """Возвращает пользователя с ролью ADMIN."""
    session = user_session()
    admin = User(
        AdminCreds.USERNAME,
        AdminCreds.PASSWORD,
        "[ADMIN]",
        session
    )
    admin.api.auth_api.authenticate(admin.creds)
    return admin

