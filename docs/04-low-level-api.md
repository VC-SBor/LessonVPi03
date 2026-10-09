# Low-level: работа с API и обработка ошибок (VKBottle)

Локальная копия документации VKBottle по разделу «Интерфейсы низкого уровня: API и обработка ошибок».
Все примеры кода скопированы дословно с указанных страниц-источников.

## Low-level API (индекс раздела)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/>

Раздел объединяет подразделы:

- API
  - [Accessing API](https://vkbottle.readthedocs.io/ru/latest/low-level/api/) — Работа с API
  - [Response Validator](https://vkbottle.readthedocs.io/ru/latest/low-level/api/response-validator/)
  - [Request Reschedulers](https://vkbottle.readthedocs.io/ru/latest/low-level/api/request-rescheduler/)
  - [Request Validators](https://vkbottle.readthedocs.io/ru/latest/low-level/api/request-validator/)
  - [Token Generators](https://vkbottle.readthedocs.io/ru/latest/low-level/api/token-generator/)
- [Exception Handling](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/)
  - [Error Handler](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/error-handler/)
  - [Code Exception](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/code-exception/)
- [Http Client](https://vkbottle.readthedocs.io/ru/latest/low-level/http-client/)
- [Polling](https://vkbottle.readthedocs.io/ru/latest/low-level/polling/)
- [Callback](https://vkbottle.readthedocs.io/ru/latest/low-level/callback/)

## Работа с API (API)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/api/>

### Обращение к API ВКонтакте

Вы можете взаимодействовать с API ВКонтакте прямо из коробки:

```python
from vkbottle import API

# ...
api = API(token="token")
await api.messages.send(peer_id=1, message="Привет Павел Дуров!")
```

> **Внимание**
> Все методы в vkbottle пишутся *снейк\_кейсом*.
> Это значит, например, что метод [`messages.getById`](https://dev.vk.ru/method/messages.getById) в vkbottle пишется как `api.messages.get_by_id`.

### Параметры

- **token** - токен сообщества/пользователя или [генератор токенов](https://vkbottle.readthedocs.io/ru/latest/low-level/api/token-generator/)
- **ignore\_error** - игнорировать ошибки VK API
- **http\_client** - клиент для запросов ([документация](https://vkbottle.readthedocs.io/ru/latest/low-level/http-client/))
- **request\_rescheduler** - рещедулер запросов ([документация](https://vkbottle.readthedocs.io/ru/latest/low-level/api/request-rescheduler/))

Таким образом, в `API` передаётся токен сообщества (group) или пользователя (user) либо генератор токенов; параметр `ignore_error` позволяет игнорировать ошибки VK API, а HTTP-клиент и решедулер запросов подключаются через одноимённые параметры.

### Captcha хендлер

Должен решить капчу и вернуть ее код:

```python
from vkbottle import CaptchaError

bot = ...


async def captcha_handler(e: CaptchaError):
    ...
    return code


bot.api.add_captcha_handler(captcha_handler)
```

## Response-Validator (валидация ответов)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/api/response-validator/>

Валидации ответов ВК нужны от случаев когда сервер по какой-то неизвестной причине возвращает html вместо json до правильно сформированной ошибки после запроса.

### Стандартные валидаторы ответов

#### JSONValidator

Парсит json из ответа с помощью самого правого json-парсера [из списка](https://vkbottle.readthedocs.io/ru/latest/modules/). Если вернулся необрабатываемый тип (например `NoneType`), то запускает `Request Rescheduler`, пока не будет получен валидный ответ.

#### VKErrorValidator

Вызывает `VKAPIError` от `CodeException` при респонсе с ошибкой от вк.

### Создание своего валидатора ответа

Пример с `response_validators` из `API` и `SomeRequestRescheduler` [отсюда](https://vkbottle.readthedocs.io/ru/latest/low-level/api/request-rescheduler/):

```python
from typing import TYPE_CHECKING, Any, NoReturn, Union
from vkbottle import API, ABCResponseValidator
from .request_rescheduler import SomeRequestRescheduler

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

class SomeResponseValidator(ABCResponseValidator):
    async def validate(
        self,
        method: str,
        data: dict[str, Any]:
        response: Any,
        ctx_api: "ABCAPI | API",
    ) -> Any | NoReturn:
        if "error" not in response:
            return response
        if ctx_api.ignore_errors:
            return None
        if response["error"]["error_code"] != 6:
            return response
        # Обрабатываем ошибку 6, которая возникает при слишком частых запросах
        return await SomeRequestRescheduler().reschedule(
            ctx_api, method, data, response
        )

api = API("token")
# Этот валидатор должен идти после JSONResponseValidator,
# но раньше VKAPIErrorResponseValidator, чтобы он не обработал эту ошибку
api.response_validators.insert(1, SomeResponseValidator())
```

Ключевой момент: ошибка VK API с кодом 6 (слишком частые запросы, т.е. превышение rate limit) перехватывается кастомным валидатором и передаётся в `Request Rescheduler`, который откладывает повтор запроса. Флаг `ctx_api.ignore_errors` отключает обработку ошибок.

## Request Rescheduler (решедулер запросов)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/api/request-rescheduler/>

Решедулеры нужны для того, чтобы отложить запрос к апи, который не удался по техническим причинам - например, ошибки серверов вконтакте.

Вызываются они из [валидаторов респонсов](https://vkbottle.readthedocs.io/ru/latest/low-level/api/response-validator/).

Решедулер должен имплементировать всего один метод - асинхронный reschedule, который получает на вход:

- `ctx_api` - апи с которым выполнялся запрос
- `method` - метод
- `data` - переданные параметры
- `recent_response` - ответ (например: None)

### Пример

```python
import asyncio
from typing import TYPE_CHECKING, Any, Union

from vkbottle import ABCRequestRescheduler

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

class SomeRequestRescheduler(ABCRequestRescheduler):
    def __init__(self, delay: int = 1):
        self.delay = delay

    async def reschedule(
        self,
        ctx_api: "ABCAPI | API",
        method: str,
        data: dict[str, Any]:
        recent_response: Any,
    ) -> dict[str, Any]:
        await asyncio.sleep(self.delay)
        return await ctx_api.request(method, data)
```

Решедулер делает паузу (`asyncio.sleep(self.delay)`) и повторяет запрос через `ctx_api.request(method, data)` — так настраиваются повторные попытки при технических сбоях и rate limit.

## Request-Validator (валидация запросов)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/api/request-validator/>

Валидации запросов к ВК нужны, например, для того, чтобы превращать списки чего-либо в строку с значениями через запятую как это требует вк.

### Стандартные валидаторы ответов

#### TranslateFriendlyTypesRequestValidator

Превращает стандартные типы питона в типы которые документирует вк:

- `list` -> `",".join(v)`
- `bool` -> `int(v)`
- `dict` -> `self.validate(v)`
- `BaseModel` -> `v.model_dump_json()`

### Создание своего валидатора ответа

Пример с `request_validators` из `API`:

```python
from vkbottle import API, ABCRequestValidator

class SomeRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict[str, Any]): -> dict[str, Any]:
        # some stuff with request data
        return request

api = API("token")
api.request_validators.append(SomeRequestValidator())
```

## Token-Generator (генератор токенов)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/api/token-generator/>

У VK существуют лимиты на запросы, но эти лимиты легко обходятся при наличии нескольких токенов, для того чтобы автоматически распределять токены на каждый запрос используются токен генераторы, существуют 2 вида генераторов из коробки:

- `SingleTokenGenerator` - используется один токен на все запросы, принимает строку
- `ConsistentTokenGenerator` - используется несколько токенов поочередно, если вы хотите его использовать грамотно, необходимо рассчитать нагрузку по времени, лимит вконтакте на запросы для ботов - 25/сек, для пользователей - 3/сек, принимает лист из строк

По правилам vkbottle вы конечно же можете реализовать свой генератор, базируясь на интерфейсе [ABCTokenGenerator](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/api/token_generator/abc.py)

Ключевые моменты:

- Генератор токенов передаётся в `API` параметром `token` (см. [Работа с API](https://vkbottle.readthedocs.io/ru/latest/low-level/api/)).
- Это способ обхода лимитов ВК за счёт нескольких токенов: токены автоматически распределяются между запросами.
- Официальные лимиты: для ботов (group-токены) — 25 запросов/сек, для пользователей (user-токены) — 3 запроса/сек.
- Свои генераторы пишутся на основе интерфейса `ABCTokenGenerator`.

## HTTP-Client (HTTP-клиент)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/http-client/>

По-умолчанию библиотека использует `SingleAiohttpClient` для отправки всех запросов.
(Его особенность в том, что он всегда использует одну и ту же сессию.)

### Работа с клиентами

#### request\_raw

Делает реквест. Для aiohttp возвращает объект `aiohttp.ClientResponse`.

#### request\_text

Делает реквест и читает поле `text`. Возвращает строковый тип

#### request\_json

Делает реквест и десериализует `json` с помощью одной из доступных библиотек, выбираются с помощью `choicelib` в порядке слева направо: `json`, `ujson`, `hyperjson`, `orjson`. Возвращает словарь десериализованный из `json`а

#### request\_content

Делает реквест и читает вернувшийся `content`, используется для скачивания медиафайлов в аплоадерах. Возвращает байты

#### Параметры

- `url` - ссылка по которой будет произведен
- `method` - HTTP метод запроса (например: get)
- `data` - данные которые будут переданы в запросе
- `**kwargs` - передаются в качестве параметров в запросе

##### При инициализации `AiohttpClient` можно указать параметры

- `session` - объект сессии (если не указан, то будет создан новый)
- `json_processing_module` - модуль для десериализации json
  (если не указан, то будет использован [один из доступных модулей](https://vkbottle.readthedocs.io/ru/latest/modules/))
- `optimize` - если передан True, то в конструктор сессии будут переданы параметры `raise_for_status=True` и `skip_auto_headers={"User-Agent"}`.
- `**session_params` - `**kwargs`, передаются в конструктор сессии.
  Можно использовать для передачи `headers` или `cookies`

> **Примечание**
> Подробнее обо всех параметрах можно почитать [здесь](https://docs.aiohttp.org/en/stable/client_reference.html).

#### Пример

```python
from vkbottle.http import AiohttpClient

# ...
http_client = AiohttpClient()
await http_client.request_text("https://google.com")
```

### Создание кастомного клиента

Кастомный клиент должен унаследовать `ABCHTTPClient` и имплементировать вышеупомянутые методы.

## Error-Handler (хендлер ошибок)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/error-handler/>

Хендлер ошибок нужен для быстрой и простой обработки любых типов исключений.

Для того, чтобы начать с ним работу, потребуется создать его и зарегистрировать в него хендлеры исключений:

```python
from vkbottle import ErrorHandler

error_handler = ErrorHandler(redirect_arguments=False, raise_exceptions=False)
# Если redirect_arguments = True, то все аргументы обернутой функции будут поступать и в хендлер исключения
# Если raise_exceptions = True, то все необработанные исключения будут выброшены (игнорируется, если есть обработчик для ненайденных ошибок)


@error_handler.register_error_handler(RuntimeError)
async def exc_handler_runtime(e: RuntimeError):
    print("Oh no runtime error occurred:", e)


@error_handler.register_error_handler(LookupError)
async def exc_handler_lookup(e: LookupError):
    print("Oh no lookup error occurred:", e)
```

Еще вы можете добавить хендлер для ненайденных ошибок:

```python
@error_handler.register_undefined_error_handler
async def exc_handler_undefined(e: Exception):
    print("Oh no unknown error occurred", e)
```

Теперь чтобы error_handler сработал на вашей асинхронной функции добавьте к ней декоратор:

```python
@error_handler.catch
async def main():
    raise LookupError("I ve lost my keys")
```

Запустите ее и оцените вывод:

```python
import asyncio

asyncio.run(main())
```

```text
Oh no lookup error occurred: I've lost my keys
```

Ключевые моменты:

- `ErrorHandler` создаётся с флагами `redirect_arguments` (передавать аргументы обёрнутой функции в хендлер исключения) и `raise_exceptions` (выбрасывать необработанные исключения).
- Хендлеры регистрируются декоратором `register_error_handler` для конкретного типа исключения, `register_undefined_error_handler` — для всех остальных.
- Применяется к асинхронным функциям через декоратор `@error_handler.catch`.

## Code-Exception (исключения с кодом)

Источник: <https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/code-exception/>

Фреймворк заботится о том как вы будете хендлить исключения (не ошибки, а именно исключения, которые уже были выброшены; для того чтобы хендлить ошибки читайте соответствующую документацию).

### Использование

Базовый класс для исключений с кодом это `CodeException`.
`CodeException` имеет generic-подобный синтаксис, код ошибки указывается в `[квадратных скобках]`.
Базовое Исключение для ошибок API можно импортировать под именем `VKAPIError`.

### Вызов исключения и способы хендлинга с `CodeException`

```python
class MyCodeError(CodeException):
    pass


try:
    raise MyCodeError[1]("Error description")
except MyCodeError[1]:
    print("Error with code 1 appeared")
except MyCodeError[2, 3]:
    print("Error with code 2 or 3 appeared")
except MyCodeError as e:  # Ошибка с любым кодом
    print(f"Error with code {e.code} appeared")
```

Ключевые моменты:

- `VKAPIError` — базовое исключение для ошибок VK API (ошибки API порождаются `VKErrorValidator` в цепочке валидаторов ответов, см. [Response Validator](https://vkbottle.readthedocs.io/ru/latest/low-level/api/response-validator/)).
- Перехват возможен по конкретному коду (`MyCodeError[1]`), по нескольким кодам (`MyCodeError[2, 3]`) или по любому коду (`except MyCodeError as e`, код доступен через `e.code`).
