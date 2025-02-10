import asyncio
import logging
import os
import pathlib
import datetime
import json

from src.data.config import PATH_TO_LOGS, PATH_TO_LIST_OF_CLASSES

from src.handlers.users.start import router_start
from src.handlers.users.mark_absent import router_mark_absent
from src.handlers.users.support import router_support
from src.handlers.users.help import router_help
from src.handlers.users.unmarked_classes import router_unmarked_classes

from src.handlers.admins.ban import router_ban
from src.handlers.admins.get_absent import router_get_absent
from src.handlers.admins.get_user import router_get_user
from src.handlers.admins.remove_entry import router_remove_entry
from src.handlers.admins.unban import router_unban
from src.handlers.admins.add_class import router_add_class
from src.handlers.admins.remove_class import router_remove_class
from src.handlers.admins.list_of_classes import router_list_of_classes
from src.handlers.admins.admin_help import router_admin_help
from src.handlers.admins.create_code import router_create_code
from src.handlers.admins.get_codes import router_get_codes
from src.handlers.admins.remove_code import router_remove_code
from src.handlers.admins.give_permission import router_get_permission
from src.handlers.admins.remove_permission import router_remove_permission
from src.handlers.admins.admin_panel import router_admin_panel

from src.middlewares.ignore_banned_users import IgonareBannedUsersMiddleware
from src.middlewares.ignore_not_admin import IgnoreNotAdminMiddleware

from src.database.queries import DataBase

from loader import bot, dp




async def main():
    path_to_logs = pathlib.Path(PATH_TO_LOGS)
    if path_to_logs.exists() == False:
        os.mkdir(PATH_TO_LOGS)
    
    path_to_list_of_classes = pathlib.Path(PATH_TO_LIST_OF_CLASSES)
    if path_to_list_of_classes.exists() == False:
        with open(PATH_TO_LIST_OF_CLASSES, "w") as f:
            lst = ["example_class"]
            json.dump((lst), f)

    log_time = datetime.datetime.now().strftime("%d-%m-%Y %H.%M.%S")

    logging.basicConfig(level = logging.INFO, handlers = (logging.FileHandler(f"{PATH_TO_LOGS}/{log_time}.log"), logging.StreamHandler()), format = "%(asctime)s %(levelname)s: %(message)s")


    await DataBase.create_tables()


    dp.update.middleware(IgonareBannedUsersMiddleware())
    router_add_class.message.middleware(IgnoreNotAdminMiddleware())
    router_ban.message.middleware(IgnoreNotAdminMiddleware())
    router_get_absent.message.middleware(IgnoreNotAdminMiddleware())
    router_get_user.message.middleware(IgnoreNotAdminMiddleware())
    router_list_of_classes.message.middleware(IgnoreNotAdminMiddleware())
    router_remove_class.message.middleware(IgnoreNotAdminMiddleware())
    router_remove_entry.message.middleware(IgnoreNotAdminMiddleware())
    router_unban.message.middleware(IgnoreNotAdminMiddleware())
    router_admin_help.message.middleware(IgnoreNotAdminMiddleware())
    router_create_code.message.middleware(IgnoreNotAdminMiddleware())
    router_get_codes.message.middleware(IgnoreNotAdminMiddleware())
    router_remove_code.message.middleware(IgnoreNotAdminMiddleware())
    router_get_permission.message.middleware(IgnoreNotAdminMiddleware())
    router_remove_permission.message.middleware(IgnoreNotAdminMiddleware())
    router_admin_panel.message.middleware(IgnoreNotAdminMiddleware())

    
    dp.include_routers(router_start, router_mark_absent, router_support, router_ban, router_unban, router_get_absent, router_get_user, router_remove_entry, router_add_class, router_remove_class, router_list_of_classes, router_admin_help, router_create_code, router_get_codes, router_remove_code, router_get_permission, router_remove_permission, router_admin_panel, router_unmarked_classes, router_help)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())