from requests import Session

from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI
from api.user_api import UserAPI
from constants import BASE_URL, BASE_URL_AUTH

class ApiManager:
    def __init__(self, session: Session):
        self.session = session
        self.auth_api = AuthAPI(self.session, BASE_URL_AUTH)
        self.user_api = UserAPI(self.session, BASE_URL_AUTH)
        self.movies_api = MoviesAPI(self.session, BASE_URL)


    def close_session(self):
        self.session.close()