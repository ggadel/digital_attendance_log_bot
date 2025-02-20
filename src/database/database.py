from sqlalchemy.ext.asyncio import create_async_engine

from src.data.config import PG_LINK




async_engine = create_async_engine(
    url=PG_LINK,
    connect_args={"server_settings": {"client_encoding": "utf8"}},
)