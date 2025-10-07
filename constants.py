from enum import Enum

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "login"
REGISTER_ENDPOINT = "register"

ADMIN_CREDENTIALS = {
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
}

BASE_URL_AUTH = "https://auth.dev-cinescope.coconutqa.ru/"
BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"