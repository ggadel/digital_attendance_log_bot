from sqlalchemy import insert, update, select, delete

from src.database.database import async_engine
from src.models.models import metadata_obj, journal, users, permission_codes
from sqlalchemy.orm import aliased

import datetime




class DataBase:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.create_all)


    @staticmethod
    async def add_user(user_tg_id, username, registered_at):
        async with async_engine.connect() as conn:
            stmt = insert(users).values(
                [
                    {'user_tg_id': user_tg_id, "username": username, "registered_at": registered_at},
                ]
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def update_username(user_tg_id: int, new_username: str):
        async with async_engine.connect() as conn:
            stmt = (
                update(users)
                .values(username=new_username)
                .filter_by(id=user_tg_id)
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def get_user(user_tg_id: int):
        async with async_engine.connect() as conn:
            query = select(users).where(users.c.user_tg_id == user_tg_id)
            result = await conn.execute(query)
            user = result.fetchall()
            for data in user:
                if user_tg_id == data[1]:
                    return data
            return "User not found"



    @staticmethod
    async def check_user(user_tg_id: int, current_username: str):
        async with async_engine.connect() as conn:
            query = select(users).where(users.c.user_tg_id == user_tg_id)
            result = await conn.execute(query)
            user = result.fetchall()
            if len(user) > 0:
                for data in user:
                    if data[2] == current_username:
                        return True
                return False
            else:
                return "User not found"


    @staticmethod
    async def check_ban_user(user_tg_id):
        async with async_engine.connect() as conn:
            query = select(users).where(users.c.user_tg_id == user_tg_id)
            result = await conn.execute(query)
            users_list = result.fetchall()
            for user in users_list:
                if user[3] == True:
                    return True
            return False


    @staticmethod
    async def ban_user(user_tg_id: int):
        async with async_engine.connect() as conn:
            stmt = (
                update(users)
                .values(banned=True)
                .filter_by(user_tg_id=user_tg_id)
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def unban_user(user_tg_id: int):
        async with async_engine.connect() as conn:
            stmt = (
                update(users)
                .values(banned=False)
                .filter_by(user_tg_id=user_tg_id)
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def give_mark_permission(user_tg_id, permission_code_id):
        async with async_engine.connect() as conn:
            stmt = (
                update(users)
                .values(mark_permission=True)
                .values(permission_code_id=permission_code_id)
                .filter_by(user_tg_id=user_tg_id)
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def remove_mark_permission(user_tg_id):
        async with async_engine.connect() as conn:
            stmt = (
                update(users)
                .values(mark_permission=False)
                .filter_by(user_tg_id=user_tg_id)
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def check_mark_permission(user_tg_id):
        async with async_engine.connect() as conn:
            query = select(users).where(users.c.user_tg_id == user_tg_id)
            result = await conn.execute(query)
            users_list = result.fetchall()
            for user in users_list:
                if user[4] == True:
                    return True
            return False


    
    
    @staticmethod
    async def send_form(final_data):
        async with async_engine.connect() as conn:
            stmt = insert(journal).values(
                [
                    final_data,
                ]
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def check_form_completion(date, class_name):
        async with async_engine.connect() as conn:
            query = select(journal).where(journal.c.date == date)
            result = await conn.execute(query)
            rows = result.fetchall()
            for row in rows:
                if row[1] == class_name:
                    return True
            return False
        
    @staticmethod
    async def get_absent(date):
        async with async_engine.connect() as conn:
            j = aliased(journal)
            u = aliased(users)
            subq = (
                select(
                    j,
                    u,
                )
                # .select_from(r)
                .join(j, j.c.sender_tg_id == u.c.user_tg_id).subquery("helper1")
            )
            cte = (
                select(
                    subq.c.id,
                    subq.c.class_name,
                    subq.c.amount_of_students,
                    subq.c.amount_of_absent,
                    subq.c.list_of_absent,
                    subq.c.sender_tg_id,
                    subq.c.username,
                    subq.c.date,
                    subq.c.time,
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .where(cte.c.date == date)
            )

            res = await conn.execute(query)
            result = res.all()
            return result


    @staticmethod
    async def remove_entry(id):
        async with async_engine.connect() as conn:
            stmt = (
                delete(journal)
                .filter_by(id=id)
            )
            await conn.execute(stmt)
            await conn.commit()




    @staticmethod
    async def add_code(permission_code, name, creater_tg_id, created_at):
        async with async_engine.connect() as conn:
            stmt = insert(permission_codes).values(
                [
                    {"permission_code": permission_code, "name": name, "creater_tg_id": creater_tg_id, "created_at": created_at},
                ]
            )
            await conn.execute(stmt)
            await conn.commit()


    @staticmethod
    async def check_permission_code(permission_code):
        async with async_engine.connect() as conn:
            query = select(permission_codes).where(permission_codes.c.permission_code == permission_code)
            result = await conn.execute(query)
            code = result.fetchone()
            print(code)
            if code != None:
                return code
            else:
                return False


    @staticmethod
    async def get_codes():
        async with async_engine.connect() as conn:
            query = select(permission_codes)
            result = await conn.execute(query)
            codes = result.fetchall()
            return codes


    @staticmethod
    async def remove_code(id):
        async with async_engine.connect() as conn:
            stmt = (
                delete(permission_codes)
                .filter_by(id=id)
            )
            await conn.execute(stmt)
            await conn.commit()