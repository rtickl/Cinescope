import logging


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
        self.headers = headers or {"Content-Type": "application/json"}

        if headers is None:
            self.headers = {"Content-Type": "application/json"}
        elif isinstance(headers, dict):
            self.headers = headers
        else:
            raise TypeError("headers must be dict or None")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
        self,
        method,
        endpoint,
        expected_status=200,
        data = None,
        params = None
    ):
        """
        Универсальный метод для отправки запросов.
        :param method: HTTP метод (GET, POST, PUT, DELETE и т.д.).
        :param endpoint: Эндпоинт (например, "/login").
        :param data: Тело запроса (JSON-данные).
        :param expected_status: Ожидаемый статус-код (по умолчанию 200).
        :param params: Параметры (по умолчанию None).
        :return: Объект ответа requests.Response.
        """
        url = f"{self.base_url}{endpoint}"

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

        if expected_status is not None and response.status_code != expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        return response

    def log_request_and_response(self, response):
        """Простое логирование запроса и ответа."""
        req = response.request
        print("\n===== REQUEST =====")
        print(req.method, req.url)
        print("Headers:", dict(req.headers))
        print("Body:", req.body)
        print("\n===== RESPONSE =====")
        print("Status:", response.status_code)
        print("Body:", response.text[:500])