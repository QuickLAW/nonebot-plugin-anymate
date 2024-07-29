from ..api_operate import api_upvote, api_get_token_by_remember, api_get_explore_post
from ..config import Config
from ..sql_operate import SQL_Operate
from ..utils.send_msg import send_private_msg
from ..utils.simple_func import generate_unique_random_numbers

from nonebot import get_plugin_config, on_command, require, get_bot
from nonebot.log import logger
from nonebot.adapters import Event

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

any_config = get_plugin_config(Config)
task_time = any_config.task_time
time_parts = task_time.split(":")
hours, minutes, seconds = map(int, time_parts)

upvote = on_command("any点赞", aliases={"点赞"}, priority=113)
upvote_debug = on_command("any点赞debug", aliases={"点赞debug"}, priority=114)


@upvote.handle()
async def upvote_func_by_hand(event: Event):
    user_id = event.get_user_id()

    cookies = {}

    mateId_list = await SQL_Operate.query_data_by_anything(
        any_config.db_dir,
        any_config.user_table_name,
        user_id,
        "mateId",
        "user_id",
    )

    if not mateId_list:
        await upvote.finish("未找到账号，请先使用/anylogin指令绑定账号")
        
    upvote.send(f"共有{len(mateId_list)}个账户\n{str(mateId_list)}")
    # 获取replyId、UUID
    explore_posts = await api_get_explore_post(5)
    
    replyId_list = []
    last_explore_post_list = explore_posts["page"]["data"]
    for last_explore_post in last_explore_post_list:
        replyId_list.append(last_explore_post["reply"]["id"])

    number_list = generate_unique_random_numbers(5, 19)

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
        UUID_list: str = await SQL_Operate.query_data_by_anything(
            any_config.db_dir, any_config.user_table_name, mateId, "UUID", "mateId"
        )
        
        cookies["XSRF-TOKEN"] = token_list[0]
        cookies["anymate_session"] = session_list[0]
        cookies[remember_key_list[0]] = remember_web_list[0]
        
        for i in range(len(number_list)):

            # 通过remember更新token
            cookies = await api_get_token_by_remember(cookies=cookies)

            # 点赞
            result, new_cookies = await api_upvote(
                emojiId=number_list[i],
                replyId=replyId_list[i],
                UUID=UUID_list[0],
                cookies=cookies,
            )

            if result["code"] != 200:
                await upvote.send(f"点赞出错！错误信息: {result}")
            else:
                await SQL_Operate.insert_or_update_user_data(
                    db_dir=any_config.db_dir,
                    table_name=any_config.user_table_name,
                    token=new_cookies["XSRF-TOKEN"],
                    session=new_cookies["anymate_session"],
                    mateId=mateId,
                )
                await upvote.send(
                    f"{i + 1}/5\n手动点赞成功\n表情ID: {number_list[i]}\nmateId: {mateId}"
                )


@scheduler.scheduled_job("cron", hour=hours, minute=minutes, second=seconds, id="102")
@upvote_debug.handle()
async def upvote_func_auto():
    logger.info("开始每日Anymate点赞")
    mateId_list = await SQL_Operate.query_total_column(
        any_config.db_dir, any_config.user_table_name, "mateId"
    )
    if not mateId_list:
        return

    for mateId in mateId_list:
        logger.info(f"正在点赞: {mateId}")
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
        user_id = user_id_list[0]

        cookies["anymate_session"] = session_list[0]
        cookies["XSRF-TOKEN"] = token_list[0]
        cookies[remember_key_list[0]] = remember_web_list[0]

        # 通过remember更新token
        cookies = await api_get_token_by_remember(cookies=cookies)

        # 获取replyId、UUID
        explore_posts = await api_get_explore_post()
        replyId_list = []
        last_explore_post_list = explore_posts["page"]["data"]
        for last_explore_post in last_explore_post_list:
            replyId_list.append(last_explore_post["reply"]["id"])
        UUID: str = await SQL_Operate.query_data_by_anything(
            any_config.db_dir, any_config.user_table_name, mateId, "UUID", "mateId"
        )
        UUID = UUID[0]

        number_list = generate_unique_random_numbers(5, 20)
        for i in range(5):
            result, new_cookies = await api_upvote(
                emojiId=number_list[i], replyId=replyId_list[i], UUID=UUID, cookies=cookies
            )

            if result["code"] != 200:
                await send_private_msg(
                    user_id=user_id,
                    message=f"{i + 1}/5\n点赞出错！错误信息: {result}",
                    bot=get_bot(),
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
                    user_id=user_id,
                    message=f"{i + 1}/5\n点赞成功\n表情ID: {number_list[i]}\nmateId: {mateId}",
                    bot=get_bot(),
                )
        logger.success(f"Anymate点赞完成：{mateId}")
    logger.success("Anymate每日点赞完成！")
