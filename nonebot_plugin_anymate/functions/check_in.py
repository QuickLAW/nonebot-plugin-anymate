from ..api_operate import api_check_in, api_get_token_by_remember
from ..config import Config
from ..sql_operate import SQL_Operate
from ..utils.send_msg import send_private_msg

from nonebot import get_plugin_config, on_command, require, get_bot
from nonebot.log import logger
from nonebot.adapters import Event

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

any_config = get_plugin_config(Config)
task_time = any_config.task_time
time_parts = task_time.split(":")
hours, minutes, seconds = map(int, time_parts)
logger.success(f"自动签到时间为: {type(hours)}{hours} {type(minutes)}{minutes} {type(seconds)}{seconds}")

check_in = on_command("any签到", aliases={"any打卡"}, priority=111)
check_in_debug = on_command("any签到debug", aliases={"any打卡debug"}, priority=112)


@check_in.handle()
async def check_in_func_by_hand(event: Event):
    user_id = event.get_user_id()

    cookies = {}

    mateId_list: list = await SQL_Operate.query_data_by_anything(
        any_config.db_dir, any_config.user_table_name, user_id, "mateId", "user_id"
    )
    if not mateId_list:
        await check_in.finish("未找到账号，请先使用/anylogin指令绑定账号")
       
    check_in.send(f"共有{len(mateId_list)}个账户\n{str(mateId_list)}")

    for mateId in mateId_list:
        token_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "XSRF_TOKEN",
            "mateId",
        )
        session_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "anymate_session",
            "mateId",
        )
        remember_key_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "remember_key",
            "mateId",
        )
        remember_web_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "remember_web",
            "mateId",
        )

        cookies["XSRF-TOKEN"] = token_list[0]
        cookies["anymate_session"] = session_list[0]
        cookies[remember_key_list[0]] = remember_web_list[0]

        # 通过remember更新token
        new_cookies = await api_get_token_by_remember(cookies=cookies)

        result, new_cookies = await api_check_in(cookies=new_cookies)

        if result["code"] == 400:
            await check_in.send(f"mateId: {mateId}\n今日已经签到过啦！")

        elif result["code"] != 200:
            await check_in.send(f"mateId: {mateId}\n签到出错！错误信息: {result}")
        else:
            await SQL_Operate.insert_or_update_user_data(
                db_dir=any_config.db_dir,
                table_name=any_config.user_table_name,
                token=new_cookies["XSRF-TOKEN"],
                session=new_cookies["anymate_session"],
                mateId=mateId,
            )
            await check_in.send(f"Anymate\nmateId: {mateId}\n签到完成！")


@scheduler.scheduled_job("cron", hour=hours, minute=minutes, second=seconds, id="101")
@check_in_debug.handle()
async def check_in_func_auto():
    logger.info("开始每日Anymate签到")
    bot = get_bot()
    mateId_list = await SQL_Operate.query_total_column(
        any_config.db_dir, any_config.user_table_name, "mateId"
    )
    if not mateId_list:
        return

    for mateId in mateId_list:
        logger.info(f"正在签到: {mateId}")
        cookies = {}
        token_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "XSRF_TOKEN",
            "mateId",
        )
        session_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "anymate_session",
            "mateId",
        )
        remember_key_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "remember_key",
            "mateId",
        )
        remember_web_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "remember_web",
            "mateId",
        )
        user_id_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir,
            any_config.user_table_name,
            mateId,
            "user_id",
            "mateId",
        )

        cookies["anymate_session"] = session_list[0]
        cookies["XSRF-TOKEN"] = token_list[0]
        cookies[remember_key_list[0]] = remember_web_list[0]

        # 通过remember更新token
        cookies = await api_get_token_by_remember(cookies=cookies)

        result, new_cookies = await api_check_in(cookies=cookies)

        if result["code"] == 400:
            await send_private_msg(
                user_id=user_id_list[0],
                message=f"mateId: {mateId}\n今日已经签到过啦！",
                bot=bot,
            )
            await SQL_Operate.insert_or_update_user_data(
                db_dir=any_config.db_dir,
                table_name=any_config.user_table_name,
                token=cookies["XSRF-TOKEN"],
                session=cookies["anymate_session"],
                mateId=mateId,
            )

        elif result["code"] != 200:
            await send_private_msg(
                user_id=user_id_list[0],
                message=f"mateId: {mateId}\n签到出错！错误信息: {result}",
                bot=bot,
            )
        else:
            await SQL_Operate.insert_or_update_user_data(
                db_dir=any_config.db_dir,
                table_name=any_config.user_table_name,
                token=new_cookies["XSRF-TOKEN"],
                session=new_cookies["anymate_session"],
                mateId=mateId,
            )
            await send_private_msg(
                user_id=user_id_list[0],
                message=f"mateId: {mateId}\nAnymate签到完成！",
                bot=bot,
            )
        logger.success(f"{mateId}签到完成")
    logger.success("Anymate每日签到完成！")
