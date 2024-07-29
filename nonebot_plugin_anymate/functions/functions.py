from ..api_operate import (
    api_get_info_func,
    api_get_last_post,
    api_search_func,
    api_get_explore_post,
)
from ..config import Config
from ..sql_operate import SQL_Operate
from ..tools import Tools

from datetime import datetime, timezone
import pytz

from nonebot.params import CommandArg
from nonebot.plugin import on_command, get_plugin_config
from nonebot.exception import ActionFailed
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.message import MessageSegment

login_dict = {}

any_config = get_plugin_config(Config)

get_info = on_command("角色信息", aliases={"信息"}, priority=108)
get_last_post = on_command("最新动态", aliases={"动态"}, priority=107)
search = on_command("角色搜索", aliases={"搜索"}, priority=109)
add_char = on_command("添加角色", aliases={"添加UUID", "添加角色UUID"}, priority=105)
remind_update = on_command("催更", priority=110)
get_explore = on_command("发现", aliases={"首页动态", "首页"}, priority=101)
any_help = on_command("anyhelp", aliases={"any帮助", "any"}, priority=100)


@get_info.handle()
async def get_info_func(args: Message = CommandArg()):
    uuid = await SQL_Operate.query_data_by_anything(
        any_config.db_dir, any_config.info_table_name, str(args), "UUID", "name"
    )
    if not uuid:
        await get_info.finish(f"{args}目前为机器人未记录的角色")
    if len(uuid) > 1:
        name_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir, any_config.info_table_name, str(args), "name", "name"
        )
        message = MessageSegment.text("查找到多个结果\n")
        for i in name_list:
            message += MessageSegment.text(i + "\n")
        message += MessageSegment.text("请重新输入")
        await get_info.finish(message)

    info = {
        "角色名": None,
        "账号ID": None,
        "角色ID": None,
        "年龄": None,
        "个人简介": None,
        "mediaUrl": None,
    }
    info_result = await api_get_info_func(uuid[0])
    info["角色名"] = info_result["item"]["name"]
    info["账号ID"] = info_result["item"]["userId"]
    info["角色ID"] = info_result["item"]["id"]
    info["年龄"] = info_result["item"]["age"]
    info["个人简介"] = info_result["item"]["bio"]
    info["mediaUrl"] = info_result["item"]["mediaUrl"]

    try:
        message = MessageSegment.text(
            f"""角色名：{info['角色名']}\nmateID：{info["角色ID"]}\n年龄：{info["年龄"]}\n个人简介：{info["个人简介"]}\n"""
        )
        message += MessageSegment.image(info["mediaUrl"])

        await get_info.finish(message)
    except ActionFailed:
        message = MessageSegment.text(
            f"""角色名：{info['角色名']}\nmateID：{info["角色ID"]}\n年龄：{info["年龄"]}\n个人简介：{info["个人简介"]}\n"""
        )
        message += MessageSegment.text(info["mediaUrl"])

        await get_info.finish(message)


@get_last_post.handle()
async def get_last_post_func(args: Message = CommandArg()):
    args_list = []
    if not str(args):
        await search.finish("请至少包含角色名")
    if str(args):
        args_list = str(args).split()
        try:
            perPage = int(args_list[1])
        except IndexError:
            perPage = 5
        except ValueError:
            await get_last_post.finish("输入需要为数字")
    if perPage > 20:
        await get_last_post.send("超出最大数量限制！！")
        perPage = 5

    mateId = await SQL_Operate.query_data_by_anything(
        any_config.db_dir, any_config.info_table_name, args_list[0], "mateId", "name"
    )
    if not mateId:
        await get_last_post.finish(f"{args}目前为机器人未记录的角色")
    if len(mateId) > 1:
        name_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir, any_config.info_table_name, args_list[0], "name", "name"
        )
        message = MessageSegment.text("查找到多个角色\n")
        for i in name_list:
            message += MessageSegment.text(i + "\n")
        message += MessageSegment.text("请重新输入")
        await get_last_post.finish(message)

    post_content = await api_get_last_post(mateId, perPage)

    data = post_content["page"]["data"]
    info = {"dtCreate": [], "mediazz": [], "text": []}
    for i in data:
        info["mediazz"].append(i["mediazz"])
        info["text"].append(i["text"])

        dtCreate: str = i["dtCreate"]
        formatted_time = Tools.time_to_format(dtCreate, any_config.UTC)
        info["dtCreate"].append(formatted_time)

    perPage = min(perPage, len(data))

    for i in range(perPage):
        try:
            message = MessageSegment.text(f"动态 [{i+1}/{perPage}]：\n")
            mediazz = info["mediazz"][i]
            text = info["text"][i]
            dtCreate = f"更新时间：\n{info['dtCreate'][i]}" + "\n"
            message += MessageSegment.text(dtCreate)
            message += MessageSegment.text(text)
            for j in mediazz:
                message += MessageSegment.image(j["url"])
            await get_last_post.send(message)
        except ActionFailed:
            message = MessageSegment.text(f"动态 [{i+1}/{perPage}]：\n")
            mediazz = info["mediazz"][i]
            text = info["text"][i]
            dtCreate = f"更新时间：\n{info['dtCreate'][i]}" + "\n"
            message += MessageSegment.text(dtCreate)
            message += MessageSegment.text(text)
            for j in mediazz:
                message += MessageSegment.text(j["url"] + "\n")
            await get_last_post.send(message)

    if not data:
        await get_last_post.finish(args_list[0] + "还没有发过动态哦~")


