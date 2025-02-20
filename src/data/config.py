import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_DB_NAME = os.getenv("PG_DB_NAME")

PG_LINK = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{PG_DB_NAME}"

ADMINS = os.getenv('ADMINS').split(",")

PATH_TO_LOGS = "bot_logs"
PATH_TO_LIST_OF_CLASSES = "src/data/list_of_classes.txt"

MARK_ABSENT_CMD_DELAY = 0 #in seconds


DEVLOPER_USER_NAME = "ggadel"