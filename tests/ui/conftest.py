from faker import Faker
import pytest
import requests
from api.api_manager import ApiManager
from constants import Roles
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from entities.user import User
from models.base_models import UserModel
from utils.data_generator import DataGenerator
from requests import Session
faker = Faker()
from resources.user_cred import SuperAdminCreds

@pytest.fixture(scope="session")
def api_manager():
    """Возвращает неавторизованный ApiManager с общей сессией."""
    session = requests.Session()
    return ApiManager(session)

@pytest.fixture
def test_user() -> UserModel:
    """Генерация случайного пользователя для тестов (Pydantic-модель)."""
    random_password = DataGenerator.generate_random_password()
    return UserModel(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )
@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    """
    Регистрация пользователя через ApiManager (без отдельного requester).
    Возвращает словарь user c присвоенным id.
    """
    resp = api_manager.auth_api.register_user(user_data=test_user, expected_status=201)
    user_id = resp.json()["id"]
    return test_user.model_copy(update={"id": user_id})

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def movies(movies_api):
    """Упрощённая фикстура: возвращает только MoviesAPI."""
    return movies_api.movies_api


@pytest.fixture(scope="session")
def movies_api():
    """Фикстура: возвращает ApiManager с авторизованной сессией под SUPER_ADMIN."""
    from api.api_manager import ApiManager
    from constants import ADMIN_CREDENTIALS
    from requests import Session

    session = Session()
    api_manager = ApiManager(session)
    creds = (ADMIN_CREDENTIALS["email"], ADMIN_CREDENTIALS["password"])
    api_manager.auth_api.authenticate(creds)
    return api_manager

@pytest.fixture
def create_movie(super_admin):
    """
    Создаёт фильм перед тестом и удаляет после (с авторизацией).
    """
    movie_data = DataGenerator.generate_movie()
    resp = super_admin.api.movies_api.create_movie(movie_data, expected_status=201)
    movie_id = resp.json()["id"]
    yield movie_id
    super_admin.api.movies_api.delete_movie(movie_id, expected_status=200)

@pytest.fixture
def movie_fixture_without_deleting(movies_api):
    """Фикстура: создаёт фильм перед тестом и удаляет после"""
    movie = DataGenerator.generate_movie()
    resp = movies_api.movies_api.create_movie(movie)
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
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: UserModel) -> UserModel:
    updated = test_user.model_copy(update={
        "verified": True,
        "banned": False
    })
    return updated

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    """Создаёт обычного пользователя через супер-админа и авторизует его."""
    new_session = user_session()
    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session
    )

    user_data = creation_user_data.model_copy(update={"verified": True, "banned": False})
    super_admin.api.user_api.create_user(user_data, expected_status=201)

    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture(scope="session")
def admin_session():
    """
    Фикстура: создаёт пул админских сессий ApiManager.
    """
    admin_pool = []

    def _create_admin_session():
        session = requests.Session()
        admin_manager = ApiManager(session)
        admin_pool.append(admin_manager)
        return admin_manager

    yield _create_admin_session

    for admin in admin_pool:
        admin.close_session()

@pytest.fixture
def admin_user(admin_session, super_admin, creation_user_data):
    """
        Фикстура: создаёт пользователя с ролью ADMIN через SuperAdmin и авторизует его.
    """
    new_session = admin_session() if callable(admin_session) else admin_session

    admin_data = creation_user_data.model_copy(update={"roles": [Roles.ADMIN.value]})
    super_admin.api.user_api.create_user(admin_data, expected_status=201)
    admin = User(
        admin_data.email,
        admin_data.password,
        admin_data.roles,
        new_session
    )
    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture
def registration_user_data() -> UserModel:
    """
        Фикстура: генерирует данные для регистрации нового пользователя.
    """
    random_password = DataGenerator.generate_random_password()
    return UserModel(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
        Фикстура, которая создает и возвращает сессию для работы с базой данных
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
        Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())

    yield user

    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)