@search.handle()
async def get_search_content_func(args: Message = CommandArg()):
    args_list = []
    if not str(args):
        await search.finish("请至少包含角色名")
    else:
        args_list = str(args).split()
        try:
            perPage = int(args_list[1])
        except IndexError:
            perPage = 5
        except ValueError:
            await search.finish("输入需要为数字")
    if perPage > 20:
        await search.send("超出最大数量限制！！")
        perPage = 5
    search_result = await api_search_func(args_list[0], perPage)

    info = {"name": [], "mateId": [], "uuid": [], "bio": [], "type": [], "mediaUrl": []}
    total = search_result["page"]["total"]

    for i in search_result["page"]["data"]:
        info["name"].append(i["name"])
        info["mateId"].append(i["id"])
        info["uuid"].append(i["uuid"])
        info["bio"].append(i["bio"])
        info["type"].append(i["type"])
        info["mediaUrl"].append(i["mediaUrl"])

    perPage = min(total, perPage)

    for i in range(perPage):
        try:
            message = MessageSegment.text(f"{args_list[0]} 搜索结果{i+1}/{perPage}：\n")
            name = info["name"][i] + "\n"
            mateId = f"mateId: {info['mateId'][i]}" + "\n"
            uuid = f"UUID: {info['uuid'][i]}" + "\n"
            char_type = f"角色类型: {info['type'][i]}" + "\n"
            mediaUrl = info["mediaUrl"][i]
            bio = f"简介：{info['bio'][i]}"
            message += MessageSegment.text(name)
            message += MessageSegment.text(mateId)
            message += MessageSegment.text(uuid)
            message += MessageSegment.text(char_type)
            message += MessageSegment.image(mediaUrl)
            message += MessageSegment.text(bio)
            await search.send(message)
        except ActionFailed:
            message = MessageSegment.text(f"{args_list[0]} 搜索结果{i+1}/{perPage}：\n")
            name = info["name"][i] + "\n"
            mateId = f"mateId: {info['mateId'][i]}" + "\n"
            uuid = f"UUID: {info['uuid'][i]}" + "\n"
            char_type = f"角色类型: {info['type'][i]}" + "\n"
            mediaUrl = info["mediaUrl"][i]
            bio = f"简介：{info['bio'][i]}"
            message += MessageSegment.text(name)
            message += MessageSegment.text(mateId)
            message += MessageSegment.text(uuid)
            message += MessageSegment.text(char_type)
            message += MessageSegment.text(mediaUrl + "\n")
            message += MessageSegment.text(bio)
            await search.send(message)


@add_char.handle()
async def add_char_by_UUID_func(args: Message = CommandArg()):
    UUID = str(args)
    if not UUID:
        await add_char.finish("需要包含UUID！")

    info_result = await api_get_info_func(UUID)
    name = info_result["item"]["name"]
    mateId = info_result["item"]["id"]

    await SQL_Operate.insert_or_update_data(
        any_config.db_dir, any_config.info_table_name, name, UUID, mateId
    )
    await add_char.finish(f"{name} 已添加")


