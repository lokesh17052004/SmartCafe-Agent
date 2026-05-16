import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_name = os.getenv("DB_NAME", "bean_brew_db")
        self.db_username = os.getenv("DB_USERNAME", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "Admin123")

settings = Settings()