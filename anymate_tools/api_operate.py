import requests
from .api import get_info_api1, get_last_post_api, search_api, get_explore_api


# 通过uuid获取信息
def api_get_info_func(UUID)->dict:
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
def api_search_func(name, perPage: int = 5)->dict:
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
def api_get_last_post(mateId, perPage: int = 5):
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
def apt_get_explore_post(perPage: int = 5):
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


