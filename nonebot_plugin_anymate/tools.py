from datetime import datetime
import os
import re
import pytz


class Tools:
    def __init__(self) -> None:
        self._name = "常用函数"

    def db_is_exist(db_dir: str) -> bool:
        """
        检查数据库文件是否存在。

        参数:
            db_dir (str): 数据库文件的路径。

        返回:
            bool: 如果文件存在，返回True；否则，返回False。
        """
        # 使用os.path.exists()检查文件是否存在
        return os.path.exists(db_dir)

    def time_to_format(dtCreate: str, timezone_str: str) -> str:
        """
        将时间字符串转换为指定时区的格式化时间字符串。

        参数:
            dtCreate (str): 原始时间字符串（ISO格式）。
            timezone_str (str): 目标时区的名称。

        返回:
            str: 格式化后的时间字符串，格式为"%Y-%m-%d %H:%M:%S"。
        """
        # 获取指定的时区
        timezone = pytz.timezone(timezone_str)

        # 将时间字符串转换为带有UTC时区信息的datetime对象
        time = datetime.fromisoformat(dtCreate.replace("Z", "+00:00")).replace(
            tzinfo=pytz.utc
        )

        # 将时间转换为指定的时区
        time = time.astimezone(timezone)

        # 返回格式化后的时间字符串
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def is_valid_email(email):
        email_re = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+$")
        return email_re.match(email) is not None
