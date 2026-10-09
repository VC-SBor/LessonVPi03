# High-level: хендлинг (VKBottle)

Локальная копия документации VKBottle по разделу «Хендлинг» и встроенным правилам.

Страницы-источники:

- [Handler](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/handler/)
- [Router](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/router/)
- [View](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/)
- [Return Manager](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/return-manager/)
- [State Dispenser](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/state-dispenser/)
- [Middleware](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/)
- [Rules](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/rules/)
- [Все встроенные правила](https://vkbottle.readthedocs.io/ru/latest/high-level/builtin-rules/)

## Handler

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/handler/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/handler/)

### Что такое хендлер

Хендлеры это конечная точка в обработке событий. Хендлеры могут быть блокирующими (если нашелся подходящий хендлер другие уже не проверяются и не выполняются) и не блокирующими (в таком случае количество выполняемых хендлеров не ограничено и зависит от того какие пройдут). По умолчанию все хендлеры являются блокирующими.

Хендлеры помечаются (лейблируются) с помощью декораторов. За это отвечает `Labeler` high-level инстанс с которым вы работаете. Пример с ботом:

```python
from vkbottle.bot import Bot, Message

bot = Bot("token")

@bot.on.message()
async def any_message(message: Message):
    await message.answer("Привет я бот")

bot.run_forever()
```

### Хендлеры ботов

#### `message`

Этот хендлер показан в примере выше. Хендлер на все сообщения (и из чата, и из личных сообщений).

#### `chat_message`

Хендлер на сообщения из чатов.

#### `private_message`

Хендлер на сообщения из личных диалогов.

> Примечание
>
> Типы хендлеров выше не делают ничего необычного, просто оперируют предустановленным правилом `PeerRule`:
>
> - в `message` он не предустанавливается
> - в `chat_message` - `PeerRule(True)`
> - в `private_message` - `PeerRule(False)`

### Аргументы декоратора

В качестве аргументов декоратор принимает инстансы правил (`ABCRule`), а в качестве `kwargs` он принимает значение из custom_rules (подробнее в [туториале](https://vkbottle.readthedocs.io/ru/latest/tutorial/rules/)).

> Примечание
>
> Если правило вернуло словарь, то он будет распакован и передан в качестве аргументов в хендлер, если он принимает их:

```python
# Кастомное правило MyRule возвращает словарь `{"some_key": "some_value"}`
@bot.on.message(MyRule())
async def some_key_handler(message: Message, some_key: str):
    await message.answer(f"some_key={some_value}")

@bot.on.message(MyRule())
async def regular_handler(message: Message):
    await message.answer("Этот хендлер не принимает аргумент 'some_key', поэтому он и не был передан")

@bot.on.message(MyRule())
async def kwargs_handler(message: Message, **kwargs: Any):
    await message.answer(f"В хендлере переданы аргументы: {kwargs}")
    # В хендлере переданы аргументы: {"some_key": "some_value"}
```

## Router

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/router/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/router/)

Роутер - компонент, который принимает запрос и передает его в подходящий [view](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/). Также роутер переватывает ошибки, которые возникают во время выполнения `view`.

### Атрибуты роутера

- `views` - словарь с view, которые будут обрабатываться роутером
- `state_dispenser` - компонент, который отвечает за хранение состояний ([документация](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/state-dispenser/))
- `error_handler` - компонент, который отвечает за обработку ошибок ([документация](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/error-handler/))

### Методы роутера

- `route` - метод, который принимает событие и контекст `API` и передает его в подходящий `view`
- `construct` - метод, который принимает атрибуты роутера и устанавливает их
- `add_view` - метод, который принимает имя `view` и сам `view` и добавляет его в словарь `views`
- `view` - декоратор, который принимает имя `view` и сам `view` и добавляет его в словарь `views`

## Handling-View

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/)

View являются блокирующими менеджерами хендлеров. Если `process_event` у view вернул `True` то другие view уже не будут проверяться.

