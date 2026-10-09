# High-level: интерфейс бота (VKBottle)

Локальная копия раздела документации VKBottle «Интерфейсы высокого уровня — бот»
(источник: <https://vkbottle.readthedocs.io/ru/latest/>, собрано 2026-10-08).

Покрытые страницы:

1. [High-level API (индекс)](https://vkbottle.readthedocs.io/ru/latest/high-level/)
2. [Bot](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/)
3. [Пара строк о User в vkbottle](https://vkbottle.readthedocs.io/ru/latest/high-level/user/)
4. [Bot-Labeler](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/labeler/)
5. [Bot-Multibot](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/multibot/)

---

## High-level API (индекс раздела)

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/>

Раздел «High-level API» состоит из двух подразделов — «Bot» и «Handling».
Содержание (все ссылки раздела):

**Bot**

- [Bot](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/)
- [User](https://vkbottle.readthedocs.io/ru/latest/high-level/user/)
- [Labeler](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/labeler/)
- [Blueprint](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/blueprint/)
- [Multibot](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/multibot/)

**Handling**

- [Handler](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/handler/)
- [View](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/view/)
- [Router](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/router/)
- [Return Manager](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/return-manager/)
- [State Dispenser](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/state-dispenser/)
- [Middleware](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/middleware/)
- [Rules](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/rules/)

**Отдельно**

- [Builtin Rules](https://vkbottle.readthedocs.io/ru/latest/high-level/builtin_rules.md)

Примеров кода на странице индекса нет.

---

## Bot

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/>

Инстанс бота состоит из стандартного апи, лонгпола и других частей фреймворка.

### Атрибуты

`bot.api` - [API документация](https://vkbottle.readthedocs.io/ru/latest/low-level/api/)  
`bot.router` - [Router документация](https://vkbottle.readthedocs.io/ru/latest/high-level/handling/router/)  
`bot.labeler`/`bot.on` - [Labeler документация](https://vkbottle.readthedocs.io/ru/latest/high-level/bot/labeler/)  
`bot.polling` - [Polling документация](https://vkbottle.readthedocs.io/ru/latest/low-level/polling/)  
`bot.callback` - [Callback документация](https://vkbottle.readthedocs.io/ru/latest/low-level/callback/)  
`bot.error_handler` - [Error handler документация](https://vkbottle.readthedocs.io/ru/latest/low-level/exception_handling/error-handler/)  
`bot.loop_wrapper` - [Loop Wrapper документация](https://vkbottle.readthedocs.io/ru/latest/tools/loop-wrapper/)  

### Функции

#### Long Poll API

**`bot.run_polling()`** — асинхронный запуск longpoll.

**`bot.run_forever()`** — синхронный запуск longpoll. Добавляет `run_polling` в таски
`bot.loop_wrapper` и вызывает `bot.loop_wrapper.run()`.

#### Callback API

**`bot.setup_webhook()`** — устанавливает сервер для `CallbackAPI` в сообщество.

**`bot.process_event(event)`** — передает полученное событие в роутер, для его обработки.

Примеров кода на странице нет.

> Примечание: параметры конструктора `Bot` (token, labeler, polling и т.д.) на этой
> странице документации не приводятся — страница описывает только атрибуты и методы
> запуска. В примерах смежных страниц бот создаётся как `Bot("token")`
> (см. раздел «Bot-Labeler» ниже).

---

## Пара строк о User в vkbottle

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/user/>

`User` (aka юзербот) реализован буквально "для галочки", для тех, кто очень сильно просил.

Его использование запрещено сразу несколькими [правилами вконтакте](https://vk.ru/terms):

- **6.3.9** `Использовать без специального на то разрешения Администрации Сайта автоматизированные скрипты (программы, боты, краулеры) для сбора информации на Сайте и/или взаимодействия с Сайтом и его функционалом.`
- **6.7** `Создаваемые Пользователями приложения API должны использовать только опубликованные на Сайте методы API, а также ID, защищенный ключ и сервисный ключ доступа, указанные в настройках данных приложений. Использование других методов API, а также ID, защищенного ключа и сервисного ключа доступа приложений API третьих лиц, в т.ч. приложения API Администрации Сайта, строго запрещено. Пользователь обязуется регулярно проверять перечень разрешённых методов и незамедлительно вносить корректировки в функциональность своих приложений API в соответствии с изменениями перечня. За нарушение настоящего пункта Пользователь несет предусмотренную применимым законодательством, настоящими Правилами и иными документами Администрации Сайта ответственность. Администрация Сайта при этом оставляет за собой право на защиту собственных прав и законных интересов.`

> **Внимание**
>
> Мы не несем никакой ответственности за ваши аккаунты, а также не обязываемся помогать
> вам в решении проблем, которые возникают в процессе использования этой части фреймворка.

Помимо ограничений от Вконтакте, наличие юзерботов накладывает ограничения на сам
фреймворк из-за огромной разницы в `User Long Poll API` и `Bot Long Poll API`.

Наглядным примером этому служат универсальные для обоих частей фреймворка типы,
не поддерживающие специфичные функции. А также необходимость использовать дженерики
в `Rule` и `Middleware`.

Если вам нужно использовать юзербота, то импортировать его и его составляющие можно
из `vkbottle.user`.

К ним относятся:

- `User`
- `Blueprint`
- `UserLabeler`
- `Message`
- `run_multibot`
- `views`

Все остальное идентично обычным ботам.

Примеров кода на странице нет.

---

## Bot-Labeler

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/labeler/>

Удобная оболочка над роутерами. С помощью лейблера создаются хендлеры. Может быть
использовано в качестве портабельного диспатчера.

Имеет метод `load`, который должен загружать хендлеры и мидлвари в текущий лейблер из
переданного. Может быть использовано для разбивания кода на много частей.

### Пример

#### bot.py

```python
from vkbottle import Bot
from routes import labelers

bot = Bot("token")

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()
```

#### routes/__init__.py

```python
from . import greetings, goodbyes

labelers = [greetings.bl, goodbyes.bl]
```

#### routes/greetings.py

```python
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

@bl.message(text=["привет", "хай", "здравствуй"])
async def greeting(message: Message):
    await message.answer("Привет, друг")
```

#### routes/goodbyes.py

```python
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

@bl.message(text=["пока", "до свидания"])
async def greeting(message: Message):
    await message.answer("До новых встреч")
```

---

## Bot-Multibot

Источник: <https://vkbottle.readthedocs.io/ru/latest/high-level/bot/multibot/>

Мультибот запускает несколько лонгполов на переданных вами API и обрабатывает получаемые
ивенты со всех лонгполов с помощью одного основного бота. Эта идея встречается например
в чат-менеджере с их субменеджерами и может быть использована в разных целях.

Пример мультибота можно увидеть [здесь](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/multibot.py).

### Запуск

Для запуска такого бота вам понадобится `run_multibot`, он добавляет `run_polling` в
таски и запускает `eventloop`. Его можно импортировать из `vkbottle.bot`:

```python
run_multibot(bot, apis, polling_type=BotPolling)
```

Основному боту передавать токен для создания API не нужно.

- `apis` — любой итерируемый объект (то есть можно легко сделать свой генератор при желании)
- `polling_type` — если вы кастомизируете поллинг вы можете изменить это значение
