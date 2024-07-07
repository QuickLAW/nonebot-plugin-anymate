from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""

    db_dir: str = "./data/anymate/data.db"
    info_table_name: str = "info_table"
    user_table_name: str = "user_table"

    UTC: str = "Asia/Shanghai"
    _info_table_sql: str = """(
            id integer primary key,
            name text,
            UUID text,
            mateId text
        )"""

    _user_table_sql: str = """(
            id integer primary key,
            user_id text,
            XSRF_TOKEN text,
            anymate_session text,
            remember_key text,
            remember_web text
        )"""

    _plugin_version = "1.4.0"
