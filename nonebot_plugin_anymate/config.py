from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    db_dir: str = "./data/anymate/data.db"
    info_table_name: str = "info_table"
    UTC: str = "Asia/Shanghai"
    _info_table_sql: str = '''(
            id integer primary key,
            name text,
            UUID text,
            mateId text
        )'''
    _plugin_version = "1.1.5"