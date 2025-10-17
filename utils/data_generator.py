import random
import string

from datetime import datetime
import uuid

from faker import Faker
faker = Faker()

class DataGenerator:
    """ Класс для генерации тестовых данных."""

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def random_string(length=8):
        """
            Генерация случайной строки из латинских букв.
        """
        return ''.join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def generate_movie():
        """
            Генерация данных для создания фильма.
        """

        return {
            "name": f"Movie_{DataGenerator.random_string()}",
            "description": f"Description_{DataGenerator.random_string(15)}",
            "price": random.randint(100, 1000),
            "location": random.choice(["MSK", "SPB"]),
            "published": True,
            "genreId": 1
        }

    @staticmethod
    def generate_user_data():
        """
            Генерирует корректные данные пользователя
        """
        return {
            "id": str(uuid.uuid4()),
            "email": faker.email(),
            "fullName": faker.name(),
            "password": faker.password(length=10),
            "passwordRepeat": None,
            "verified": False,
            "banned": False,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
        }

    @staticmethod
    def generate_random_int(length: int = 5) -> int:
        """
            Генерирует случайное целое число с заданным количеством цифр.
        """
        start = 10 ** (length - 1)
        end = (10 ** length) - 1
        return random.randint(start, end)
