from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database.queries import DataBase


class IgonareBannedUsersMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data["event_from_user"]
        if await DataBase.check_ban_user(user_tg_id=user.id) == True:
            return
        return await handler(event, data)