Процедура поиска view обрабатывающего ивент проста:

Сначала обрабатывается `process_view` который должен вернуть `boolean`-значение. Если вернулось `True` то поиск view прекращается и вызывается `handle_event` который отвечает за подбор хендлера.

### `register_middleware(BaseMiddleware)`

Добавляет мидлварь в `view.middlewares`.

### Написание view

> Примечание
>
> View - это "большой хендлер", имплементирующий индивидуальную логику работы с мидлварями, стейт менеджером и производными хендлеров
>
> Кастомные view нужны обычно для создания среды обработки какого-то ивента или группы ивентов

Посмотреть пример view для сообщений [можно здесь](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/dispatch/views/bot/message.py).

У каждого view существует минимум **4** атрибута:

- `handlers` - лист из `ABCHandler`
- `middlewares` - сет из классов `BaseMiddleware`
- `middleware_instances` - лист объектов `BaseMiddleware`, используется в `view.pre_middleware` и `view.post_middleware`
- `handler_return_manager` - `BaseReturnManager`

Из них **рекомендуются** 2 атрибута, `handlers` и `middlewares`.

Эти атрибуты впоследствии рекомендуется использовать в `handle_event` для запуска мидлварей и поиска хендлера.

```python
from vkbottle import ABCView, MiddlewareResponse
from vkbottle_types.events.bot_events import PollVoteNew

class VoteView(ABCView):
    def __init__(self):
        super().__init__()

    async def process_event(self, event: dict[str, Any]): -> bool:
        # Эта функция принимает ивент в форме словаря,
        # она должна определить подходит ли ивент под
        # текущий view или нет и вернуть соответствующее
        # boolean-значение
        return event["type"] == "poll_vote_new"

    async def handle_event(
        self, event: dict, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ):
        # Эта функция полностью обрабатывает
        # полученный ивент
        vote = PollVoteNew(**event)

        # Здесь можно обозначить стейт-каст
        # по определенному ключу для объекта
        vote.object.state_peer = await state_dispenser.cast(vote.object.user_id)

        # Здесь можно имплементировать стандартное поведение мидлварей
        # Например, если `pre_middleware` вернул что-либо, то в одном из
        # мидлварей был вызван `self.stop(...)` - обработка сразу останавливается
        mw_instances = await self.pre_middleware(vote)
        if mw_instances is None:
            return logger.info("Обработка остановлена, pre_middleware вернул ошибку")

        # `handlers` и `handle_responses` нужны для post мидлварей
        handlers = []
        handler_responses = []
        context = dict()

        for handler in self.handlers:
            if not await handler.filter(vote, context):
                continue

            handler_responses.append(await handler.handle(vote, **context))
            handlers.append(handler)

            if handler.blocking:
                break

        # Запуск post-мидлварей
        await self.post_middleware(mw_instances, handler_responses, handlers)
```

Поздравляю вы написали свой view! Теперь можно перейти к регистрации хендлеров, но для этого потребуется их создать, можно воспользоваться `FromFuncHandler`:

```python
from vkbottle.bot import Bot, rules, BotLabeler
from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle_types.events.bot_events import PollVoteNew


async def vote_up(vote: PollVoteNew):
    print(
        "{} со стейтом {} голосует за {}".format(
            vote.object.user_id, vote.object.state_peer, vote.object.option_id
        )
    )

async def vote_up_admin(vote: PollVoteNew):
    print("Админ проголосовал за {}", vote.object.option_id)

my_view = VoteView()
my_view.handlers = [
    FromFuncHandler(
        vote_up_admin,
        rules.FuncRule(lambda v: v.object.user_id in admin_ids),
    ),
    FromFuncHandler(vote_up),
]

class MyLabeler(BotLabeler):
    def views(self) -> dict[str, "ABCView"]:
        # Из views должны быть возвращены все view которые
        # будут позже обрабатываться роутером
        return {"vote_view": my_view}

bot = Bot()
bot.labeler = MyLabeler()
admin_ids = [1]
```