@remind_update.handle()
async def remind_update_func(args: Message = CommandArg()):
    name = str(args)
    mateId = await SQL_Operate.query_data_by_anything(
        any_config.db_dir, any_config.info_table_name, name, "mateId", "name"
    )
    if not mateId:
        await remind_update.finish(f"{args}目前为机器人未记录的角色")
    if len(mateId) > 1:
        name_list = await SQL_Operate.query_data_by_anything(
            any_config.db_dir, any_config.info_table_name, name, "name", "name"
        )
        message = MessageSegment.text("查找到多个结果\n")
        for i in name_list:
            message += MessageSegment.text(i + "\n")
        message += MessageSegment.text("请重新输入")
        await remind_update.finish(message)

    post_content = await api_get_last_post(mateId)
    dtCreate: str = post_content["page"]["data"][0]["dtCreate"]

    timezone_str = any_config.UTC
    timezone = pytz.timezone(timezone_str)

    time = datetime.fromisoformat(dtCreate.replace("Z", "+00:00")).replace(
        tzinfo=pytz.utc
    )
    time = time.astimezone(timezone)
    formatted_time = Tools.time_to_format(dtCreate, any_config.UTC)
    current_time = datetime.now(timezone)
    time_difference = current_time - time

    # 将时间差转换为秒
    seconds_difference = int(time_difference.total_seconds())
    seconds = int(seconds_difference % 60)

    # 将时间差转换为分钟和小时
    minutes_difference = int(seconds_difference // 60)
    minutes = int(minutes_difference % 60)
    hours_difference = int(minutes_difference // 60)
    hours = int(hours_difference % 24)
    days_difference = int(hours_difference // 24)
    days = ""

    name = await SQL_Operate.query_data_by_anything(
        any_config.db_dir, any_config.info_table_name, name, "name", "name"
    )
    message = MessageSegment.text(name[0] + "\n")
    message += MessageSegment.text("最新更新时间为：" + formatted_time + "\n")
    if days_difference != 0:
        days = str(days_difference) + "天"
    result = (
        "已经"
        + days
        + str(hours)
        + "小时"
        + str(minutes)
        + "分钟"
        + str(seconds)
        + "秒"
        + "没更新啦！！！"
    )
    message += MessageSegment.text(result)

    await remind_update.finish(message)


@get_explore.handle()
async def get_explore_func(args: Message = CommandArg()):
    args_list = []
    if not str(args):
        perPage = 5
    else:
        args_list = str(args).split()
        try:
            perPage = int(args_list[0])
        except:
            await get_explore.finish("输入需要为数字")
    if int(perPage) > 20:
        await get_explore.send("超出最大数量限制！！")
        perPage = 5

    perPage = int(perPage)

    post_content = await api_get_explore_post(perPage)
    data = post_content["page"]["data"]

    info = {
        "name": [],
        "mateId": [],
        "uuid": [],
        "type": [],
        "mediaUrl": [],
        "text": [],
        "dtCreate": [],
    }
    for i in data:
        info["name"].append(i["mate"]["name"])
        info["mateId"].append(i["mate"]["id"])
        info["uuid"].append(i["mate"]["uuid"])
        info["type"].append(i["mate"]["type"])
        info["mediaUrl"].append(i["mate"]["mediaUrl"])
        info["text"].append(i["text"])

        dtCreate: str = i["dtCreate"]
        time = datetime.fromisoformat(dtCreate.replace("Z", "-08:00"))
        time = time.astimezone(timezone.utc)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
        info["dtCreate"].append(formatted_time)

    perPage = min(perPage, len(data))

    for i in range(perPage):
        try:
            message = MessageSegment.text(f"动态 [{i+1}/{perPage}]：\n")
            name = info["name"][i] + "\n"
            mateId = f"mateId: {info['mateId'][i]}" + "\n"
            uuid = f"UUID: {info['uuid'][i]}" + "\n"
            char_type = f"角色类型: {info['type'][i]}" + "\n"
            mediaUrl = info["mediaUrl"][i]
            text = info["text"][i]
            dtCreate = f"更新时间：\n{info['dtCreate'][i]}" + "\n"
            message += MessageSegment.text(name)
            message += MessageSegment.text(mateId)
            message += MessageSegment.text(uuid)
            message += MessageSegment.text(char_type)
            message += MessageSegment.text(dtCreate)
            message += MessageSegment.image(mediaUrl)
            message += MessageSegment.text(text)
            await get_explore.send(message)
        except ActionFailed:
            message = MessageSegment.text(f"动态 [{i+1}/{perPage}]：\n")
            name = info["name"][i] + "\n"
            mateId = f"mateId: {info['mateId'][i]}" + "\n"
            uuid = f"UUID: {info['uuid'][i]}" + "\n"
            char_type = f"角色类型: {info['type'][i]}" + "\n"
            mediaUrl = info["mediaUrl"][i]
            text = info["text"][i]
            dtCreate = f"更新时间：\n{info['dtCreate'][i]}" + "\n"
            message += MessageSegment.text(name)
            message += MessageSegment.text(mateId)
            message += MessageSegment.text(uuid)
            message += MessageSegment.text(char_type)
            message += MessageSegment.text(mediaUrl + "\n")
            message += MessageSegment.text(text)
            message += MessageSegment.text(dtCreate)
            await get_explore.send(message)


@any_help.handle()
async def get_help_func(args: Message = CommandArg()):
    message = MessageSegment.text(
        "🌟AnyMate小助手 " + "v" + any_config._plugin_version + "\n\n"
    )
    message += MessageSegment.text("🔹/anyhelp 展示此帮助\n")
    message += MessageSegment.text("🔸/信息 <角色名> 展示指定角色相关信息\n")
    message += MessageSegment.text(
        "🔹/动态 <角色名> [数量] 展示指定角色指定数量的最新动态\n"
    )
    message += MessageSegment.text(
        "🔸/搜索 <角色名> [数量] 搜索角色并展示指定数量的结果\n"
    )
    message += MessageSegment.text("🔹/添加角色 <UUID> 将指定角色添加入小助手数据库\n")
    message += MessageSegment.text("🔸/催更 <角色名> 催更啦！\n")
    message += MessageSegment.text("🔹/发现 [数量] 展示指定数量的发现页帖子\n")
    message += MessageSegment.text("🔸/any登录 进入登录流程\n")
    message += MessageSegment.text("🔹/any签到 登录后可以进行手动签到\n")
    message += MessageSegment.text("🔸/any签到 登录后可以进行手动每日点赞\n")
    message += MessageSegment.text("欢迎使用插件哟~可以多多支持")
    await any_help.finish(message)
