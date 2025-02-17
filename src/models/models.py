from sqlalchemy import Table, Column, BigInteger, Integer, String, Boolean, Date, DateTime, MetaData



metadata_obj = MetaData()


users = Table(
    "users",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("user_tg_id", BigInteger, nullable=False),
    Column("username", String, nullable=False),
    Column("banned", Boolean, default=False, nullable=False),
    Column("mark_permission", Boolean, default=False, nullable=False),
    Column("register_date", DateTime, nullable=False), 
)


journal = Table(
    "journal",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("class_name", String, nullable=False),
    Column("amount_of_students", Integer, nullable=False),
    Column("amount_of_absent", Integer, nullable=False),
    Column("list_of_absent", String, nullable=False),
    Column("date", Date, nullable=False),
    Column("sender_tg_id", BigInteger, nullable=False)
)


permission_codes = Table(
    "permission_codes",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("permission_code", String, nullable=False),
    Column("name", String, nullable=True),
    Column("creater_tg_id", BigInteger, nullable=False),
    Column("created_at", DateTime, nullable=False),
)