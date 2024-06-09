import requests
from .api import get_info_api1, get_last_post_api, search_api, get_explore_api

# 通过uuid获取信息
def api_get_info_func(UUID: str) -> dict:
    """
    通过UUID获取用户信息。
    
    参数:
        UUID (str): 用户的UUID。
    
    返回:
        dict: 包含用户信息的字典。如果请求失败，则返回默认的空信息字典。
    """
    url = get_info_api1 + UUID

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    info = {'角色名': None, '账号ID': None, '角色ID': None, '年龄': None, '个人简介': None}
    
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result
    return info

# 通过名称搜索
def api_search_func(name: str, perPage: int = 5) -> dict:
    """
    通过名称搜索用户信息。
    
    参数:
        name (str): 要搜索的用户名。
        perPage (int): 每页返回的结果数量。默认值为5。
    
    返回:
        dict: 包含搜索结果的字典。如果请求失败，则返回None。
    """
    perPage = max(perPage, 5)
    url = search_api

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    params = {
        "pagination[perPage]": f"{perPage}",
        "filter[query]": name
    }
    
    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        return result

# 通过mateId获取动态
def api_get_last_post(mateId: str, perPage: int = 5) -> dict:
    """
    通过mateId获取用户的最新动态。
    
    参数:
        mateId (str): 用户的mateId。
        perPage (int): 每页返回的结果数量。默认值为5。
    
    返回:
        dict: 包含最新动态的字典。如果请求失败，则返回None。
    """
    perPage = max(perPage, 5)
    url = get_last_post_api
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    params = {
        "sort[field]": "dtCreate",
        "sort[order]": "desc",
        "filter[mateId]": mateId,
        "pagination[perPage]": perPage
    }

    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result

# 获取发现页
def apt_get_explore_post(perPage: int = 5) -> dict:
    """
    获取发现页的最新动态。
    
    参数:
        perPage (int): 每页返回的结果数量。默认值为5。
    
    返回:
        dict: 包含发现页最新动态的字典。如果请求失败，则返回None。
    """
    perPage = max(perPage, 5)
    url = get_explore_api
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    params = {
        "pagination[perPage]": perPage,
        "sort[field]": "dtCreate",
        "sort[order]": "desc"
    }

    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result
