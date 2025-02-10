from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.data.config import BOT_TOKEN

dp = Dispatcher(
        storage = MemoryStorage()
        )

bot = Bot(
    token = BOT_TOKEN,
    default = DefaultBotProperties(parse_mode = ParseMode.HTML)
    )