import asyncio

from .functions.functions import *
from .tools import Tools
from .config import Config
from .sql_operate import SQL_Operate
from .functions.login import *
from .functions.check_in import *

from nonebot.plugin import PluginMetadata, get_plugin_config

__plugin_meta__ = PluginMetadata(
    name="AnyMate小助手",
    description="实现对anymate网站的简单帮助",
    usage="使用 /any帮助 来查看指令",
    config=Config,
    supported_adapters=["~onebot.v11"],
    type="application",
    homepage="https://github.com/QuickLAW/nonebot-plugin-anymate",
)

any_config = get_plugin_config(Config)

async def init():
    # 创建数据库和UUID表
    await SQL_Operate.creat_sql(any_config.db_dir)
    # 创建角色信息表
    await SQL_Operate.creat_table(
        any_config.db_dir, any_config.info_table_name, any_config._info_table_sql
    )
    # 创建账户信息表
    await SQL_Operate.creat_table(
        any_config.db_dir, any_config.user_table_name, any_config._user_table_sql
    )


asyncio.run(init())
