"""Настройки бота: чтение ключей из .env через python-dotenv."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_SYSTEM_PROMPT = (
    "Ты — дружелюбный помощник в ВКонтакте. Отвечай на языке собеседника, "
    "коротко и по существу. Если тебя просят о чём-то запрещённом или "
    "опасном — вежливо откажись."
)


class ConfigError(RuntimeError):
    """Обязательная настройка из .env отсутствует или некорректна."""


@dataclass(frozen=True)
class Settings:
    """Все настройки бота, полученные из окружения."""

    vk_token: str
    proxyapi_key: str
    ai_model: str
    ai_base_url: str
    ai_system_prompt: str
    ai_history_limit: int


def _read(name: str, *, default: str | None = None) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        if default is not None:
            return default
        raise ConfigError(
            f"Не задана переменная {name}. Заполните файл {BASE_DIR / '.env'} "
            f"(образец — .env.example) и перезапустите бота."
        )
    return value.strip()


def _read_int(name: str, *, default: int) -> int:
    raw = _read(name, default=str(default))
    try:
        return int(raw)
    except ValueError as error:
        msg = f"Переменная {name} должна быть целым числом, получено: {raw!r}"
        raise ConfigError(msg) from error


def load_settings() -> Settings:
    """Загружает .env и возвращает типизированные настройки.

    Уже заданные переменные окружения имеют приоритет над .env
    (так работает load_dotenv), поэтому бот можно запускать и через env.
    """
    load_dotenv(BASE_DIR / ".env")

    history_limit = _read_int("AI_HISTORY_LIMIT", default=10)
    if history_limit < 1:
        raise ConfigError("AI_HISTORY_LIMIT должен быть не меньше 1")

    return Settings(
        vk_token=_read("VK_TOKEN"),
        proxyapi_key=_read("PROXYAPI_KEY"),
        ai_model=_read("AI_MODEL", default="gpt-4.1-mini"),
        ai_base_url=_read("AI_BASE_URL", default="https://api.proxyapi.ru/v1"),
        ai_system_prompt=_read("AI_SYSTEM_PROMPT", default=DEFAULT_SYSTEM_PROMPT),
        ai_history_limit=history_limit,
    )