Бот с `VoteView` готов.

## Return-Manager

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/return-manager/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/return-manager/)

Для каждого [view](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/) можно установить `handler_return_manager`. Этот менеджер будет обрабатывать то, что возвращается из хендлеров.

По умолчанию менеджеры предустановлены в некоторых `view`.

Например, для сообщений:

- строка отправится в качестве текста сообщения
- каждый элемент кортежа или листа будет отправлен как сообщение
- словарь распакуется в метод отправки сообщения

Вот так выглядит его реализация:

```python
from vkbottle import BaseReturnManager
from vkbottle.bot import Message
from typing import Union


class BotMessageReturnHandler(BaseReturnManager):
    @BaseReturnManager.instance_of(str)
    async def str_handler(self, value: str, message: Message, _: dict[str, Any]):
        await message.answer(value)

    @BaseReturnManager.instance_of((tuple, list))
    async def iter_handler(self, value: tuple | list, message: Message, _: dict[str, Any]):
        [await message.answer(str(e)) for e in value]

    @BaseReturnManager.instance_of(dict)
    async def dict_handler(self, value: dict, message: Message, _: dict[str, Any]):
        await message.answer(**value)
```

---

Первым аргументов в хендлер приходит само значение, что было получено из хендлера, вторым - объект ивента, третьим - данные из рулзов и мидлварей.

---

Хендлеры оборачиваются в декоратор `instance_of`, который принимает в качестве единственного аргумента тип или кортеж типов.

## State-Dispenser

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/state-dispenser/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/state-dispenser/)

StateDispenser'ы нужны, чтобы организовывать веточную систему организации пользователя. Сложное меню - стейты, квиз - стейты, какая-то игра - стейты.

### Методы StateDispenser

#### `get`

Возвращает `StatePeer` (если запись на запрошенный peer_id существует) или `None` (если нет). На вход получает `peer_id`.

#### `set`

Делает запись. На вход получает `peer_id` и `state`.

#### `delete`

Удаляет запись. На вход получает `peer_id`.

### Работа со стейтами

Получить стейт можно из объекта любого ивента `event.state_peer.state`.

Чтобы задать стейт пользователю, достаточно воспользоваться вышеупомянутым методом `set`.

Ловить пользователей со стейтами в хендлерами можно с помощью `StateRule`.

Пример:

```python
from vkbottle import BaseStateGroup
from vkbottle.bot import Message, Bot

bot = Bot("t")

class SuperStates(BaseStateGroup):
    AWKWARD_STATE = "awkward"
    CONFIDENT_STATE = "confident"
    TERRIFYING_STATE = "terrifying"

@bot.on.message(state=SuperStates.AWKWARD_STATE)  # StateRule(SuperStates.AWKWARD_STATE)
async def awkward_handler(message: Message):
    await message.answer("oi awkward")

@bot.on.message(lev="/die")
async def die_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
    return "ok"

bot.run_forever()
```

> Примечание
>
> `.set()` может принимать `**payload` который позже доступен как словарь из `message.state_peer.payload`

```python
# ... In handler:
await bot.state_dispenser.set(message.peer_id, SuperStates.TERRIFYING_STATE, something=1)
# ... With state:
print(message.state_peer.payload["something"])  # 1
```

## Middleware

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/)

### Общее

Мидлварь должен имплементировать методы `pre` и/или `post`. `pre` вызывается до поиска хендлеров, а `post` после.

Мидлвари всегда распаковываются из `labeler`.

Абстрактный класс для мидлварей - `BaseMiddleware`.

Конструктор принимает ивент в качестве аргумента.

`pre`/`post` не принимают аргументов, должны возвращать `None`:

- `self.stop(ошибка)` - исполнение view срочно останавливается
- `self.send({ключ: значение})` - в контекст добавляются аргументы (ключ - имя аргумента)

