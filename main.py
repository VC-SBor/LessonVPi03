"""ВК-бот на vkbottle (LongPoll API).

Две задачи:
1. приветствовать пользователей, вошедших в беседу;
2. отвечать на входящие сообщения с помощью AI (ProxyAPI, gpt-4.1-mini).

Запуск: python main.py
"""

from __future__ import annotations

from vkbottle.bot import Bot, Message
from vkbottle.modules import logger

from ai_client import AIBillingError, AIError, ProxyAIClient
from config import ConfigError, Settings, load_settings

GREETING = (
    "👋 Привет, [id{member_id}|{name}]! "
    "Рады видеть тебя в беседе. Напиши что-нибудь — я отвечу с помощью ИИ."
)
AI_FALLBACK = "😔 Не получилось получить ответ ИИ. Попробуйте позже."
# 402 = на балансе ProxyAPI нет денег: повторная попытка не поможет,
# поэтому не обнадёживаем «попробуйте позже»
AI_NO_BALANCE = "😔 Сервис ИИ сейчас недоступен. Приносим извинения."


def build_bot(settings: Settings) -> Bot:
    """Создаёт бота со всеми хендлерами по настройкам из .env."""
    ai = ProxyAIClient(
        base_url=settings.ai_base_url,
        api_key=settings.proxyapi_key,
        model=settings.ai_model,
        system_prompt=settings.ai_system_prompt,
        history_limit=settings.ai_history_limit,
    )

    bot = Bot(token=settings.vk_token)

    # 1) Приветствие: ловим события входа в беседу (ChatActionRule).
    #    События: "chat_invite_user" — пригласили по ссылке на профиль,
    #    "chat_invite_user_by_link" — вошли по ссылке-приглашению в беседу.
    @bot.on.chat_message(action=["chat_invite_user", "chat_invite_user_by_link"])
    async def greet_new_user(message: Message) -> None:
        member_id = message.action.member_id if message.action else None
        if member_id is None or member_id <= 0:
            # в беседу добавили группу или бота — приветствие не отправляем
            return

        try:
            users = await bot.api.users.get(member_id)
            name = users[0].first_name if users else "новый участник"
        except Exception as error:  # noqa: BLE001 — имя не критично для приветствия
            logger.warning("Не удалось получить имя участника {}: {}", member_id, error)
            name = "новый участник"

        await message.answer(GREETING.format(member_id=member_id, name=name))

    # 2) AI-ответы: любой текст (длина >= 1 — чтобы не реагировать на пустые
    #    события-действия вроде выхода из беседы). Хендлер приветствия
    #    зарегистрирован первым, поэтому действий он не задевает.
    @bot.on.message(length=1)
    async def reply_with_ai(message: Message) -> None:
        try:
            answer = await ai.ask(message.peer_id, message.text)
        except AIBillingError as error:
            logger.error("ProxyAPI: нет баланса — {}", error)
            await message.answer(AI_NO_BALANCE)
            return
        except AIError as error:
            logger.error("Ошибка ProxyAPI: {}", error)
            await message.answer(AI_FALLBACK)
            return
        await message.answer(answer)

    # закрываем HTTP-сессию AI-клиента при остановке бота
    bot.on_shutdown.append(ai.close())
    return bot


def main() -> None:
    try:
        settings = load_settings()
    except ConfigError as error:
        logger.error("{}", error)
        raise SystemExit(1) from error

    bot = build_bot(settings)
    logger.info("Бот запускается (LongPoll), модель {}", settings.ai_model)
    bot.run()  # в vkbottle 4.x актуальный запуск longpoll


if __name__ == "__main__":
    main()
