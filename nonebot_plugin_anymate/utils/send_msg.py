from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot_plugin_saa import TargetQQPrivate, MessageFactory


async def send_private_msg(
    user_id: str,
    message: Message | str,
    bot: Bot
):
        
    message = str(message)

    target = TargetQQPrivate(user_id=user_id)
    await MessageFactory(message=message).send_to(target=target, bot=bot)
