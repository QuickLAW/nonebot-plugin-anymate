from ..api_operate import api_check_in, api_get_token_by_remember
from ..config import Config
from ..sql_operate import SQL_Operate
from ..utils.send_msg import send_private_msg

from nonebot import get_plugin_config, on_command, require
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11.bot import Bot

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

any_config = get_plugin_config(Config)

check_in = on_command("any签到", aliases={"any打卡"}, priority=111)
check_in_debug = on_command("any签到debug", aliases={"any打卡debug"}, priority=112)


@check_in.handle()
async def check_in_func_by_hand(event: Event):
    user_id = event.get_user_id()

    cookies = {}

    token_list = await SQL_Operate.query_data_by_anything(
        any_config.db_dir, any_config.user_table_name, user_id, "XSRF_TOKEN", "user_id"
    )
    cookies["XSRF-TOKEN"] = token_list[0]
    if not cookies["XSRF-TOKEN"]:
        await check_in.finish("未找到账号，请先使用/anylogin指令绑定账号")
    if len(token_list) > 1:
        await check_in.finish("查找到多个id值！请联系开发者")

    session_list = await SQL_Operate.query_data_by_anything(
        any_config.db_dir,
        any_config.user_table_name,
        user_id,
        "anymate_session",
        "user_id",
    )
    remember_key_list = await SQL_Operate.query_data_by_anything(
        any_config.db_dir,
        any_config.user_table_name,
        user_id,
        "remember_key",
        "user_id",
    )
    remember_web_list = await SQL_Operate.query_data_by_anything(
        any_config.db_dir,
        any_config.user_table_name,
        user_id,
        "remember_web",
        "user_id",
    )

    cookies["anymate_session"] = session_list[0]
    cookies[remember_key_list[0]] = remember_web_list[0]

    # 通过remember更新token
    new_cookies = await api_get_token_by_remember(cookies=cookies)

    result, new_cookies = await api_check_in(cookies=new_cookies)

    if result["code"] == 400:
        await check_in.finish("今日已经签到过啦！")

    if result["code"] != 200:
        await check_in.finish(f"签到出错！错误信息: {result}")
    else:
        await SQL_Operate.insert_or_update_user_data(
            any_config.db_dir,
            any_config.user_table_name,
            user_id,
            new_cookies["XSRF-TOKEN"],
            new_cookies["anymate_session"],
        )
        await check_in.finish(f"Anymate签到完成！")


@scheduler.scheduled_job(
    "cron", hour=8, minute=0, second=0, id="101", kwargs={"bot": Bot}
)
@check_in_debug.handle()
async def check_in_func_auto(bot: Bot):
    user_id_list = await SQL_Operate.query_total_column(
        any_config.db_dir, any_config.user_table_name, "user_id"
    )
    if not user_id_list:
        return

    for user_id in user_id_list:
        cookies = {}
        token_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            user_id,
            "XSRF_TOKEN",
            "user_id",
        )
        session_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            user_id,
            "anymate_session",
            "user_id",
        )
        remember_key_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            user_id,
            "remember_key",
            "user_id",
        )
        remember_web_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            user_id,
            "remember_web",
            "user_id",
        )

        cookies["anymate_session"] = session_list[0]
        cookies["XSRF-TOKEN"] = token_list[0]
        cookies[remember_key_list[0]] = remember_web_list[0]

        # 通过remember更新token
        cookies = await api_get_token_by_remember(cookies=cookies)

        result, new_cookies = await api_check_in(cookies=cookies)

        if result["code"] == 400:
            await send_private_msg(
                user_id=user_id, message="今日已经签到过啦！", bot=bot
            )
            await SQL_Operate.insert_or_update_user_data(
                any_config.db_dir,
                any_config.user_table_name,
                user_id,
                cookies["XSRF-TOKEN"],
                cookies["anymate_session"],
            )

        elif result["code"] != 200:
            await send_private_msg(
                user_id=user_id, message=f"签到出错！错误信息: {result}", bot=bot
            )
        else:
            await SQL_Operate.insert_or_update_user_data(
                any_config.db_dir,
                any_config.user_table_name,
                user_id,
                new_cookies["XSRF-TOKEN"],
                new_cookies["anymate_session"],
            )
            await send_private_msg(
                user_id=user_id, message=f"Anymate签到完成！", bot=bot
            )
