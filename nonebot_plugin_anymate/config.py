from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""

    db_dir: str = "./data/anymate/data.db"
    info_table_name: str = "info_table"
    user_table_name: str = "user_table"

    UTC: str = "Asia/Shanghai"
    task_time: str = "09:00:00"
    _info_table_sql: str = """(
            id integer primary key,
            name text,
            UUID text,
            mateId integer
        )"""

    _user_table_sql: str = """(
            id integer primary key,
            mateId integer,
            UUID text,
            user_id text,
            XSRF_TOKEN text,
            anymate_session text,
            remember_key text,
            remember_web text
        )"""

    _plugin_version = "1.5.8"
