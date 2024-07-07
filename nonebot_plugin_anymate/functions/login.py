from ..api_operate import api_get_login_token, api_login, api_post_code
from ..tools import Tools
from ..config import Config
from ..sql_operate import SQL_Operate

from nonebot import get_plugin_config, on_command
from nonebot.params import ArgStr
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11.message import MessageSegment


login_dict = {}

any_config = get_plugin_config(Config)

log_in = on_command("any登录", aliases={"anylogin"}, priority=110)


@log_in.handle()
async def any_login_func(event: Event):
    user_id = event.get_user_id()
    login_dict[user_id] = {}
    await log_in.send("请输入邮箱, 输入‘退出’结束登录流程: ")


@log_in.got("email")
async def get_email(event: Event, email: str = ArgStr()):
    user_id = event.get_user_id()
    if email == "退出":
        await log_in.finish("已退出")

    if not Tools.is_valid_email(email):
        await log_in.reject("邮箱非法，请检查邮箱输入是否正确！\n请重新输入：")

    cookie_dict = await api_get_login_token()
    login_dict[user_id]["email"] = email
    login_dict[user_id]["cookies"] = cookie_dict

    result, cookie_dict = await api_login(email=email, cookies=cookie_dict)
    if result["code"] == 200:
        await log_in.send("请输入验证码")
        login_dict[user_id]["cookies"] = cookie_dict
    else:
        await log_in.finish(result)


@log_in.got("code")
async def get_code(event: Event, code: str = ArgStr()):
    user_id = event.get_user_id()
    if code == "退出":
        await log_in.finish("已退出")

    email = login_dict[user_id]["email"]
    cookies_dict = login_dict[user_id]["cookies"]
    result, cookies_dict = await api_post_code(
        email=email, code=code, cookies=cookies_dict
    )

    info = {}
    info["username"] = result["item"]["name"]
    info["email"] = result["item"]["email"]
    info["id"] = result["item"]["id"]
    info["paypel"] = result["item"]["paypal"]
    info["coinAmount"] = result["item"]["coinAmount"]
    info["coinAmountToday"] = result["item"]["coinAmountToday"]

    if result["code"] == 200:
        message = MessageSegment.text(
            "账号信息\n用户名: " + str(info["username"]) + "\n"
        )
        message += MessageSegment.text("邮箱: " + str(info["email"]) + "\n")
        message += MessageSegment.text("ID" + str(info["id"]) + "\n")
        message += MessageSegment.text("PayPal账号: " + str(info["paypel"]) + "\n")
        message += MessageSegment.text("硬币数量: " + str(info["coinAmount"]) + "\n")
        message += MessageSegment.text(
            "coinAmountToday: " + str(info["coinAmountToday"]) + "\n"
        )

        del login_dict[user_id]
        remember_key = [k for k in cookies_dict if k.startswith("remember_web_")][0]
        token = cookies_dict["XSRF-TOKEN"]
        session = cookies_dict["anymate_session"]
        remember_web = cookies_dict[remember_key]

        await SQL_Operate.insert_or_update_user_data(
            any_config.db_dir,
            any_config.user_table_name,
            user_id,
            token,
            session,
            remember_key,
            remember_web,
        )

        await log_in.finish(message)

    if result["code"] == 400:
        await log_in.reject("验证码错误，请重新输入")
    else:
        await log_in.finish(f"出现异常错误: \n错误码: {result['code']}")
