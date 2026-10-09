# Tools: базовые инструменты (VKBottle)

Локальная копия документации VKBottle по базовым инструментам. Все примеры кода скопированы дословно со страниц-источников.

## Индекс раздела «Дополнительные инструменты»

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/](https://vkbottle.readthedocs.io/ru/latest/tools/)

Раздел «Дополнительные инструменты» объединяет следующие страницы:

- [Auth Flows](https://vkbottle.readthedocs.io/ru/latest/tools/auth/)
- [Formatting](https://vkbottle.readthedocs.io/ru/latest/tools/formatting/)
- [Keyboard](https://vkbottle.readthedocs.io/ru/latest/tools/keyboard/)
- [Loop Wrapper](https://vkbottle.readthedocs.io/ru/latest/tools/loop-wrapper/)
- [Message Event](https://vkbottle.readthedocs.io/ru/latest/tools/message-event/)
- [Storage](https://vkbottle.readthedocs.io/ru/latest/tools/storage/)
- [Template](https://vkbottle.readthedocs.io/ru/latest/tools/template/)
- [Uploaders](https://vkbottle.readthedocs.io/ru/latest/tools/uploaders/)
- [VKScript](https://vkbottle.readthedocs.io/ru/latest/tools/vkscript/)
- [Waiter Machine](https://vkbottle.readthedocs.io/ru/latest/tools/waiter-machine/)

В данном файле собраны базовые страницы: Keyboard, Uploaders, Formatting, Template, Message Event, Storage.

## Keyboard (построение клавиатур)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/keyboard/](https://vkbottle.readthedocs.io/ru/latest/tools/keyboard/)

Внимание: подразумевается, что вы уже ознакомились с [документацией ВК по клавиатуре](https://dev.vk.ru/api/bots/development/keyboard).

Создавать клавиатуры в vkbottle очень просто. Импортируйте `Keyboard`, `KeyboardButtonColor` и нужные вам `action` (например: `Text`, `OpenLink`, `Location`, `VKApps`, `Callback`).

Создайте объект клавиатуры:

```python
from vkbottle import Keyboard, KeyboardButtonColor, Text
keyboard = Keyboard(one_time=True, inline=False)
# О параметрах one_time и inline вы можете прочитать в документации к апи вконтакте
keyboard.add(Text("Кнопка 1"), color=KeyboardButtonColor.POSITIVE)
# Первая строка (ряд) добавляется автоматически
keyboard.row()  # Переходим на следующую строку
keyboard.add(Text("Кнопка 2"))
keyboard.add(Text("Кнопка 3", payload={"command": 3}))
```

Теперь, чтобы получить `json` для отправки клавиатуры в сообщении можно использовать метод объекта клавиатуры `get_json()`.

Например:

```python
await message.answer(message="Смотри сколько кнопок!!", keyboard=keyboard.get_json())
```

Для клавиатуры доступен интерфейс билдера, поэтому весь код выше можно заменить этим:

```python
from vkbottle import Keyboard, KeyboardButtonColor, Text

# ...
keyboard = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Кнопка 1"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Кнопка 2"))
    .add(Text("Кнопка 3", payload={"command": 3}))
).get_json()

await message.answer(
    message="Смотри сколько кнопок!!",
    keyboard=keyboard
)
```

Примечание: для того, чтобы удалить клавиатуру у пользователя, вам нужно отправить `EMPTY_KEYBOARD`.

Ключевые моменты:

- `Keyboard(one_time=True, inline=False)` — параметры `one_time` (одноразовая) и `inline` (внутриклавиатурные/inline-кнопки) описаны в документации VK API.
- Кнопки добавляются методом `.add(...)`, цвет кнопки задаётся через `KeyboardButtonColor` (в примере — `KeyboardButtonColor.POSITIVE`).
- Переход на новую строку — метод `.row()`; первая строка создаётся автоматически.
- В кнопку можно передать `payload` (полезная нагрузка), например `Text("Кнопка 3", payload={"command": 3})`.
- `keyboard.get_json()` возвращает JSON клавиатуры для отправки в `message.answer(..., keyboard=...)`.
- Интерфейс билдера: цепочка вызовов `.add(...).row().add(...)` с завершением `.get_json()`.
- Для удаления клавиатуры отправляется `EMPTY_KEYBOARD`.

## Uploaders (загрузка медиа)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/uploaders/](https://vkbottle.readthedocs.io/ru/latest/tools/uploaders/)

Загрузка медиа разного типа в ВК. Существует несколько типов аплоадеров:

- `audio` — загрузка аудио
- `doc` — загрузка документов разного типа
- `photo` — загрузка фото
- `speech` — загрузка аудиофайлов для распознавание речи
- `video` — загрузка видео

### Пример

```python
from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot

bot = Bot("token")
photo_uploader = PhotoMessageUploader(bot.api)


@bot.on.message(text="photo")
async def handler(message):
    photo = await photo_uploader.upload(
        file_source="photo.png",
        peer_id=m.peer_id,
    )
    await message.answer(attachment=photo)

bot.run_forever()
```

### Интерфейс аплоадера

Аплоадер принимает объект `API` при инициализации.

Аплоадеры имеет два метода:

- `.upload(...)`
- `.raw_upload(...)`

Оба метода имеют одинаковый интерфейс, но различаются в том, что первый метод возвращает готовую строку аттачмента, а второй — словарь с ответом сервера.

Внимание: не все аплоадеры имеют метод `upload`, для них невозможно вернуть строку аттачмента.

Все аплоадеры различаются методом получения сервера. Получить сервер аплоадера можно с помощью метода `.get_server(...)`.

Так же у аплоадеров есть методы базового класса, одинаковые для всех:

- `.upload_files(url, files)` — загрузка файлов методом POST
- `.get_bytes_io(data)` — приводит сырые байты в подходящий для вк вид
- `.generate_attachment_string(attachment_type, owner_id, item_id, access_key)` — делает строку, которую вк принимает, как медиа для отправки
- `.read(file_source)` — читает файл, если `file_source` строка, а если байты — возвращает их

Обычно нужен только метод `upload`.

### Виды аплоадеров

- Для фото:
  - `PhotoMessageUploader` — загрузка в сообщение
  - `PhotoToAlbumUploader` — загрузка в альбом
  - `PhotoWallUploader` — загрузка на стену
  - `PhotoFaviconUploader` — загрузка аватарки
  - `PhotoChatFaviconUploader` — загрузка аватарки беседы
  - `PhotoMarketUploader` — загрузка картинки для товара
- Для документов:
  - `DocWallUploader` — загрузка документов на стену
  - `DocMessagesUploader` — загрузка документов в сообщение
  - `VoiceMessageUploader` — загрузка голосовых сообщений
  - `GraffitiUploader` — загрузка граффити
- `AudioUploader` — загрузка аудио
- `VideoUploader` — загрузка видео

### Дополнительные примеры

- [Uploaders example](https://github.com/vkbottle/vkbottle/blob/master/examples/high-level/uploaders_example.py)

## Formatting (форматирование текста)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/formatting/](https://vkbottle.readthedocs.io/ru/latest/tools/formatting/)

Формирование форматированного текста осуществляется с помощью вспомогательного класса `Formatter`, который наследует класс `str` и имеет два перегруженных метода: `format`, `format_map`.

```python
from vkbottle.tools.formatting import Formatter
```

Доступные типы форматирования:

- `bold` — полужирный.
- `italic` — курсив.
- `url` — ссылка.
- `underline` — подчеркнутый.

Примечание: для типов форматирования специально реализованы такие же по названию функции, которые импортируются из модуля `vkbottle.tools.formatting`.

Метод `format` принимает `*args`, `**kwargs` и форматирует строку по специальным заменам, которые заключаются в `{}`.

Например:

```python
Formatter("Hi, {}.").format("Alex")  # Hi, Alex.
Formatter("Hi, {name}.").format(name="Maria")  # Hi, Maria.
```

Метод также поддерживает специальные идентификаторы:

- bold
- italic
- underline

Пример использования:

```python
Formatter("{:bold}, nice formatting!").format("Wow")  # Wow, nice formatting!
Formatter("{framework:italic} has been around for over 5 years!").format(framework="vkbottle")  # vkbottle has been around for over 5 years!
```

Для того, чтобы объединить типы форматов, используется синтаксис объединения через символ `+`.

```python
Formatter("Very cool {:bold+italic} ^_^").format("bold-italic message")  # Very cool bold-italic message ^_^
```

Метод `format_map` работает так же, как и `format`, за исключением того, что метод принимает один аргумент типа `Mapping`, который передается в метод `format`.

```python
Formatter("My bestie is {bestie:underline}").format_map({"bestie": "telegrinder")  # My bestie is telegrinder
```

Объект `Formatter` имеет 2 свойства для того, чтобы получить форматирование в виде `json`:

- `format_data` — словарь `{"version": ..., "items": [...]}`.
- `raw_format_data` — сырой объект `format_data`.

Примечание: `format_data` необходим для методов, которые могут работать с форматированным текстом, например: `messages.send`. Более подробно ознакомиться можно в [документации VK API](https://dev.vk.ru/ru/reference/objects/message#format_data).

Класс `Format` необходим для представления типа форматирования, таких как: `bold`, `italic` и т. д. Класс поддерживает оператор `+=`, конкатенацию строк и самих типов-форматов.

```python
from vkbottle.tools.formatting import Format
```

Пример использования функций-форматирования:

```python
bold("Hello, ") + italic("World!")  # Hello, World! ('Hello, ' is bold, 'World!' is italic)
"Hello, " + italic("World!")  # Hello, World! ('World!' is italic)
bold("Hello") + ", " + italic("World!")  # Hello, World! ('Hello' is bold, 'World!' is italic)
bold("vkbottle documentation:") + " " + url(italic("click me"), href="vkbottle.readthedocs.io/ru/latest")  # vkbottle documentation: click me ('click me' has an url)
```

`Format` имеет 2 метода для того, чтобы получить форматирование в виде `json`:

- `as_data` — словарь `{"version": ..., "items": [...]}`.
- `as_raw_data` — сырой объект `as_data`.

Пример использования с методом `BaseMessageMin.answer()`:

```python
await message.answer(Formatter("Hello, {:bold}!").format("World"))
await message.answer(underline(bold("Hello") + ", " + italic("World!")))
```

Ключевые моменты:

- `Formatter` (наследник `str`) с методами `format(*args, **kwargs)` и `format_map(mapping)`.
- Типы форматирования: `bold`, `italic`, `url`, `underline`; одноимённые функции импортируются из `vkbottle.tools.formatting`.
- Идентификаторы в фигурных скобках: `{:bold}`, `{name:italic}`; объединение типов через `+`: `{:bold+italic}`.
- Класс `Format`: оператор `+=`, конкатенация строк и типов-форматов; методы `as_data` / `as_raw_data` для JSON-представления.
- Свойства `Formatter`: `format_data` (словарь `{"version": ..., "items": [...]}`) и `raw_format_data`.

## Template (шаблоны сообщений)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/template/](https://vkbottle.readthedocs.io/ru/latest/tools/template/)

Посмотреть как применять темплейты можно [здесь](https://dev.vk.ru/api/bots/development/messages#Шаблоны%20сообщений).

Для создания темплейтов есть `template_gen`.

Импортируйте нужные компоненты:

```python
from vkbottle import TemplateElement, template_gen

my_template = template_gen(
    TemplateElement(...), # о том как нужно сочетать параметры можно
    TemplateElement(...)  # прочитать в документации Вконтакте выше
)

# my_template - готовый для отправки json
# ...
await message.answer("Держи карусель!", template=my_template)
```

Ключевые моменты:

- `template_gen(TemplateElement(...), TemplateElement(...))` собирает карусель (шаблон сообщения) из компонентов `TemplateElement`.
- Результат — готовый для отправки JSON, передаётся в `message.answer(..., template=my_template)`.
- Сочетание параметров `TemplateElement` описано в документации ВКонтакте (ссылка выше).

## Message Event (обработка callback-кнопок)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/message-event/](https://vkbottle.readthedocs.io/ru/latest/tools/message-event/)

Обработка `callback` кнопок выходит на новый уровень:

```python
from vkbottle import GroupEventType
from vkbottle.bot import MessageEvent

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def handle_message_event(event: MessageEvent):
    await event.show_snackbar("Сейчас я исчезну")
```

- Никакого `object`. Всё находится уже в `event`, вместе с `group_id`.
- Поддержка всех генераторов `event-data` при помощи соответствующими функциями.
- Поддержка рулзов, связанных с `payload`.
- Так же есть `message_edit` и `message_send`.

### Старый способ

```python
from vkbottle import GroupEventType, GroupTypes, ShowSnackbarEvent

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent):
    await event.ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=ShowSnackbarEvent(text="Сейчас я исчезну").model_dump_json(),
    )
```

[Полноценный пример](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/callback_buttons.py)

Ключевые моменты:

- События callback-кнопок обрабатываются через `bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)`.
- В новом способе данные события доступны напрямую в `event` (включая `group_id`), без обращения к `object`.
- Готовые методы: `event.show_snackbar(...)`, а также `message_edit` и `message_send`.
- Старый способ: `dataclass=GroupTypes.MessageEvent`, ответ через `event.ctx_api.messages.send_message_event_answer(...)` c `event_data=ShowSnackbarEvent(...).model_dump_json()`.

## Storage (хранилища)

Источник: [https://vkbottle.readthedocs.io/ru/latest/tools/storage/](https://vkbottle.readthedocs.io/ru/latest/tools/storage/)

Хранилища как бы это не было очевидно нужны чтобы хранить информацию в формате `ключ`: `значение`.

Все хранилища имеют такие методы:

- `get(key)`
- `set(key, value)`
- `delete(key)`
- `contains(key)`

### CtxStorage

Контекстное хранилище как и любое другое хранилище удобно тем что его можно открыть и изменить из любого места в коде, а главное оно доступно из-коробки, [смотрите пример](https://github.com/vkbottle/vkbottle/tree/master/examples/low-level/ctx_storage_example.py)

### Создание своего хранилища

Если вы хотите создать свое хранилище например на основе `Rabbit MQ` вы можете это легко сделать:

- Наследуйтесь от `ABCStorage`.
- Имплементируйте методы `get`, `set`, `delete` и `contains` (указаны ранее) c подключением к `Rabbit MQ`.

Ключевые моменты:

- Хранилище — структура `ключ: значение` с методами `get`, `set`, `delete`, `contains`.
- `CtxStorage` — контекстное хранилище, доступное из коробки и из любого места кода.
- Своё хранилище создаётся наследованием от `ABCStorage` с имплементацией методов `get`, `set`, `delete`, `contains`.
