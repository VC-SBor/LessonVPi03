"""Клиент текстовой генерации ProxyAPI для бота.

По документации ProxyAPI (https://proxyapi.ru/docs/openai-text-generation):
- запрос: POST {base_url}/chat/completions с заголовком Authorization: Bearer <ключ>;
- тело: {"model": ..., "messages": [{"role": ..., "content": ...}, ...]};
- ответ: текст лежит в choices[0].message.content;
- модель не помнит переписку между запросами, поэтому всю историю
  нужно отправлять заново — с ролью "assistant" у своих прошлых ответов.
"""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp


class AIError(RuntimeError):
    """Не удалось получить ответ от ProxyAPI."""


class AIBillingError(AIError):
    """На балансе ProxyAPI не хватает денег (HTTP 402).

    Само по себе не лечится перезапуском — нужно пополнить баланс,
    поэтому обрабатывается отдельно от остальных ошибок.
    """


class ProxyAIClient:
    """HTTP-клиент к ProxyAPI + история диалогов по каждому peer_id."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        system_prompt: str,
        history_limit: int = 10,
        timeout: float = 60.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._system_prompt = system_prompt
        # history_limit — сколько пар реплик (user + assistant) помнит диалог
        self._history_limit = max(history_limit, 1)
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: aiohttp.ClientSession | None = None
        self._history: dict[int, list[dict[str, str]]] = {}

    async def ask(self, peer_id: int, text: str) -> str:
        """Возвращает ответ модели на `text` в контексте диалога `peer_id`.

        История пополняется только после успешного ответа, чтобы при ошибке
        не ломать согласованность ролей user/assistant.
        """
        history = self._history.setdefault(peer_id, [])
        messages: list[dict[str, str]] = [
            {"role": "system", "content": self._system_prompt},
            *history,
            {"role": "user", "content": text},
        ]

        content = await self._chat(messages)

        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": content})

        # отбрасываем самые старые пары, держим не больше history_limit пар
        excess = len(history) - 2 * self._history_limit
        if excess > 0:
            del history[:excess]

        return content

    def clear_history(self, peer_id: int) -> None:
        """Забывает историю диалога (полезно для отладки)."""
        self._history.pop(peer_id, None)

    async def close(self) -> None:
        """Закрывает HTTP-сессию (регистрируется в bot.on_shutdown)."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    async def _chat(self, messages: list[dict[str, str]]) -> str:
        url = f"{self._base_url}/chat/completions"
        payload = {"model": self._model, "messages": messages}
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        session = await self._get_session()
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    body = (await response.text())[:300]
                    message = f"POST {url} → HTTP {response.status}: {body}"
                    if response.status == 402:
                        raise AIBillingError(message)
                    raise AIError(message)
                data = await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as error:
            raise AIError(f"POST {url} → ошибка соединения: {error}") from error

        return self._extract(data)

    @staticmethod
    def _extract(data: Any) -> str:
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            msg = f"Неожиданный формат ответа ProxyAPI: {data!r:.300}"
            raise AIError(msg) from error
        if not isinstance(content, str) or not content.strip():
            raise AIError("ProxyAPI вернул пустой ответ")
        return content.strip()