### Атрибуты `BaseMiddleware`

- `event` (сам евент, как указать его тип, смотрите ниже)
- `view: ABCView` (с которым был обработан ивент)
- `handle_responses: list` (все то что вернули хендлеры по порядку их исполнения)
- `handlers: list[ABCHandler]` (все хендлеры что были исполнены)

### Тип ивента в дженерике

Тип ивента, который будет обрабатывать мидлварь, указывается в дженерике конструктора мидлвари. Например:

```python
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

class MyMiddleware(BaseMiddleware[Message]):
    ...
```

Для `message_view` это `Message`, а для `raw_event_view` словарь.

[Больше примеров можно посмотреть здесь](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/middleware_example.py).

## Rules

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/handling/rules/](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/rules/)

### Labeler Custom Rules

Список keyword-аргументов декораторов хендлеров и правил, из которых они создаются:

- `from_chat` - от `PeerRule`
- `mention` - от `MentionRule`
- `command` - от `CommandRule`
- `from_user` - от `FromUserRule`
- `peer_ids` - от `FromPeerRule`
- `sticker` - от `StickerRule`
- `attachment` - от `AttachmentTypeRule`
- `levenshtein` и `lev` - от `LevenshteinRule`
- `length` - от `MessageLengthRule`
- `action` - от `ChatActionRule`
- `payload` - от `PayloadRule`
- `payload_contains` - от `PayloadContainsRule`
- `payload_map` - от `PayloadMapRule`
- `func` - от `FuncRule`
- `coroutine` и `coro` - от `CoroutineRule`
- `state` - от `StateRule`
- `state_group` - от `StateGroupRule`
- `regexp` и `regex` - от `RegexRule`
- `macro` - от `MacroRule`
- `text` - от `VBMLRule`
- `fuzzy` - от `FuzzyTextRule`

> Внимание
>
> Все встроенные рулзы работают только с объектами `Message` и `MessageEvent` из `vkbottle.bot`, для обработки сырых евентов нужно писать свою реализацию.

Посмотреть логику рулзов можно [здесь](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/dispatch/rules/base.py).

## Все встроенные правила

