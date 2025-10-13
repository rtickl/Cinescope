import psycopg2
import logging

from constant_color import RESET, GREEN, RED
from resources.db_creds import MoviesDbCreds



class DBClient:
    """Клиент для подключения к PostgreSQL в стиле логирования Cinescope."""

    def __init__(self):
        self.conn = None
        self.logger = logging.getLogger(__name__)

        # Подключаем креды в UPPERCASE стиле
        self.host = MoviesDbCreds.HOST
        self.port = MoviesDbCreds.PORT
        self.database = MoviesDbCreds.DATABASE_NAME
        self.user = MoviesDbCreds.USERNAME
        self.password = MoviesDbCreds.PASSWORD

    def connect(self):
        """Устанавливает соединение с БД и выводит информацию о сервере."""
        try:
            print("=" * 80)
            print(
                f"{GREEN}Connecting to PostgreSQL...{RESET}\n"
                f"curl 'postgresql://{self.user}:*****@{self.host}:{self.port}/{self.database}'"
            )

            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password
            )

            cur = self.conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]

            self.logger.info(
                f"{GREEN}✅ Connected successfully!{RESET}\n"
                f"PostgreSQL version: {version}"
            )
            print(f"{GREEN}✅ Connected successfully! PostgreSQL version:{RESET} {version}")
            cur.close()

        except Exception as e:
            self.logger.error(f"{RED}❌ Database connection failed:{RESET} {e}")
            print(f"{RED}❌ Ошибка подключения: {e}{RESET}")

    def get_table_count(self):
        """Возвращает количество таблиц в текущей схеме."""
        try:
            if not self.conn:
                self.connect()

            cur = self.conn.cursor()
            cur.execute(
                "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
            )
            count = cur.fetchone()[0]
            print(f"📊 Количество таблиц в public: {count}")
            return count
        except Exception as e:
            self.logger.error(f"{RED}Ошибка при выполнении запроса:{RESET} {e}")
        finally:
            if self.conn:
                cur.close()

    def close(self):
        """Закрывает соединение."""
        if self.conn:
            self.conn.close()
            print(f"{GREEN}🔒 Соединение закрыто.{RESET}")


if __name__ == "__main__":
    db_client = DBClient()
    db_client.connect()
    db_client.get_table_count()
    db_client.close()
