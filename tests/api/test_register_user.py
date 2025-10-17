from api.api_manager import ApiManager
from models.base_models import UserModel, RegisterUserResponse
from utils.data_generator import DataGenerator
from constants import Roles

def test_register_user(api_manager: ApiManager):
    """
        Проверка успешной регистрации нового пользователя.
    """

    pwd = DataGenerator.generate_random_password()
    model = UserModel(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=pwd,
        passwordRepeat=pwd,
        roles=[Roles.USER.value]
    )
    response = api_manager.auth_api.register_user(user_data=model, expected_status=201)
    dto = RegisterUserResponse(**response.json())
    assert dto.email == model.email, "Email не совпадает"
