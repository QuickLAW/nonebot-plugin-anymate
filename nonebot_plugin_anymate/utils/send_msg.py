from nonebot import require
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.bot import Bot as OnebotV11Bot

require("nonebot_plugin_saa")
from nonebot_plugin_saa import TargetQQPrivate, MessageFactory


async def send_private_msg(
    user_id: str,
    message: Message | str,
    bot: OnebotV11Bot
):
        
    message = str(message)

    target = TargetQQPrivate(user_id=user_id)
    await MessageFactory(message=message).send_to(target=target, bot=bot)
