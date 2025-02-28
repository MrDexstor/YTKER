import asyncio
import json
import logging
import sys

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcore.settings")
django.setup()

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from ai.ai import ai_request
from ai.task import taskCreate, getUserTask
from config import BOT_TOKEN

# Bot token can be obtained via https://t.me/BotFather
TOKEN = BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Добро пожаловать в систему У.Т.К.Э.Р.")
    await message.answer(f"Что вы хотите сделать?")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        msg = ai_request(message.text)
        ai_answer = json.loads(msg)

        type = ai_answer['type']

        if type == 'request':
            await message.answer(ai_answer['user_message'])
        elif type == 'task':
            await taskCreate(message.chat.id, ai_answer)
            await message.answer(ai_answer['user_message'])
        elif type == 'task_search':
            await message.answer(ai_answer['user_message'])
            task_airq = ai_request(message.text, await getUserTask(message.chat.id))
            await message.answer(task_airq)

    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Пожалуйста, уточните ваш запрос.")
        await message.answer(f"Что вы хотите сделать?")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())