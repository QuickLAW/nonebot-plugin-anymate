from datetime import datetime
import os
import pytz


def db_is_exist(db_dir: str):
    # 定义文件路径（这里假设文件在当前工作目录下）  
    file_path = db_dir
    
    # 使用os.path.exists()检查文件是否存在  
    if os.path.exists(file_path):  
        return True
    else:  
        return False
    

def time_to_format(dtCreate: str, timezone_str: str):
    timezone = pytz.timezone(timezone_str)

    time = datetime.fromisoformat(dtCreate.replace('Z', '+00:00')).replace(tzinfo=pytz.utc)
    time = time.astimezone(timezone) 
    return  time.strftime("%Y-%m-%d %H:%M:%S")
