import json
import logging
import os
from pydantic import BaseModel

from constant_color import RED, GREEN


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """


    def __init__(self, session, base_url, headers=None):
        """
        Инициализация кастомного реквестера.
       :param session: requests.Session для повторного использования соединений
       :param base_url: базовый URL сервиса
       :param headers: заголовки по умолчанию
        """
        self.session = session
        self.base_url = base_url
        self.base_headers = headers or {"Content-Type": "application/json"}
        self.headers = dict(self.base_headers)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
            self,
            method,
            endpoint,
            expected_status,
            data=None,
            params=None
    ):
        """Универсальный метод для отправки запросов."""
        url = f"{self.base_url}{endpoint}"

        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))

        print("=" * 80)
        print(f"[REQUEST] {method} {url}")
        if data:
            print(f"[REQUEST JSON] {data}")
        if params:
            print(f"[REQUEST PARAMS] {params}")
        print(f"[HEADERS] {self.headers}")

        response = self.session.request(
            method,
            url,
            json=data,
            params=params,
            headers=self.headers,
            verify=True
        )

        print(f"[RESPONSE STATUS] {response.status_code}")
        try:
            print(f"[RESPONSE BODY] {response.json()}")
        except Exception:
            print(f"[RESPONSE TEXT] {response.text}")
        print("=" * 80)

        self.log_request_and_response(response)

        if expected_status is not None and response.status_code != expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        return response

    def log_request_and_response(self, response, RESET=None):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(
                    f"\tRESPONSE:"
                    f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                    f"\nDATA: {RED}{response_data}{RESET}"
                )
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")

    def _update_session_headers(self, **kwargs):
        """Обновление заголовков сессии."""
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)
