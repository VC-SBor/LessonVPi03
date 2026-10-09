# Tools: продвинутые инструменты и кастомизация (VKBottle)

Локальная копия разделов документации VKBottle. Все примеры кода скопированы дословно с указанных страниц.

## VKScript (Vkscript Converter)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/vkscript/](https://vkbottle.readthedocs.io/ru/latest/tools/vkscript/)

### Зачем нужен

Просто импортируйте `vkscript` из библиотеки и напишите функцию, которая будет работать с api для того, обернув в декоратор, чтобы после ее вызова вам вернулся код выполняющий логику вашей функции, но в `VKScript`.

То есть VKScript Converter позволяет писать обычный Python-код, который затем автоматически конвертируется в код для VK API метода `execute` и выполняется на стороне ВК — так можно за один запрос выполнить цепочку действий (например, обойти несколько пользователей и отправить им сообщения).

### Пример

```python
from vkbottle import vkscript

@vkscript
def my_execute(api, user_ids=()):
    message_ids = []
    for user_id in user_ids:
        user = api.users.get(user_ids=user_id)[0]
        message_ids.append(api.messages.send(message=f"{user.first_name}, спасибо что зашел на чай", random_id=0, peer_id=user_id))
    return message_ids

# далее вызывая эту функцию вы можете использовать ее ответ в качестве кода для execute

await api.execute(code=my_execute(user_ids=[10, 11, 12]))
```

