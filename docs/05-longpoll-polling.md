# Long Poll API (Polling) — VKBottle

Документ собран со страниц:
- <https://vkbottle.readthedocs.io/ru/latest/low-level/polling/> (основная страница Polling)
- <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/> (запуск longpoll у `Bot`)
- <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/multibot/> (запуск нескольких лонгполов)
- <https://vkbottle.readthedocs.io/ru/latest/tutorial/first-bot/> (пример запуска и настройки лонгпола)

> **Ключевая мысль:** библиотека использует `Polling`, чтобы реализовывать longpoll. Для ботов и юзеров создан соответствующий поллинг (так как они разные). Вы можете написать свой поллинг, базируясь на абстрактном `ABCPolling`.

## Интерфейс поллинга (low-level)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/polling/>

### `get_server`

Получает сервер для поллинга и возвращает его.

### `get_event`

Получает сервер из `get_server` в параметр и делает долгий POST реквест.

### `listen`

Асинхронный итератор (будет использован с `async with`). Генерирует приходящие ивенты.

### `construct`

Принимает API, нужно для того чтобы конструировать поллинг с обновленным API при каждом вызове. Возвращает собственный инстанс, может быть использован в билдер интерфейсе.

### Стандартные параметры для BotPolling / UserPolling

- **api** — если не указано будет получено в `listen`
- **group_id** / **user_id** — если не указано будет получено в `listen`
- **wait** — лимит секунд после которого вк будет принудительно возвращает ответ на долгий реквест (даже если нет обновлений)
- **rps_delay** — если не указано задержка равна 0

### Создание кастомного клиента

Кастомный поллинг должен унаследовать `ABCPolling` и имплементировать вышеупомянутые методы.

## Запуск Long Poll API у Bot

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/>

Инстанс бота состоит из стандартного апи, лонгпола и других частей фреймворка. Поллинг доступен как атрибут **`bot.polling`** — [Polling документация](https://vkbottle.readthedocs.io/ru/latest/low-level/polling/).

### `bot.run_polling()`

Асинхронный запуск longpoll.

### `bot.run_forever()`

Синхронный запуск longpoll. Добавляет `run_polling` в таски `bot.loop_wrapper` и вызывает `bot.loop_wrapper.run()`.

## Пример: полный бот на Long Poll

Источник: <https://vkbottle.readthedocs.io/ru/latest/tutorial/first-bot/> (пример дословно)

Чтобы начать работу с ботом, требуется импортировать класс `Bot` из корня проекта (`vkbottle`) или из специализированного пакета (`vkbottle.bot`):

```python
from vkbottle.bot import Bot
```

Для инициализации бота обязателен аргумент — `token` *или* `api`. `token` нужен для сокращения кода: если вы передадите `token`, будет создан `API` с соответствующим генератором токена. Если вы передадите `api`, он и будет использоваться для бота:

```python
# Инициализация токеном
bot = Bot(token="token")
# (или) Инициализация с апи
bot = Bot(api=api)
```

Полный пример бота с запуском лонгпола:

```python
from vkbottle.bot import Bot, Message

bot = Bot(token="token")

@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}".format(users_info[0].first_name))

bot.run_forever()
```

Разбор запуска из туториала (дословно):

> `bot.run_forever()` - помогает асинхронно запустить бота из синхронной среды, если бы была создана асинхронная, вы бы могли использовать `await run_polling()`

> Если представленный код не работает, проверьте поставили ли вы галочки в настройках лонгпола на нужные события (в данном случае на новые сообщения) и сам лонгпол (стабильна версия `5.131`)

> **Примечание**
>
> Если вы не хотите использовать простые (high-level) инструменты для разработки бота вы можете использовать low-level [Polling](https://vkbottle.readthedocs.io/ru/latest/low-level/polling/), или самостоятельно написать всю логику на запросах к api как показано в разделе выше

## Несколько лонгполов (Multibot)

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/multibot/>

Мультибот запускает несколько лонгполов на переданных вами API и обрабатывает получаемые ивенты со всех лонгполов с помощью одного основного бота. Эта идея встречается например в чат-менеджере с их субменеджерами и может быть использована в разных целях.

Для запуска такого бота вам понадобится `run_multibot`, он добавляет `run_polling` в таски и запускает `eventloop`. Его можно импортировать из `vkbottle.bot`:

```python
run_multibot(bot, apis, polling_type=BotPolling)
```

Основному боту передавать токен для создания API не нужно.

- `apis` — любой итерируемый объект (то есть можно легко сделать свой генератор при желании)
- `polling_type` — если вы кастомизируете поллинг вы можете изменить это значение

Пример мультибота можно увидеть [здесь](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/multibot.py).

## Связанные разделы нашей документации

- Про запуск бота и атрибуты: [02-high-level-bot.md](02-high-level-bot.md)
- Ошибки при работе с API: [04-low-level-api.md](04-low-level-api.md)
- Альтернатива Long Poll — Callback API (вебхуки): [06-callback-api.md](06-callback-api.md)
- Настройки логирования и цикла (Loop Wrapper): [08-tools-advanced.md](08-tools-advanced.md)
