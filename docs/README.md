# Документация VKBottle (локальная копия)

Локальная копия ключевых разделов документации [VKBottle](https://vkbottle.readthedocs.io/ru/latest/) — Python-фреймворка для создания ботов ВКонтакте.

- Источник: <https://vkbottle.readthedocs.io/ru/latest/> (версия `ru/latest`)
- Все примеры кода в файлах скопированы **дословно** со страниц-источников (ничего не придумано); у каждого раздела указан URL страницы-источника.
- Назначение: опираться на эти файлы при разработке бота, не обращаясь каждый раз к сайту.

## Файлы

| Файл | Что внутри | Страницы-источники |
|---|---|---|
| [01-tutorial.md](01-tutorial.md) | Туториал: первый бот, правила, разделение кода, клавиатуры и вложения, мидлвари и return-менеджеры, обработка ошибок, FAQ | `tutorial/` (8 страниц) |
| [02-high-level-bot.md](02-high-level-bot.md) | Интерфейс `Bot` (атрибуты, `run_polling`/`run_forever`), `User` (юзербот), `BotLabeler`, мультибот `run_multibot` | `high-level/`, `high-level/bot/`, `user/`, `bot/labeler/`, `bot/multibot/` |
| [03-handling.md](03-handling.md) | Хендлинг: Handler, Router, View, Return Manager, State Dispenser, Middleware, Rules + все встроенные правила (23 шт. с сигнатурами и примерами) | `high-level/handling/*` (7 страниц), `high-level/builtin-rules/` |
| [04-low-level-api.md](04-low-level-api.md) | Работа с API (`API`, снейк-кейс, captcha), лимиты ВК и обход rate limit, валидаторы, token generator, HTTP-клиент, `ErrorHandler`, `CodeException` | `low-level/` (9 страниц) |
| [05-longpoll-polling.md](05-longpoll-polling.md) | **Long Poll API**: `Polling`/`ABCPolling`, методы `get_server`/`get_event`/`listen`/`construct`, параметры `BotPolling`, запуск `bot.run_polling()`/`bot.run_forever()`, кастомный поллинг, мультибот | `low-level/polling/`, `high-level/bot/`, `high-level/bot/multibot/`, `tutorial/first-bot/` |
| [06-callback-api.md](06-callback-api.md) | Callback API (вебхуки): `BotCallback`, secret key, confirmation, подключение через веб-сервер (`aiohttp`/`flask`/`fastapi`), `bot.process_event(event)` | `low-level/callback/`, `tutorial/callback-bot/` |
| [07-tools-core.md](07-tools-core.md) | Базовые инструменты: `Keyboard` и кнопки, аплоадеры файлов, форматирование текста, шаблоны, message event (callback-кнопки), storage (`CtxStorage`) | `tools/` (7 страниц) |
| [08-tools-advanced.md](08-tools-advanced.md) | Продвинутые инструменты: `@vkscript`, Waiter Machine, Auth Flows (получение user-токена), Loop Wrapper, кастомизация зависимостей (JSON/логирование) | `tools/vkscript/`, `waiter-machine/`, `auth/`, `loop-wrapper/`, `modules/` |

## Рекомендуемый порядок изучения

1. **[01-tutorial.md](01-tutorial.md)** — базовый: как создать бота, хендлеры, правила, клавиатуры.
2. **[05-longpoll-polling.md](05-longpoll-polling.md)** — как работает и запускается Long Poll (обязательно перед настройкой).
3. **[02-high-level-bot.md](02-high-level-bot.md)** и **[03-handling.md](03-handling.md)** — интерфейс бота и вся система обработки событий.
4. **[04-low-level-api.md](04-low-level-api.md)** — работа с API, лимиты и ошибки.
5. **[07-tools-core.md](07-tools-core.md)** / **[08-tools-advanced.md](08-tools-advanced.md)** — клавиатуры, вложения, хранилища и прочее.
6. **[06-callback-api.md](06-callback-api.md)** — если нужен Callback API вместо Long Poll.

## Быстрая шпаргалка (из примеров сайта)

```python
from vkbottle.bot import Bot, Message

bot = Bot(token="token")

@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}".format(users_info[0].first_name))

bot.run_forever()
```

- `@bot.on.message` — и из бесед, и из личных; `@bot.on.private_message` — только личные; `@bot.on.chat_message` — только беседы.
- Все методы API пишутся **снейк-кейсом**: `api.messages.get_by_id(...)` вместо `messages.getById`.
- Декоратор хендлера: `bot.on` — это `bot.labeler`.
- Запуск: `bot.run_forever()` (синхронный) или `await bot.run_polling()` (асинхронный).
- Стабильная версия API для лонгпола — `5.131`; не забудьте галочки в настройках лонгпола сообщества (нужные события, в т.ч. новые сообщения).

## Не покрыто (при необходимости — дособрать со сайта)

- Раздел «Что нового» (`whats_new/4.0` … `4.3`).
- Страница `tutorial/recommended-ide/` (рекомендуемые IDE).
- Страница `high-level/handling/blueprint` отсутствует в навигации `ru/latest`; `Blueprint` упоминается в `02-high-level-bot.md`.
