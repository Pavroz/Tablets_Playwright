# Файл нужен для создания переменных из секретов в env

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")

config = Config()

# Альтернативный вариант с проверкой
# load_dotenv()
#
# def _require(value: str | None, name: str) -> str:
#     if not value:
#         raise RuntimeError(f"Missing required env var: {name}")
#     return value
#
#
# class Config:
#     LOGIN = _require(os.getenv("LOGIN"), "LOGIN")
#     PASSWORD = _require(os.getenv("PASSWORD"), "PASSWORD")
#
# config = Config()