Источник: [https://vkbottle.readthedocs.io/ru/latest/high-level/builtin-rules/](https://vkbottle.readthedocs.io/ru/latest/high-level/builtin-rules/)

### PeerRule

`PeerRule(from_chat: bool = True)`

Нужно для ограничения источника сообщения, `PeerRule(from_chat=False)` например, будет указывать на то, что сообщение должно быть из личного диалога с ботом.

### MentionRule

`MentionRule(mention_only: bool = False)`

Используется для проверки на то, что бот был упомянут в сообщении. Параметр `mention_only` используется чтобы указать, что кроме упоминания в сообщении быть ничего не должно, в ином случае из сообщения удаляется упоминание чтобы другие правила могли обработать уже сам текст.

### CommandRule

```python
CommandRule(
    command_text,
    prefixes,
    args_count = 0,
    sep = " "
)
```

Используется для того чтобы реагировать на команды.

Команда выглядит так:

```text
{prefix}{command_text}{sep.join(args)}
```

В `command_text` можно передать несколько вариантов названия команды.

В `prefixes` можно передать несколько возможных префиксов (например: '/', '!').

В `args_count` передается количество обязательных аргументов с `sep` в качестве разделителя.

### VBMLRule

```python
VBMLRule(
    pattern,
    patcher = None,
    flags = None
)
```

Используется в качестве парсера текстов сообщений. Разметка vbml исторически была сделана специально для фреймворка, чтобы легко писать паттерны с валидируемыми аргументами.

Пример:

```python
rule = VBMLRule("/cmd <eggs:int>")
rst = await rule.check(Message(text="/cmd 11", ...))
assert rst == {"eggs": 11}
```

Больше документации [CLICK 🤩](https://github.com/tesseradecade/vbml/blob/master/docs/index.md).

### RegexRule

`RegexRule(regexp)`

Используется для проверки на соответствие текста сообщения регулярному выражению.

### StickerRule

`StickerRule(sticker_ids = None)`

Используется для того чтобы отлавливать отправку стикеров в сообщении. Если sticker_ids = None, то проходить будет любое сообщение содержащее стикер.

### FromPeerRule

`FromPeerRule(peer_ids)`

Используется для отлова сообщений отправленных пользователем/группой с одним из указанных ID.

### AttachementTypeRule

`AttachementTypeRule(attachment_types)`

Используется для отлова сообщений с указанным типом вложений (например: `photo`).

### ForwardMessagesRule

Используется для того, чтобы проверить, что сообщение содержит в себе вложенные сообщения.

### ReplyMessageRule

`ReplyMessageRule(reply_message: bool = True)`

### GeoRule

Используется для того чтобы отлавливать сообщения с геометкой.

### LevenshteinRule

> Deprecation
>
> На данный момент обсуждается удаление этого правила из новых версий из-за его неоптимальности. Вместо этого рекомендуется использовать `FuzzyTextRule`

`LevenshteinRule(levenshtein_texts, max_distance: int = 1)`

Используется для fuzzy string matching'а.

Может принимать max_distance - максимальное отклонение от заданного текста.

### FuzzyTextRule

`FuzzyTextRule(texts, min_ratio: float = 0.7)`

Используется для fuzzy string matching'а.

Настраивается через min_ratio - минимальная *похожесть* сообщения с переданным текстом (от 0 до 1).

### MessageLengthRule

`MessageLengthRule(min_length: int)`

Используется для ограничения минимальной длины текстового сообщения.

### ChatActionRule

`ChatActionRule(chat_action_types)`

Используется для отлова событий в беседах (например: `chat_invite_user`). [Документация ВК по chat actions](https://dev.vk.ru/reference/objects/message#action)

### PayloadRule

`PayloadRule(payload)`

Проверяет что у сообщения payload равен одному из данных.

### PayloadContainsRule

`PayloadContainsRule(payload_part)`

Проверяет что в payload сообщения содержит данную часть.

### PayloadMapRule

`PayloadMapRule(payload_map)`

Используется для создания ассоциаций необходимых значений и типов в payload сообщений.

Например, такой payload как:

```json
{"name": "boba", "data": {"action": "do", "number": 12}}
```

Выражается таким payload map:

```python
PayloadMapRule({"name": str, "data": {"action": str, "number": int}})
```

Вместо типа данных так же можно передать валидатор (`ABCValidator`), функцию (она будет вызвана со значением из полезной нагрузки сообщения) или literal-значения, например, если `"name"` в полезной нагрузке должен быть всегда `"boba"`, можно указать нужное значение в маппинге.

Пример:

```python
PayloadMapRule(
    {
        "name": "boba",
        "data": {
            "action": lambda x: x in ("do", "undo"),
            "number": int,
        }
    }
)
```

### FromUserRule

`FromUserRule(from_user: bool = True)`

Используется для проверки что сообщение было отправлено пользователем, а не ботом.

При `from_user = False`, работает в обратную сторону, проверяет что сообщение отправлено ботом.

### FuncRule

`FuncRule(func)`

Принимает функцию, которая будет вызвана с единственным аргументом - событием. Функция должна вернуть bool или dict с обновлением контекста.

### CoroutineRule

`CoroutineRule(coro)`

Ответ проверки правила получается из переданной корутины.

### StateRule

`StateRule(state)`

Нужно для стейт-машины, проверяет что источник ивента находится в переданном состоянии.

Если переданное состояние = None, то правило проверяет чтобы источник не находился ни в каком состоянии.

### StateGroupRule

`StateGroupRule(state_group)`

Проверяет что пользователь находится в нужной коллекции состояний.
