import aiosqlite
import os

from nonebot.log import logger


class SQL_Operate:
    def __init__(self) -> None:
        pass

    async def creat_sql(db_dir: str):
        """
        创建SQLite数据库文件。如果数据库文件所在的文件夹不存在，则创建该文件夹。

        参数:
            db_dir (str): 数据库文件的路径。
        """
        folder_path = os.path.dirname(db_dir)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        async with aiosqlite.connect(db_dir) as db:
            pass
        return

    async def creat_table(db_dir: str, table_name: str, table_sql: str):
        """
        创建数据表。如果数据表不存在，则创建该数据表。

        参数:
            db_dir (str): 数据库文件的路径。
            table_name (str): 数据表的名称。
            table_sql (str): 创建数据表的SQL语句。
        """
        logger.info(f"开始创建表{table_name}")
        async with aiosqlite.connect(db_dir) as db:
            await db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {table_sql}")
            await db.commit()
            logger.success(f"数据表 {table_name} 创建成功")

    async def insert_or_update_data(
        db_dir: str, table_name: str, name: str, UUID: str, mateId: str
    ):
        """
        插入或更新数据。如果UUID已经存在，则更新name和mateId；否则，插入新记录。

        参数:
            db_dir (str): 数据库文件的路径。
            table_name (str): 数据表的名称。
            name (str): 角色名称。
            UUID (str): 角色UUID。
            mateId (str): 角色mateId。
        """
        async with aiosqlite.connect(db_dir) as db:
            # 构造查询和插入/更新语句
            query_sql = f"SELECT id FROM {table_name} WHERE UUID = ?;"
            insert_sql = (
                f"INSERT INTO {table_name} (name, UUID, mateId) VALUES (?, ?, ?);"
            )
            update_sql = f"UPDATE {table_name} SET name = ?, mateId = ? WHERE UUID = ?;"

            # 查询是否已经存在具有相同UUID的记录
            cursor = await db.cursor()
            await cursor.execute(query_sql, (UUID,))
            result = await cursor.fetchone()

            if result:
                # 如果存在，则更新name和mateId
                await db.execute(update_sql, (name, mateId, UUID))
                logger.info(f"UUID数据已存在，{name} 和 {mateId} 已更新")
            else:
                # 如果不存在，则插入新记录
                await db.execute(insert_sql, (name, UUID, mateId))
                logger.info(f"UUID数据{name}: {UUID} 已添加，mateId: {mateId}")

            await db.commit()

    async def query_data_by_anything(
        db_dir: str, table_name: str, input: str, target: str, origin: str
    ) -> list | None:
        """
        通过指定数据搜索数据库数据。

        参数:
            db_dir (str): 数据库文件的路径。
            table_name (str): 数据表的名称。
            input (str): 输入的数据。
            target (str): 查找数据的标签。
            origin (str): 输入数据所在的标签。
        """
        async with aiosqlite.connect(db_dir) as db:
            # 构造查询语句
            query_sql = f"SELECT {target} FROM {table_name} WHERE {origin} LIKE ?;"

            # 执行查询
            cursor = await db.cursor()
            await cursor.execute(query_sql, ("%" + str(input) + "%",))
            result = await cursor.fetchall()

            # 如果没有找到匹配项，返回None
            if not result:
                return None

            # 返回找到的list
            return [row[0] for row in result]

    async def insert_or_update_user_data(
        db_dir: str,
        table_name: str,
        token: str,
        session: str,
        mateId: int,
        UUID: str = None,
        user_id: str = None,
        remember_key: str = None,
        remember_web: str = None,
        switch_mateid: str = None,
    ):
        """
        插入或更新数据。如果ID已经存在，则更新token和session；否则，插入新记录。

        参数:
            db_dir (str): 数据库文件的路径。
            table_name (str): 数据表的名称。
            user_id (str): 用户id。
            token (str): XSRF-TOKEN。
            session (str): anymate_session。
            remember_web (str): 用于长时间未登录时获取token和session。
            switch_mateid (str): 待定（推测用于切换账户下角色）。
        """
        async with aiosqlite.connect(db_dir) as db:
            # 构造查询和插入/更新语句
            query_sql = f"SELECT id FROM {table_name} WHERE mateId = ?;"
            insert_sql = f"INSERT INTO {table_name} (mateId, UUID, user_id, XSRF_TOKEN, anymate_session, remember_key, remember_web) VALUES (?, ?, ?, ?, ?, ?, ?);"
            update_all_sql = f"UPDATE {table_name} SET XSRF_TOKEN = ?, anymate_session = ?, remember_key = ?, remember_web = ? WHERE mateId = ?;"
            update_two_sql = f"UPDATE {table_name} SET XSRF_TOKEN = ?, anymate_session = ? WHERE mateId = ?;"

            # 查询是否已经存在具有相同mateId的记录
            cursor = await db.cursor()
            await cursor.execute(query_sql, (mateId,))
            result = await cursor.fetchone()

            if result:
                if remember_key:
                    # 如果存在，则更新remember_web, anymate_session, XSRF_TOKEN
                    await db.execute(
                        update_all_sql,
                        (token, session, remember_key, remember_web, mateId),
                    )
                    logger.info(
                        f"{UUID}数据已存在，{token} , {session} , {remember_web} 已更新"
                    )
                else:
                    await db.execute(update_two_sql, (token, session, mateId))
                    logger.info(f"{UUID}数据已存在，{token} , {session} 已更新")
            else:
                # 如果不存在，则插入新记录
                await db.execute(
                    insert_sql, (mateId, UUID, user_id, token, session, remember_key, remember_web)
                )
                logger.info(
                    f"{UUID}: {mateId}, 数据{user_id}: {token} 已添加, session: {session}, {remember_key}: {remember_web}"
                )

            await db.commit()


    async def add_column_if_not_exists(db_dir, table_name, new_column, new_type, default_value):
        """
        检查并添加新列到指定的表中，并为已有的数据赋予默认值。

        参数:
            db_dir (str): 数据库文件的路径。
            table_name (str): 数据表的名称。
            new_column (str): 新添加的列名。
            default_value (str): 新列的默认值。
        """
        async with aiosqlite.connect(db_dir) as db:
            # 构造查询语句以获取表的列信息
            check_column_sql = f"PRAGMA table_info({table_name});"

            # 获取表的列信息
            cursor = await db.cursor()
            await cursor.execute(check_column_sql)
            columns = await cursor.fetchall()

            # 提取所有的列名
            column_names = [column[1] for column in columns]

            # 检查新列是否存在
            if new_column not in column_names:
                # 如果列不存在，则构造添加新列的语句
                add_column_sql = f"ALTER TABLE {table_name} ADD COLUMN {new_column} {new_type} DEFAULT '{default_value}';"
                
                # 执行添加新列的操作
                await db.execute(add_column_sql)
                logger.info(f"列{new_column}(类型: {new_type})已添加到{table_name}表中，默认值为{default_value}")

            # 提交更改
            await db.commit()
        
        
    async def query_total_column(
        db_dir: str, table_name: str, target: str
    ) -> list | None:
        """
        查询数据库指定列的所有数据。

        参数:
            db_dir (str): 数据库文件的路径。
            table_name (str): 数据表的名称。
            target (str): 查找数据的标签。
        """
        async with aiosqlite.connect(db_dir) as db:
            # 构造查询语句
            query_sql = f"SELECT {target} FROM {table_name};"

            # 执行查询
            cursor = await db.cursor()
            await cursor.execute(query_sql)
            result = await cursor.fetchall()

            # 如果没有找到匹配项，返回None
            if not result:
                return None

            # 返回找到的list
            return [row[0] for row in result]
