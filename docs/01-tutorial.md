# Туториал VKBottle

Локальная копия раздела «Туториал» документации VKBottle (https://vkbottle.readthedocs.io/ru/latest/). Все примеры кода приведены дословно с сайта-источника.

## Содержание туториала

Источник: [tutorial/](https://vkbottle.readthedocs.io/ru/latest/tutorial/)

### Ключевые моменты

- Полный список разделов туториала VKBottle: первый бот, правила, разделение кода, клавиатуры и вложения, мидлвари и return менеджеры, обработка ошибок, подключение CallbackAPI, рекомендуемые IDE, FAQ.

1. [Первый бот на vkbottle](https://vkbottle.readthedocs.io/ru/latest/tutorial/first-bot/)
2. [Правила](https://vkbottle.readthedocs.io/ru/latest/tutorial/rules/)
3. [Разделение кода](https://vkbottle.readthedocs.io/ru/latest/tutorial/code-separation/)
4. [Клавиатуры и вложения](https://vkbottle.readthedocs.io/ru/latest/tutorial/keyboards-attachments/)
5. [Мидлвари и return менеджеры](https://vkbottle.readthedocs.io/ru/latest/tutorial/middlewares-return-managers/)
6. [Обработка ошибок](https://vkbottle.readthedocs.io/ru/latest/tutorial/error-handling/)
7. [Подключение CallbackAPI](https://vkbottle.readthedocs.io/ru/latest/tutorial/callback-bot/)
8. [Рекомендуемые IDE](https://vkbottle.readthedocs.io/ru/latest/tutorial/recommended-ide/)
9. [FAQ](https://vkbottle.readthedocs.io/ru/latest/tutorial/faq/)

## Первый бот на vkbottle

Источник: [tutorial/first-bot/](https://vkbottle.readthedocs.io/ru/latest/tutorial/first-bot/)

### Ключевые моменты

- Импорт `API` из `vkbottle` — полная типизация запросов к VK API (пакет vkbottle/types), вызов методов через `await`, параметры передаются аргументами.
- Инициализация `API` строкой-токеном или листом токенов (автоконвертация в token-generator).
- Класс `Bot` (из `vkbottle` или `vkbottle.bot`) — обязателен аргумент `token` **или** `api`; `Bot` только для групп, для юзербота есть отдельный интерфейс.
- Регистрация хендлеров через `bot.labeler` / `bot.on`: декораторы `.message` (беседы + ЛС), `.private_message` (только ЛС), `.chat_message` (только беседы).
- Шорткаты хендлера: `message.answer(...)` (аналог `messages.send`, не требует `peer_id` и `random_id`), `bot.api.users.get(...)`.
- Запуск: `bot.run_forever()` из синхронной среды или `await run_polling()` в асинхронной.
- Предупреждение: в настройках лонгпола должны быть отмечены нужные события (новые сообщения), стабильная версия API — `5.131`.

Добро пожаловать в первую часть туториала, здесь будет представлено как можно взаимодействовать с `API` и рассказано почему нужно использовать только асинхронные библиотеки при работе с `vkbottle`

Для начала работы с апи следует импортировать нужный объект - `vkbottle.API`

```python
from vkbottle import API
```

`API` - готовый инструмент для того, чтобы делать запросы к апи вконтакте, приятная особенность этого инструмента в vkbottle - полная типизация ([vkbottle/types](https://github.com/vkbottle/types "GitHub Repository: vkbottle/types")).

### Типизация

При условии, что у вас стоит [нормальное IDE](https://vkbottle.readthedocs.io/ru/latest/tutorial/recommended-ide/) вы можете использовать подсказки типов:

![api highlighting](https://vkbottle.readthedocs.io/ru/latest/tutorial/assets/api-highlighting.png "api highlighting")

Это значительно ускорит скорость разработки и позволит не обращаться в документацию api вконтакте каждый раз

Как уже стало понятно из картинки выше, для вызова метода используется ключевое слово `await`, которое является частью реализации асинхронности python, перед продолжением чтения туториала рекомендуется [почитать официальную документацию](https://docs.python.org/3/library/asyncio.html), если вы этого не делали

### Первый запрос

Для того чтобы инициализировать `API` вам понадобится строка (токен) или вы можете использовать лист строк (токенов), которые автоматически конвертируются в специальный [token-generator](https://vkbottle.readthedocs.io/ru/latest/low-level/api/token-generator/)

Обернем наш будущий запрос базовым способом исполнения асинхронного кода:

```python
import asyncio

async def main():
    ...

asyncio.run(main())
```

Теперь напишем само взаимодействие:

```python
api = API("token")
await api.wall.post(message="#vkbottle прекрасен!")
```

Такой запрос создаст пост на стене группы/пользователя с указанным текстом, как вы видите параметры запроса принимаются в качестве аргументов (IDE вам все подскажет)

Вот, что должно получиться в итоге:

```python
import asyncio
from vkbottle import API

async def main():
    api = API("token")
    await api.wall.post(message="#vkbottle прекрасен!")

asyncio.run(main())
```

Поздравляю, теперь вы умеете работать с инструментом `API`!

### Первый бот

> **Примечание**
>
> Если вы не хотите использовать простые (high-level) инструменты для разработки бота вы можете использовать low-level [Polling](https://vkbottle.readthedocs.io/ru/latest/low-level/polling/), или самостоятельно написать всю логику на запросах к api как показано в разделе выше

Чтобы начать работу с ботом, требуется импортировать класс `Bot` из корня проекта (`vkbottle`) или из специализированного пакета (`vkbottle.bot`):

> **Внимание**
>
> Bot - это класс исключительно для групп, если вы хотите использовать юзербота, то сначала ознакомьтесь с [этим](https://vkbottle.readthedocs.io/ru/latest/high-level/user/).

```python
from vkbottle.bot import Bot
```

Для инициализации бота обязателен аргумент - `token` *или* `api`. `token` нужен для сокращения кода: если вы передадите `token`, будет создан `API` с соответствующим генератором токена. Если вы передадите `api`, он и будет использоваться для бота

```python
# Инициализация токеном
bot = Bot(token="token")
# (или) Инициализация с апи
bot = Bot(api=api)
```

Теперь вы можете добавить нужные хендлеры, за удобное добавление хендлеров отвечает элемент [labeler](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/labeler/), к которому вы можете обратиться через `bot.labeler` или `bot.on` (`.on` нужен просто для красоты и для традиционного legacy вкботла из второй версии)

```python
from vkbottle.bot import Bot, Message

bot = Bot(token="token")

@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}".format(users_info[0].first_name))

bot.run_forever()
```

Разберем новый код построчно:

`@bot.on.message(text="Привет")` - это декоратор, он означает, что если сообщение будет отвечать заданным правилам (`text="привет"`), сработает хендлер под декоратором

Для сообщений в vkbottle существует 3 декоратора:

`.message` - обрабатывает сообщения и из бесед и из личных переписок

`.private_message` - обрабатывает сообщения только из личных переписок

`.chat_message` - обрабатывает сообщения только из бесед

`async def hi_handler(message: Message)` - объявление хендлера, `hi_handler` - название функции, может быть разумно любым, `message` - аргумент, который обязательно вернется в хендлер, нужный для получения информации о событии

`users_info = await bot.api.users.get(message.from_id)` - запрос к API, получение информации о пользователе, написавшем сообщение

`await message.answer("Привет, {}".format(users_info[0].first_name))` - отправка сообщения в чат с пользователем, `answer` - удобный шорткат для ответа на сообщения, аргументы идентичны методу `messages.send`, но шорткат не требует id чата и `random_id`

`bot.run_forever()` - помогает асинхронно запустить бота из синхронной среды, если бы была создана асинхронная, вы бы могли использовать `await run_polling()`

Если представленный код не работает, проверьте поставили ли вы галочки в настройках лонгпола на нужные события (в данном случае на новые сообщения) и сам лонгпол (стабильна версия `5.131`)

### Экзамплы по этой части туториала

- [easy-bot](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/easy_bot.py)

## Правила

Источник: [tutorial/rules/](https://vkbottle.readthedocs.io/ru/latest/tutorial/rules/)

### Ключевые моменты

- Правила (rules/«рулзы») определяют, какие события ловит хендлер; встроенные правила рассчитаны только на объект `Message` (для сырых евентов — своя реализация).
- Способы использования: импорт из `vkbottle.dispatch.rules.base` (например `CommandRule('say', ['!', '/'], 1)`) или шорткаты в декораторе (`command=('say', 1)`).
- Интерфейс правила — класс `ABCRule[Message]` с одним асинхронным методом `check`, возвращающим `False`, `True` либо словарь аргументов для распаковки в хендлер.
- Регистрация кастомного правила для шортката: `bot.labeler.custom_rules['my_rule'] = MyRule` (до объявления хендлеров), затем `@bot.on.message(my_rule=50)`.
- Правила-врапперы: `func` (шорткат `FuncRule`), `coro`/`coroutine` (шорткат `CoroutineRule`).

Для того чтобы хендлер ловил только нужные сообщения/другие ивенты, нужны правила (rules, рулзы - устоявшаяся транслитерация в комьюнити вкботла), в вкботле существует множество рулзов прямо из коробки.

> **Внимание**
>
> Все встроенные рулзы работают только с объектом `Message`, для обработки сырых евентов нужно писать свою реализацию.

Есть несколько способов использования правил:

1. Импортировать их из `vkbottle.dispatch.rules.base` и использовать, инициализируя прямо в декораторе или в любой другой части кода:

```python
from vkbottle.dispatch.rules.base import CommandRule

@bot.on.message(CommandRule("say", ["!", "/"], 1))
async def say_handler(message: Message, args: tuple[str]):
    await message.answer(f"<<{args[0]}>>")
```

2. Использовать шорткаты, список с названиями можно найти [здесь](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/rules/)

```python
@bot.on.message(command=("say", 1))
async def say_handler(message: Message, args: tuple[str]):
    await message.answer(f"<<{args[0]}>>")
```

> **Примечание**
>
> Некоторые правила принимают в качестве аргумента итерируемый объект.
>
> Например, `CommandRule`, который принимает два аргумента: `command` и `args_count`, но при использовании шортката можно передавать их в кортеже:
>
> `@bot.on.message(command=("help", 0))`

### Создание собственных правил

> **Примечание**
>
> Правило - это класс соответствующий интерфейсу `ABCRule`, который должен реализовать лишь один асинхронный метод `check`, принимающий ивент и возвращающий `False` если проверка пройдена не была и `True` либо словарь с аргументами, которые будут распакованы в хендлер как непозиционные аргументы

#### Создание правил напрямую

Чтобы создать правила импортируем `ABCRule` и имплементируем асинхронный метод `check`, еще стоит импортировать `Union` из `typing` для типизации вашего кода:

```python
from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class MyRule(ABCRule[Message]):
    async def check(self, event: Message) -> dict[str, Any] | bool:
        ...
```

Теперь стоит имплементировать логику правила `MyRule`, пусть оно будет просто проверять что длина сообщения меньше ста символов:

```python
return len(message.text) < 100
```

Вот что получилось:

> **Примечание**
>
> Union в данном правиле не понадобился поэтому его допустимо опустить по стандартам mypy, в любом случае на сигнатуру это не повлияет

```python
from typing import Union
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class MyRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        return len(event.text) < 100
```

Теперь правило можно использовать как первым способом:

```python
@bot.on.message(MyRule())
```

Вторым способом рулзом `MyRule` в текущем состоянии воспользоваться не получится, из-за отсутствия каких-либо параметров правила, предлагается его кастомизировать с помощью метода `__init__`:

```python
# Новый вид правила
class MyRule(ABCRule[Message]):
    def __init__(self, lt: int = 100):
        self.lt = lt

    async def check(self, event: Message) -> bool:
        return len(event.text) < self.lt
```

Теперь, если предварительно (до объявления хендлеров) зарегистрировать правило в локальный лейблер

```python
bot.labeler.custom_rules["my_rule"] = MyRule
```

Его можно будет использовать и вторым способом:

```python
@bot.on.message(my_rule=50)
```

#### Создание правил через правила-врапперы

> **Примечание**
>
> Есть так называемые правила-врапперы, правила - которые исполняют какой-то код который получают как параметры

К правилам-врапперам из коробки можно отнести: `func`, шорткат для `FuncRule`; `coro` или `coroutine`, шорткат для `CoroutineRule`

`FuncRule` принимает в качестве аргумента функцию (которая может быть лямбдой). Созданное напрямую правило `MyRule` можно заменить вот так:

```python
@bot.on.message(func=lambda message: len(message.text) < 100)
```

### Экзамплы по этой части туториала

- [labeler-setup](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/labeler_setup.py)
- [rules-shortcuts](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/rules_shortcuts.py)

## Разделение кода

Источник: [tutorial/code-separation/](https://vkbottle.readthedocs.io/ru/latest/tutorial/code-separation/)

### Ключевые моменты

- Составляющие фреймворка (`API`, `BotLabeler`, `BuiltinStateDispenser`) используются отдельно от `Bot` и собираются в `config.py`.
- Рекомендуемая структура: `/src/` с папкой `handlers` (`__init__.py`, `admin.py`, `chat.py`, `ping.py`), `bot.py`, `config.py`.
- `auto_rules` в лейблере автоматически добавляет правила всем хендлерам сообщений; для сырых евентов — `raw_event_auto_rules`.
- Локальные лейблеры: `BotLabeler()`, настройки `vbml_ignore_case`, `auto_rules = [rules.PeerRule(from_chat=True), ...]`, контекстные аргументы из правил (`chat: MessagesConversation`).
- Загрузка лейблеров в глобальный: `labeler.load(chat_labeler)`, порядок регистрации = порядок импорта.
- Создание бота: `Bot(api=api, labeler=labeler, state_dispenser=state_dispenser)`, запуск — `bot.run_forever()`.

> **Примечание**
>
> Разделение кода - очень важная вещь для создания структуры проекта

Чтобы делать это, в vkbottle можно использовать составляющие фреймворка отдельно от `Bot`

Разделение кода, кроме того может быть очень грамотно использовано для создания локальных изменений в лейблере, например `auto_rules` поможет установить правила, которые будут накладываться на все хендлеры сообщений

> **Внимание**
>
> Правила в `auto_rules` распространяются только на хендлеры сообщений, для сырых евентов вам нужен `raw_event_auto_rules` и кастомные правила, работающие с ними

### Стандартная иерархия файлов

Для удобства разработки больших проектов, рекомендуется использовать подобную структуру файлов:

```text
/src/
├── handlers
│   ├── __init__.py
│   ├── admin.py
│   ├── chat.py
│   └── ping.py
├── bot.py
└── config.py
```

#### `config.py`

Для начала создадим файл с конфигом, в котором будут храниться все глобальные переменные, которые будут использоваться в разных частях проекта

```python
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

api = API("token")
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
```

> **Примечание**
>
> В данном примере стейт диспенсер не используется, но объявлен для наглядности
>
> Если вы хотите использовать его, то просто импортируйте из `config.py` и используйте в своих хендлерах
>
> Не забудьте указать `state_dispenser` в `Bot` в `bot.py`

#### `ping.py`

Теперь создадим файл `ping.py` в папке `handlers`, в котором будет простой хендлер, обрабатывающий сообщения с текстом `ping`

```python
from config import labeler

@labeler.message(text="ping")
async def ping_handler(message):
    await message.answer("pong")
```

#### `chat.py`

В этом случае мы будем использовать `auto_rules`, чтобы автоматически добавлять правила к хендлерам,
поэтому создадим новый лейблер, который будет использоваться только в этом файле

1. Добавим в auto_rules правило, которое будет следить чтобы все сообщения шли только из чата
2. Создадим правило, которое будет получать информацию о чате и возвращать ее для всех хендлеров этого лейблера
3. Добавим несколько хендлеров

```python
from vkbottle.bot import BotLabeler, Message, rules
from vkbottle_types.objects import MessagesConversation

class ChatInfoRule(rules.ABCRule[Message]):
    async def check(self, message: Message) -> dict[str, Any]:
        chats_info = await message.ctx_api.messages.get_conversations_by_id(message.peer_id)
        return {"chat": chats_info.items[0]}

chat_labeler = BotLabeler()
chat_labeler.vbml_ignore_case = True
chat_labeler.auto_rules = [rules.PeerRule(from_chat=True), ChatInfoRule()]

@chat_labeler.message(command="самобан")
async def kick(message: Message, chat: MessagesConversation):
    await message.ctx_api.messages.remove_chat_user(message.chat_id, message.from_id)
    await message.answer(f"Участник самоустранился из {chat.chat_settings.title} по собственному желанию")

@chat_labeler.message(text="где я")
async def where_am_i(message: Message, chat: MessagesConversation):
    await message.answer(f"Вы в <<{chat.chat_settings.title}>>")
```

#### `admin.py`

> Пусть эти команды будут доступны только, например, создателю бота

1. Создадим проверку на id пользователя, написавшего сообщение
2. Добавим несколько хендлеров

```python
from vkbottle.bot import BotLabeler, Message, rules

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(1)] # Допустим, вы являетесь Павлом Дуровым

@admin_labeler.message(command="halt")
async def halt(_):
    exit(0)
```

#### `__init__.py`

Теперь создадим файл `__init__.py` в папке `handlers`, в котором будем импортировать все лейблеры

```python
from .chat import chat_labeler
from .admin import admin_labeler
from .ping import labeler
# Если использовать глобальный лейблер, то все хендлеры будут зарегистрированы в том же порядке, в котором они были импортированы

__all__ = ("admin_labeler", "chat_labeler", "labeler")
```

#### `bot.py`

Теперь мы можем создать файл `bot.py`, в котором будем создавать бота и регистрировать лейблеры

```python
from vkbottle import Bot
from config import api, state_dispenser, labeler
from handlers import chat_labeler, admin_labeler
```

> Так как мы создали файл `__init__.py` в папке `handlers`, интерпретатор выполнит код в `echo.py` и нам не нужно будет импортировать лейблер оттуда

Теперь нам нужно загрузить хендлеры в глобальный лейблер:

```python
labeler.load(chat_labeler)
labeler.load(admin_labeler)
```

Далее нужно создать инстанс бота и указать, какой лейблер и стейт диспенсер использовать:

```python
bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)
```

Осталось только запустить бота:

```python
bot.run_forever()
```

### Экзамплы по этой части туториала

- [code_separation](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/code_separation)

## Клавиатуры и вложения

Источник: [tutorial/keyboards-attachments/](https://vkbottle.readthedocs.io/ru/latest/tutorial/keyboards-attachments/)

### Ключевые моменты

- `Keyboard` (из `vkbottle`) с параметрами `one_time` и `inline`; методы: `add(action, color)`, `row()`, `get_json()`; создание использует `json.dumps` (для статичной клавиатуры можно преобразовать один раз).
- Отправка: `message.answer(..., keyboard=keyboard)`.
- Вложения: готовая ссылка вида `"type{OWNER_ID}_{ITEM_ID}"` передаётся в `message.answer(..., attachment=attachment)`; для динамических вложений используются загрузчики (`AnyUploader(bot.api)`, `await uploader.upload("path/to/file")`).
- Шаблоны (пока только карусель): `TemplateElement` и `template_gen(...)` из `vkbottle.tools`, отправка через `message.answer(..., template=my_template)`.

### Клавиатура

#### Создание через `Keyboard`

```python
from vkbottle import Keyboard
```

`Keyboard` принимает параметры `one_time` и `inline` (их значение описано [здесь](https://vk.ru/dev/bots_docs_3?f=4.2.%20Структура%20данных)).

Методы `Keyboard`:

- `add(action, color)` - добавляет кнопку к текущему ряду кнопок;
- `row()` - создаёт следующий ряд кнопок, переводит "курсор" на него;
- `get_json()` - преобразует клавиатуру в JSON-объект, который можно отправить в сообщении.

Создание клавиатуры использует `json.dumps` для преобразования в JSON-объект. Если ваша клавиатура статична, то вы можете избежать этой повторяющейся операции, создав её один раз, и используя уже "преобразованную" клавиатуру.

Примеры создания клавиатуры приведены [здесь](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/generate_keyboard.py), а отправить её можно так:

```python
keyboard = ...  # see examples above

@bot.on.message()
async def send_keyboard(message):
    await message.answer("Here is your keyboard!", keyboard=keyboard)
```

### Вложения

#### Если у вас уже есть ссылка на вложение

Если у вас уже есть ссылка на вложение вида `"type{OWNER_ID}_{ITEM_ID}"` (например `"photo-41629685_457239401"`), то вы можете отправить её так:

```python
attachment = ... # see example above

@bot.on.message
async def send_attachment(message):
    await message.answer("See that attachment!", attachment=attachment)
```

#### Если вы загружаете вложения динамически

Для того чтобы отправлять вложения, загруженные во время работы бота, нужны загрузчики. Прочитайте [документацию про загрузчики], и возвращайтесь сюда.

Пример отправки вложения, полученного из загрузчика:

```python
uploader = AnyUploader(bot.api)  # see uploaders types in "Uploaders documentation" above

@bot.on.message()
async def send_attachment(message):
    attachment = await uploader.upload("path/to/file")
    await message.answer("See that attachment!", attachment=attachment)
```

### Шаблоны

На данный момент ВКонтакте поддерживает только один вид шаблона — карусель. Документация по этому виду шаблона представлена [здесь](https://vk.ru/dev/bot_docs_templates?f=5.%20Шаблоны%20сообщений).

Вы можете создать шаблон через vkbottle с помощью:

- `TemplateElement` - элемент шаблона. Названия полей соответствуют названиям полей в документации ВКонтакте.
- `template_gen` - создаёт шаблон из предоставленных элементов:

```python
from vkbottle.tools import template_gen, TemplateElement

my_template = template_gen(TemplateElement(...), TemplateElement(...), TemplateElement(...))
```

В этом примере `my_template` - уже готовый JSON-объект для отправки в сообщении. Вот пример его отправки:

```python
my_template = ...  # see example above

@bot.on.message()
async def send_template(message):
    await message.answer("Sending template...", template=my_template)
```

### Расширенные примеры по этой части

- [Создание клавиатуры](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/generate_keyboard.py)
- [Загрузка и отправка вложений](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/uploaders_example.py)

## Мидлвари и return менеджеры

Источник: [tutorial/middlewares-return-managers/](https://vkbottle.readthedocs.io/ru/latest/tutorial/middlewares-return-managers/)

### Ключевые моменты

- Мидлварь — внешний слой вокруг обработки хендлеров, состояния `pre` (до поиска хендлера) и `post` (после обработки); базовый класс `BaseMiddleware[Message]` из `vkbottle`.
- `async def pre(self)`: доступ к ивенту через `self.event`, остановка обработки — `self.stop(...)`, обновление контекста — `self.send`.
- `async def post(self)`: повлиять на обработку нельзя (обычно статистика/логи), доступны `self.handlers`, `self.handle_responses`, `self.view`.
- Регистрация: `bot.labeler.message_view.register_middleware(...)` (view `MessageView` лежит в `.message_view`), метод можно использовать и как декоратор.
- Return менеджер `MessageView`: `str` → отправляется сообщением; `tuple`/`list` → элементы конвертируются в строки и отправляются; `dict` → распаковывается как kwargs для `message.answer`.

### Мидлвари

Мидлвари - так называемые внешние слои, покрывающие обработку хендлеров. У мидлварей есть два состояния - `pre` и `post`, `pre` это то, что происходит до начала поиска хендлера (когда только нашелся нужный `view`), а `post` - то что происходит когда хендлер уже был обработан и известно все о прошедшей обработке: какие хендлеры сработали, что они вернули

Чтобы создать мидлварь, импортируйте для начала абстрактный класс для него из корневого пакета:

```python
from vkbottle import BaseMiddleware
from vkbottle.bot import Message
```

Теперь начните писать ваш собственный класс:

```python
class MiddlewareName(BaseMiddleware[Message]):
```

Так как наш мидлварь обрабатывает именно сообщения, нужно указать тип в дженерике.
В данном случае мы используем класс `Message` из `vkbottle.bot`

Middleware без методов `pre` или/и `post` бесполезен, нужно разобраться как реализовать каждый из них

#### async def pre(self)

`pre` имеет доступ к ивенту (например сообщению) через `self` и может вернуть ошибку через `self.stop` или обновить контекст через `self.send`

[Техническая документация](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/)

Вот так например можно отсеивать все сообщения от ботов:

```python
from vkbottle.bot import Message
from vkbottle import BaseMiddleware, MiddlewareResponse

class NoBotMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("from_id меньше 0")
```

#### async def post(self)

`post` уже никак не может повлиять на обработку ивента. Обычно его используют для статистики и логов

```python
from vkbottle.bot import Message
from vkbottle import BaseMiddleware

class LogMiddleware(BaseMiddleware[Message]):
    async def post(self):
        if not self.handlers:
            return

        print(f"{len(self.handlers)} хендлеров сработало на сообщение. "
              f"Они вернули {self.handle_responses}, "
              f"все они принадлежали к view {self.view}")
```

---

`pre` и `post` можно использовать и одновременно в одном мидлваре

#### Регистрация мидлварей

Чтобы зарегистрировать мидлварь (и он работал) нужно определиться с view к которому он принадлежит, в данном случае это `MessageView`

В лейблере `MessageView` располагается по адресу `.message_view`

У каждого view есть метод `register_middleware`, воспользуемся им:

```python
bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.labeler.message_view.register_middleware(LogMiddleware)
```

Кстати методом `register_middleware` можно пользоваться и как декоратором.

Полный код с мидлварями вы можете найти [в этом экзампле](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py)

### Return менеджеры

В этой части туториала упоминалось о каких-то значениях, что возвращаются их хендлеров. Что же это и зачем они нужны?

> **Примечание**
>
> Создание кастомного менеджера для вашего view выходит за рамки этого туториала, но вы можете [прочитать об этом в технической документации](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/), когда посчитаете что готовы

Для общего понимания будет разобран return менеджер из коробки для `MessageView`

Суть заключается в том, что возвращая значения некоторых типов из хендлера, сработают хендлеры return менеджера которые произведут некоторые действия, вот что будет необходимо знать для комфортной разработки:

| тип значения | что произойдет |
| --- | --- |
| str | строка отправится как сообщение |
| `tuple` или `list` | все элементы будут конвертированы в строки и отправлены как сообщения |
| dict | словарь распакуется как непозиционные аргументы для метода `message.answer` |

### Экзамплы по этой части туториала

- [middleware](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py)

## Обработка ошибок

Источник: [tutorial/error-handling/](https://vkbottle.readthedocs.io/ru/latest/tutorial/error-handling/)

### Ключевые моменты

- `VKAPIError` (подтип `CodeException`): поля `code` (int) и `error_msg` (str); ловится без кода (`except VKAPIError`) и по коду (`except VKAPIError[902]`), комбинирование блоков поддерживается.
- Специфичные ошибки: `CaptchaError` с полями `captcha_sid`, `captcha_img`.
- `ErrorHandler` (доступен как `bot.error_handler`), 4 метода: `register_error_handler` (декоратор, принимает типы ошибок), `register_undefined_error_handler`, `handle(error)`, `catch` (декоратор).
- Параметр `redirect_arguments: bool` — передаёт в хендлер аргументы из задекорированной `catch` функции (в т.ч. контекстные аргументы правил и мидлварей).
- Регистрация сразу для нескольких типов: `register_error_handler(TypeError, ValueError)` и `register_error_handler(*VKAPIError[6, 9])`.

Иногда при запросах к api вконтакте возникают ошибки, для их обработки во фреймворке предусмотрено несколько инструментов

### try ... except VKAPIError

Для начала разъясним что такое `VKAPIError`, это подтип `CodeException`, особенность которого заключается в том, чтобы ошибка идентифицировалась в except и без указанного кода (`except VKAPIError`) и при указании кода (`except VKAPIError[code]`)

В `VKAPIError` есть два поля:

- `code` - код ошибки, int
- `error_msg` - описание ошибки, str

Чтобы использовать `VKAPIError` нужно импортировать его:

```python
from vkbottle import VKAPIError
```

Теперь можно обернуть какой нибудь код с запросом к API:

```python
try:
    await api.wall.post()
except VKAPIError as e:
    print("Возникла ошибка", e.code)
```

При исполнении этого кода vk вернет ошибку, из-за того что не были переданы нужные параметры

### try ... except VKAPIError[code]

Кроме более общего способа для обработки всех ошибок vk в одном блоке except, вы можете воспользоваться более конкретным `VKAPIError[code]`

> **Примечание**
>
> Список всех ошибок с их кодами вы можете найти [здесь](https://dev.vk.ru/reference/errors)

Сделаем несколько блоков для демонстрации того, как первый и второй способ можно комбинировать

```python
try:
    await api.messages.send(peer_id=1, message="привет!", random_id=0)
except VKAPIError[902] as e:
    print("не могу отправить сообщение из-за настроек приватности")
except VKAPIError as e:
    print("не могу отправить:", e.error_msg)
```

### Специфичные ошибки

Некоторые ошибки vk имеют дополнительные поля, которые могут понадобиться вам для их обработки:

- `CaptchaError`:
  - `captcha_sid` - идентификатор captcha, str
  - `captcha_img` - ссылка на изображение, str

### ErrorHandler

> **Примечание**
>
> Инструмент будет рассматриваться конкретно с ботом, хоть это и отдельный объект, так как это - туториал - упрощенный вариант документации
>
> Техническая документация по хендлеру ошибок [здесь](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/error-handler/)

У `ErrorHandler` есть 4 метода:

- `register_error_handler` - декоратор, принимающий типы ошибок и асинхронную функцию-хендлер. Если возникнет одна из указанных ошибок (или её подтипа), исполнится указанный хендлер.
- `register_undefined_error_handler` - декоратор, принимающий тип ошибки и асинхронную функцию-хендлер. Если возникнет неизвестная ошибка, исполнится этот хендлер.
- `handle`, принимающий экземпляр ошибки. Передаёт ошибку в соответствующий хендлер, зарегистрированный с помощью вышеописанных декораторов. Если для данной ошибки нет хендлера, поднимает её.
- `catch` - декоратор. Ловит ошибки из декорированной функции и передаёт их методу `handle`.

```python
from vkbottle import Bot, VKAPIError

bot = Bot("token")

@bot.error_handler.register_error_handler(RuntimeError)
async def runtime_error_handler(e: RuntimeError):
    print("возникла ошибка runtime", e)

@bot.error_handler.register_error_handler(VKAPIError[902])
async def unable_to_write_handler(e: VKAPIError):
    print("человек не разрешил отправлять сообщения", e)
```

В примере создано 2 хендлера ошибок: для `RuntimeError` и конкретизированного `VKAPIError`

Также можно регистрировать хендлеры сразу для нескольких типов ошибок:

```python
from typing import Union

from vkbottle import Bot, VKAPIError

bot = Bot("token")

@bot.error_handler.register_error_handler(TypeError, ValueError)
async def type_or_value_error_handler(e: TypeError | ValueError):
    print("возникла ошибка type или value", e)

@bot.error_handler.register_error_handler(*VKAPIError[6, 9])
async def limit_reached_write_handler(e: VKAPIError):
    print("ой, слишком много запросов", e)
```

Ещё у `ErrorHandler` есть параметр `redirect_arguments: bool`, который позволяет передавать в хендлер аргументы из задекорированной с помощью `catch` функции. В связке с ботом позволяет передать в хендлер контекстные аргументы из правил и мидлварей.

Подробнее про `ErrorHandler.catch` можно почитать [здесь](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/error-handler/)

## Некоторые ответы на часто задаваемые вопросы

Источник: [tutorial/faq/](https://vkbottle.readthedocs.io/ru/latest/tutorial/faq/)

### Ключевые моменты

- Asyncio: coroutine вызывается через `await`; `await` — только внутри `async` функций; вместо `time.sleep()` — `asyncio.sleep()`, вместо `requests`/`urllib3`/`vk_api` — `aiohttp` или встроенный `AiohttpClient` (`vkbottle.http`).
- Методы VK API во фреймворке присутствуют все, имена в `snake_case` (`account.get_banned` вместо `account.getBanned`), всё типизировано.
- Токены: для пользователя — vkhost.github.io, для бота — инструкция «Чат бот Быстрый старт» (у токена сообщества не все методы доступны).
- Нет нужного метода — `API.request`, `Bot.api.request`, `Message.ctx_api.request` (возвращают сырой dict-JSON), также `api.request_many(...)` + `api.APIRequest(...)` для пакетного вызова.
- `Pydantic.error_wrappers.ValidationError` — обновление типов: `pip install git+https://github.com/vkbottle/types -U`, далее issue в vkbottle или чат ВК/Телеграм.

### Asyncio

В этом разделе будет очень сжатое и простое описание работы с модулем **asyncio** и простые рекомендации как решать проблемы с блокировками.

### Что такое coroutine?

Coroutine это функция (сопрограмма), которая должна вызываться через **await**.

Когда в Python выполнение кода доходит до **await**, он останавливает выполнение в этой функции, и вернётся к ней, пока
не выполнит другие сопрограммы и не завершит работу этой функции.

Благодаря такому подходу, программа может выполнять конкурентно несколько задач одновременно без использования потоков,
а следовательно, будет экономия ресурсов железа и высокая производительность.

#### Не забывайте перед async функцией писать вначале await, иначе она не запустится

```python
import asyncio

async def get_banana() -> str: return "banana"

async def main():
    print(get_banana())  # <coroutine object get_banana at 0x...>
    print(await get_banana())  # banana

asyncio.run(main())
```

### Где надо писать **await** ?

Надо **await** писать только внутри **async** функций и больше нигде.

```python
# bad
async def foo() -> str: return "foo"

def main():
    print(await foo()) # SyntaxError: 'await' outside async function

main()
```

```python
# bad
async def main():
    print("main")

await main()  # SyntaxError: 'await' outside function
```

```python
# good
import asyncio

async def foo() -> str: return "foo"

async def main():
    print(await foo())

asyncio.run(main())
```

### Как происходит "блокировка" функции?

В асинхронном программировании блокирующие функции это все функции без конструкции **await**, работающие на принципе
IO [(Input/Output)](https://en.wikipedia.org/wiki/Input/output).

Но не все блокирующие функции плохи, так как их использование неизбежно. Главное этим не злоупотреблять.
Если заблокируете выполнение функции надолго, то ваш бот зависнет,
потому что он не остановил функцию в нужный момент, чтобы выполнять другие сопрограммы.

Конечно, интерпретатор Python не запрещает использовать синхронные решения в программировании асинхронных,
но в этом нет смысла, так как пропадают все преимущества асинхронности.

Самые частые проблемы блокировок происходят из-за функций то типу `time.sleep()`.
В **async** функциях используйте `asyncio.sleep()`.

```python
# bad
time.sleep(10)
```

```python
# good
await asyncio.sleep(10)
```

Так же распространённой проблемой долгой блокировки является модуль **requests**, **urllib3**
и ему производные API-обёртки (**vk_api**, и тп).

Они хороши для **неасинхронного** программирования, но могут произойти ситуации, когда запрос и ответ с сервера
может идти долго и бот из-за этого зависнет. Используйте для этого модуль
[aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html),
он идёт зависимостью в vkbottle или используйте встроенный AiohttpClient.

```python
# bad
async def send_httpbin_get() -> dict[str, Any]:
    r = requests.get('http://httpbin.org/get')
    if r.status_code == 200:
        js = r.model_dump_json()
        return js
```

```python
# good, recommended
# see https://vkbottle.rtfd.io/ru/latest/low-level/http-client/
from vkbottle.http import AiohttpClient

async def send_httpbin_get() -> dict[str, Any]:
    http_client = AiohttpClient()
    return await http_client.request_json('http://httpbin.org/get')
```

```python
# good
import aiohttp

async def send_httpbin_get() -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as r:
            if r.status == 200:
                js = await r.json()
                return js
```

### Почему так мало базы? Ничего не понятно

В Python написание async кода требует такого же освоения и понимания, как и других синтаксических конструкций.

Подробнее о работе с asyncio читайте в [официальной документации](https://docs.python.org/3/library/asyncio.html).

Дополнительные материалы помимо официальной документации:

- [В форме текста](https://www.google.com/search?q=python+asyncio)
- [В форме текста, на русском](https://www.google.com/search?q=python+asyncio+lang%3Aru)
- [В форме плейлистов youtube](https://www.youtube.com/results?search_query=python+asyncio&sp=EgIQAw%253D%253D)

### Какие методы присутствуют во фреймворке

Всё что есть в [официальной документации от vk.ru](https://dev.vk.ru/reference).

Синтаксис методов, параметры и ошибки аналогичны документации выше,
только методы пишутся в **snake_case**, а не **camelCase**.

```python
from vkbottle.api import API

api = API("token")

# https://api.vk.ru/method/account.ban
await api.account.ban(owner_id=1)

# https://api.vk.ru/method/account.getBanned
await api.account.get_banned(offset=0, count=1)
```

Все официальные методы, ответы и ошибки в этом фреймворке **типизированы**.
Чтобы не гадать, перебирать и постоянно заглядывать в документацию, поставьте [настоящий редактор кода](https://vkbottle.readthedocs.io/ru/latest/tutorial/recommended-ide/),
чтобы он давал подсказки.

А также настоятельно рекомендуется по ходу написания кода использовать
[тайпхинты](https://docs.python.org/3/library/typing.html),
чтобы облегчить себе жизнь и увеличить скорость написания и отладки кода.

### Как получить токен для пользователя

Самый простой способ воспользоваться сервисом [vkhost.github.io](https://vkhost.github.io)

### Как получить токен для бота

![bot_methods](https://vkbottle.readthedocs.io/ru/latest/tutorial/assets/bot_methods.jpg "bot methods")
У бота (токена от сообщества) не все методы доступны в отличие от получения токена через пользователя, учитывайте это.
На картинке красным выделен один из методов, который будет работать в ботах.

[Чат бот Быстрый старт](https://dev.vk.ru/api/bots/getting-started)

### Как отправить метод, которого нет во фреймворке

Если очень нужно использовать то, чего во фреймворке и официальной документации нет,
используйте `API.request`, `Bot.api.request` или `Message.ctx_api.request` методы.

После их выполнения вернёт словарь с json ответом, а не типизированный объект, учитывайте это.

Код ниже показывает простой пример использования VK API. Он выполнит заданный код и завершает работу.

```python
import asyncio

from vkbottle.api import API

api = API("token")

async def main():
    await api.request("users.get", {})  # Single request

    # Multiple request for one session
    async for response in api.request_many(
        [api.APIRequest("users.get", {}), api.APIRequest("groups.get", {})]
    ):
        print(response)

asyncio.run(main())
```

Для бота необходимо инициализировать класс **Bot**. В нём присутствует класс **API**, его дополнительно
**инициализировать не надо**.

```python
import asyncio
from vkbottle.bot import Bot

bot = Bot("token")

async def main():
    print(await bot.api.request("users.get", {}))  # Single request
    # Multiple request for one session
    async for response in bot.api.request_many(
        [bot.api.APIRequest("users.get", {}), bot.api.APIRequest("groups.get", {})]
    ):
        print(response)

asyncio.run(main())
```

Также доступ к классу **API** можно получить через объект Message с помощью параметра `Message.ctx_api`

```python
from vkbottle.bot import Bot, Message

bot = Bot(token="token")
admin_ids = [1, 100]

@bot.on.message(text="админы")
async def who_admins(message: Message):
    admins = [f"{adm.first_name} {adm.last_name}" for adm in (await message.ctx_api.users.get(admin_ids))]
    print((await message.ctx_api.request("users.get", {"user_ids": admin_ids})))
    await message.answer(f"Администраторы этого бота: {' '.join(admins)}")

bot.run_forever()
```

### Pydantic.error_wrappers.ValidationError

Объекты в этом фреймворке типизированы и генерируются на основе
[официальной VK-API схемы](https://github.com/VKCOM/vk-api-schema).

Они её обновляют без предупреждений и из-за этого могут произойти поломки с валидацией объектов.

Если эта ошибка произошла, попробуйте обновить типы:

```shell
pip install git+https://github.com/vkbottle/types -U
```

Если и это не помогло, пишите issue (в **vkbottle**, **не types**) или в чат ВК/Телеграмм.
