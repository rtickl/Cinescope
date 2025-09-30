from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI
from api.user_api import UserAPI


from constants import BASE_URL, BASE_URL_AUTH


class ApiManager:
    def __init__(self, session, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.session = session
        self.headers = headers
        self.auth_api = AuthAPI(session, BASE_URL_AUTH)
        self.user_api = UserAPI(session, BASE_URL_AUTH)
        self.movies_api = MoviesAPI(session=self.session, base_url=BASE_URL, headers=self.headers)