## Waiter Machine

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/waiter-machine/](https://vkbottle.readthedocs.io/ru/latest/tools/waiter-machine/)

### Зачем нужен

Waiter Machine для создания быстрых воронок без потери скоупа.

Таким образом с его помощью можно реализовать быстрые стейты и написать простейшие воронки.

В отличии от State Dispenser, состояния никуда не сериализуются, поэтому Waiter Machine не следует использовать для сложных стейтов, где важна консистентность проведения например транзакции или они активны долгое время.

### Простейший пример: ожидание следующего сообщения от пользователя

Простейший пример с waiter machine:

```python
from vkbottle.bot import Bot, Message
from vkbottle.tools import WaiterMachine

bot = Bot("...")
wm = WaiterMachine()


@bot.on.message(text="/wm")
async def greeting(message: Message):
    await message.answer("Как тебя зовут?")
    # Следующая строчка остановит выполнение хендлера,
    # и исполнение пойдет дальше только когда будет получено
    # сообщение соответствующее заданным правилам
    # (в данном случае просто от того же пользователя)
    m, _ = await wm.wait(bot.on.message_view, message)
    await message.answer(f"Привет, {m.text.capitalize()}! Будем знакомы.")


bot.run_forever()
```

### Возвращаемое значение `.wait`

Из `.wait` возвращается tuple с двумя элементами:

- Объект события которое разрешило ожидание (в примере выше, `Message`)
- Контекст который был сформирован в ходе обработки события

Поэтому его можно сразу раскрыть в две переменные.

### Правила и `default_behaviour`

В `.wait` можно так же передать правила, и `default_behaviour` как именованный аргумент.

```python
await message.answer("Напиши мне твой номер телефона")
m, ctx = await wm.wait(bot.on.message_view, message, RegexRule(PHONE_NUMBER_REGEX), default_behaviour="Неверный формат, напиши еще раз в правильном формате")
```

`default_behaviour` может принимать Callable, куда придет событие, либо любой другой объект который будет передан в return manager привязаный к активному view и обработан, в примере выше это строка, которая будет отправлена как сообщение, в соответствии с имплементацией в return manager для view сообщений ботов.

### `expiration` и `.drop`

`expiration` принимает timedelta или int (в секундах) для того чтобы ограничить время ожидания, если ивент придет позже чем start_ts + expiration, то будет вызван drop и ивент будет обработан в обычном view

Метод `.drop` используется чтобы сбросить ожидание ивента по идентификатору.

## Auth Flows (UserAuth)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/auth/](https://vkbottle.readthedocs.io/ru/latest/tools/auth/)

### Зачем нужен

Это простой инструмент для быстрого получения токена пользователя по логину и паролю.

> **Warning**
> Мы не несем ответственности за блокировку ваших аккаунтов ([см. подробнее](https://vkbottle.readthedocs.io/ru/latest/high-level/user/))

### Базовое получение токена

```python
from vkbottle import UserAuth

login = "89012345678"
password = "qwerty123"

async def main():
    token = await UserAuth().get_token(login, password)
```

По умолчанию `UserAuth` использует для входа мобильное приложение вк.
Вы можете указать другое приложение, передав `client_id` и `client_secret` в конструктор `UserAuth`.

### Права доступа (`scope`)

По умолчанию токен запрашивается с определенным списком прав доступа. Для переопределения этого списка можно в методе `get_token` использовать параметр `scope`. Список доступных прав перечислен ниже:

| Права | Описание | По умолчанию |
| --- | --- | --- |
| `UserPermission.notify` | Пользователь разрешил отправлять ему уведомления | ✗ |
| `UserPermission.friends` | Доступ к друзьям | ✓ |
| `UserPermission.photos` | Доступ к фотографиям | ✓ |
| `UserPermission.audio` | Доступ к аудиозаписям | ✗ |
| `UserPermission.video` | Доступ к видеозаписям | ✓ |
| `UserPermission.stories` | Доступ к историям | ✓ |
| `UserPermission.pages` | Доступ к wiki-страницам | ✓ |
| `UserPermission.menu` | Добавление ссылки на приложение в меню слева | ✗ |
| `UserPermission.wallmenu` | Быстрая публикация на стенах (устаревший параметр) | ✗ |
| `UserPermission.status` | Доступ к статусу пользователя | ✓ |
| `UserPermission.notes` | Доступ к заметкам пользователя | ✓ |
| `UserPermission.messages` | Доступ к расширенным методам работы с сообщениями | ✗ |
| `UserPermission.wall` | Доступ к обычным и расширенным методам работы со стеной | ✓ |
| `UserPermission.ads` | Доступ к расширенным методам работы с [рекламным API](https://dev.vk.ru/ru/api/ads/getting-started) | ✓ |
| `UserPermission.offline` | Доступ к API в любое время | ✓ |
| `UserPermission.docs` | Доступ к документам | ✓ |
| `UserPermission.groups` | Доступ к группам пользователя | ✓ |
| `UserPermission.notifications` | Доступ к оповещениям об ответах пользователю | ✓ |
| `UserPermission.stats` | Доступ к статистике групп и приложений пользователя, администратором которых он является | ✓ |
| `UserPermission.email` | Доступ к email пользователя | ✓ |
| `UserPermission.adsweb` | Доступ к кабинету рекламной сети | ✓ |
| `UserPermission.leads` | Доступ к рекламным акциям | ✗ |
| `UserPermission.exchange` | Доступ к кабинету биржы рекламы | ✓ |
| `UserPermission.market` | Доступ к товарам | ✓ |
| `UserPermission.phone_number` | Доступ к номеру телефона | ✗ |

Пример получения токена с нужными правами:

```python
from vkbottle import UserAuth, UserPermission

login = "89012345678"
password = "qwerty123"

async def main():
    token = await UserAuth().get_token(login, password, scope=[UserPermission.photos, UserPermission.video])
```

### Обработка капчи, SMS и 2FA

При получении токена может потребоваться ввод капчи, либо дополнительное подтверждение через SMS или приложение для двухфакторной аутентификации (2FA). Ниже приведен пример с обработкой ошибок при получении токена:

```python
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, cast
from urllib.parse import parse_qs, urlparse

from vkbottle import APIAuthError, AuthError, CaptchaError, UserAuth

if TYPE_CHECKING:
    from typing import Optional, Union

login = "89012345678"
password = "qwerty123"

async def main():
    user_auth = UserAuth()

    auth_code: bool | str = True
    captcha_sid: str | None = None
    captcha_key: str | None = None

    while True:
        try:
            token = await user_auth.get_token(
                login,
                password,
                auth_code=auth_code,
                captcha_sid=captcha_sid,
                captcha_key=captcha_key
            )
            break
        except CaptchaError as error:
            captcha_sid = error.captcha_sid
            captcha_key = input(f"Open url '{error.captcha_img}' in browser and enter captcha code: ")
        except APIAuthError as error:
            if error.validation_type == "2fa_sms":
                validation_sid = cast(str, error.validation_sid)
                await user_auth.validate_phone(validation_sid)
                auth_code = input("Enter code from SMS: ")
                continue

            if error.validation_type == "2fa_app":
                print(f"Enter code from 2FA app here: {error.redirect_uri}")
                oauth_url = input("Enter OAuth URL from VK after signin in: ")
                parsed_url = urlparse(url=oauth_url)
                token = parse_qs(parsed_url.fragment)["access_token"][0]
                break

            print(error.error_description)
            return
        except AuthError as error:
            print(error.error_description)
            return

    print(f"Your token: {token}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Loop Wrapper

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/loop-wrapper/](https://vkbottle.readthedocs.io/ru/latest/tools/loop-wrapper/)

### Зачем нужен

`LoopWrapper` нужен чтобы контролировать ивент луп для работы с `asyncio` и хранить основные таски, `startup` и `shutdown`, которые будут исполнены только при запуске ивент лупа через `run_forever`

### Таски

Вы можете создать таск так:

```python
from vkbottle import LoopWrapper

async def my_task():
    ...

lw = LoopWrapper()
lw.add_task(my_task())
lw.run()
```

### on_startup и on_shutdown

`on_startup` корутины запустятся перед запуском ивент лупа, `on_shutdown` при остановке. В экземпляре `LoopWrapper` они являются списками с корутинами, следовательно, добавлять их можно так:

```python
from vkbottle import LoopWrapper

async def startup_task():
    print("This is startup")

async def shutdown_task():
    print("This is shutdown")

lw = LoopWrapper()
lw.on_startup.append(startup_task())
lw.on_shutdown.append(shutdown_task())
lw.run()
```

### interval

Легкий темплейт для создания тасков с бесконечно повторяющимися действиями в интервале. Пример:

```python
from vkbottle import LoopWrapper

lw = LoopWrapper()

@lw.interval(seconds=10)
async def repeated_task():
    print("I'll print this every 10 seconds!")

lw.run()
```

### timer

Легкий темплейт для создания отложенного таска:

```python
from vkbottle import LoopWrapper

lw = LoopWrapper()

@lw.timer(seconds=10)
async def delayed_task():
    print("I'll print this after 10 seconds!")

lw.run()
```

> **Внимание**
> Если вы используете `LoopWrapper` вместе с `Bot`, то учтите, то `Bot` уже имеет свой `LoopWrapper`, который доступен по пути `bot.loop_wrapper` и запускается при вызове `bot.run_forever()`

## Кастомизация зависимостей (Dependencies customisation)

Источник: [https://vkbottle.readthedocs.io/ru/latest/modules/](https://vkbottle.readthedocs.io/ru/latest/modules/)

### Общие принципы

VKBottle автоматически выбирает лучшую альтернативу для стандартных библиотек.

Эти библиотеки не указаны в зависимостях, поэтому вы должны установить их сами.

### JSON

В порядке убывания: `orjson`, `hyperjson`, `ujson`, `json`

### Logging

В порядке убывания: `loguru`, `logging`

> **Внимание**
> Мы настоятельно рекомендуем использовать `loguru` вместо `logging`. Возможно, он станет обязательной зависимостью в будущих релизах.

> **Примечание**
> По умолчанию уровень логирования выставлен на `DEBUG`.
> Изменить это вы можете так:

Вкладка «logging»:

```python
import logging
logging.getLogger("vkbottle").setLevel(logging.INFO)
```

Вкладка «loguru», «Установить определенный уровень»:

```python
import sys
from loguru import logger
logger.remove()
logger.add(sys.stderr, level="INFO")
```

Или установить [переменную окружения](https://en.wikipedia.org/wiki/Environment_variable) `LOGURU_LEVEL`

Вкладка «loguru», «Отключить логирование полностью»:

```python
from loguru import logger
logger.disable("vkbottle")
```

Примечание: сама страница посвящена выбору оптимальных реализаций JSON-сериализатора и логирования; вопрос подмены storage и http client на этой странице не рассматривается.
