import json
import os
import sqlite3

def creat_sql(db_dir: str):
    """
    创建SQLite数据库文件。如果数据库文件所在的文件夹不存在，则创建该文件夹。
    
    参数:
        db_dir (str): 数据库文件的路径。
    """
    folder_path = os.path.dirname(db_dir)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    sqlite3.connect(db_dir)
    return

def creat_table(db_dir: str, table_name: str, table_sql: str):
    """
    创建数据表。如果数据表不存在，则创建该数据表。
    
    参数:
        db_dir (str): 数据库文件的路径。
        table_name (str): 数据表的名称。
        table_sql (str): 创建数据表的SQL语句。
    """
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()
    c.execute(f"create table if not exists {table_name}{table_sql}")
    print(f"数据表 {table_name} 创建成功")
    conn.commit()
    conn.close()
    return

def insert_or_update_data(db_dir: str, table_name: str, name: str, UUID: str, mateId: str):
    """
    插入或更新数据。如果UUID已经存在，则更新name和mateId；否则，插入新记录。
    
    参数:
        db_dir (str): 数据库文件的路径。
        table_name (str): 数据表的名称。
        name (str): 角色名称。
        UUID (str): 角色UUID。
        mateId (str): 角色mateId。
    """
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()
    
    # 构造查询和插入/更新语句
    query_sql = f'''
        SELECT id FROM {table_name} WHERE UUID = ?;
    '''
    insert_sql = f'''
        INSERT INTO {table_name} (name, UUID, mateId)
        VALUES (?, ?, ?);
    '''
    update_sql = f'''
        UPDATE {table_name} SET name = ?, mateId = ? WHERE UUID = ?;
    '''
    
    # 查询是否已经存在具有相同UUID的记录
    c.execute(query_sql, (UUID,))
    result = c.fetchone()
    
    if result:
        # 如果存在，则更新name和mateId
        c.execute(update_sql, (name, mateId, UUID))
        print(f"UUID数据已存在，{name} 和 {mateId} 已更新")
    else:
        # 如果不存在，则插入新记录
        c.execute(insert_sql, (name, UUID, mateId))
        print(f"UUID数据{name}: {UUID} 已添加，mateId: {mateId}")
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()

def query_UUID_by_name(db_dir: str, table_name: str, name: str):
    """
    根据角色名查询UUID。
    
    参数:
        db_dir (str): 数据库文件的路径。
        table_name (str): 数据表的名称。
        name (str): 角色名称。
    
    返回:
        result (str): 查询到的UUID，如果没有找到匹配项，则返回None。
    """
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()
    
    # 构造查询语句
    query_sql = f'''
        SELECT UUID FROM {table_name} WHERE name LIKE ?;
    '''
    
    # 执行查询
    c.execute(query_sql, ('%'+name+'%',))
    result = c.fetchone()
    
    # 如果没有找到匹配项，返回None
    if result is None:
        return None
    
    # 返回找到的UUID
    return result

def insert_from_json(db_dir: str, table_name: str, json_file_path: str):
    """
    从JSON文件中读取数据并插入到数据库中。
    
    参数:
        db_dir (str): 数据库文件的路径。
        table_name (str): 数据表的名称。
        json_file_path (str): JSON文件的路径。
    """
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data: dict = json.load(file)
        
        # 遍历数据并插入到数据库
        for name, UUID in data.items():
            insert_or_update_data(db_dir, table_name, name, UUID)
    
    except Exception as e:
        print(f"发生错误: {e}")

def query_mateId_by_name(db_dir: str, table_name: str, name: str):
    """
    根据角色名查询mateId。
    
    参数:
        db_dir (str): 数据库文件的路径。
        table_name (str): 数据表的名称。
        name (str): 角色名称。
    
    返回:
        result (str): 查询到的mateId，如果没有找到匹配项，则返回None。
    """
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()
    
    # 构造查询语句
    query_sql = f'''
        SELECT mateId FROM {table_name} WHERE name LIKE ?;
    '''
    
    # 执行查询
    c.execute(query_sql, ('%'+name+'%',))
    result = c.fetchone()
    
    # 如果没有找到匹配项，返回None
    if result is None:
        return None
    
    # 返回找到的mateId
    return result

def query_name_by_name(db_dir: str, table_name: str, name: str) -> None | list:
    """
    根据角色名查询角色名列表。
    
    参数:
        db_dir (str): 数据库文件的路径。
        table_name (str): 数据表的名称。
        name (str): 角色名称。
    
    返回:
        result (list): 查询到的角色名列表，如果没有找到匹配项，则返回None。
    """
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()
    
    # 构造查询语句
    query_sql = f'''
        SELECT name FROM {table_name} WHERE name LIKE ?;
    '''
    
    # 执行查询
    c.execute(query_sql, ('%'+name+'%',))
    result = c.fetchall()
    
    # 如果没有找到匹配项，返回None
    if result is None:
        return None
    
    # 返回找到的name_list
    return [row[0] for row in result]
