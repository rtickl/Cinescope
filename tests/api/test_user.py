from models.base_models import UserModel
from resources.user_cred import SuperAdminCreds


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        """
            Проверка получения данных супер-админа по его логину.
        """
        response = super_admin.api.user_api.get_user(SuperAdminCreds.USERNAME).json()

        assert response["email"] == SuperAdminCreds.USERNAME
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """
            Проверка получения данных супер-админа по его ID и email.
        """
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_email.get('email') == creation_user_data.email
        assert response_by_id.get('fullName') == creation_user_data.fullName
        assert response_by_id.get('roles', []) == creation_user_data.roles
        assert response_by_id.get('verified') is True

    def test_super_admin_can_create_user(self, super_admin, creation_user_data: UserModel):
        """
            Проверка, что SUPER_ADMIN может создать нового пользователя.
        """
        resp = super_admin.api.user_api.create_user(creation_user_data, expected_status=201)
        created_id = resp.json()["id"]
        get_resp = super_admin.api.user_api.get_user(created_id, expected_status=200)

        assert get_resp.json()["email"] == creation_user_data.email

        super_admin.api.user_api.delete_user(created_id, expected_status=200)

