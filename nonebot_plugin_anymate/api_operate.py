import httpx
from urllib.parse import unquote

from .api import (
    get_info_api1,
    get_last_post_api,
    search_api,
    get_explore_api,
    login_api,
    code_api,
    get_login_token_api,
    check_in_api,
    upvote_api,
    get_mate_page,
)


# 通过uuid获取信息
async def api_get_info_func(UUID: str) -> dict:
    """
    通过UUID获取用户信息。

    参数:
        UUID (str): 用户的UUID。

    返回:
        dict: 包含用户信息的字典。如果请求失败，则返回默认的空信息字典。
    """
    url = get_info_api1 + UUID

    headers = {"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(url=url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result


# 通过名称搜索
async def api_search_func(name: str, perPage: int = 5) -> dict:
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

    headers = {"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    params = {"pagination[perPage]": f"{perPage}", "filter[query]": name}

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            return result


# 通过mateId获取动态
async def api_get_last_post(mateId: str, perPage: int = 5) -> dict:
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
    headers = {"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    params = {
        "sort[field]": "dtCreate",
        "sort[order]": "desc",
        "filter[mateId]": mateId,
        "pagination[perPage]": perPage,
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(url=url, params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result


# 获取发现页
async def api_get_explore_post(perPage: int = 5) -> dict:
    """
    获取发现页的最新动态。

    参数:
        perPage (int): 每页返回的结果数量。默认值为5。

    返回:
        dict: 包含发现页最新动态的字典。如果请求失败，则返回None。
    """
    perPage = max(perPage, 5)
    url = get_explore_api
    headers = {"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    params = {
        "pagination[perPage]": perPage,
        "sort[field]": "dtCreate",
        "sort[order]": "desc",
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(url=url, params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result


# 登录操作
async def api_login(email, cookies: dict) -> dict:
    json_data = {"email": email}

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "X-Xsrf-Token": cookies["XSRF-TOKEN"],
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        flag = 0
        while flag < 10:
            try:
                response = await client.post(
                    url=login_api, headers=headers, json=json_data, cookies=cookies
                )
                break
            except httpx.ReadTimeout:
                flag += 1
        if response.status_code == 200:
            result = response.json()
            cookies = response.cookies.jar
            cookies_dict = {cookie.name: unquote(cookie.value) for cookie in cookies}
            return result, cookies_dict
        if response.status_code == 404:
            return {"code": 404}
        return response.json(), {}


# 提交邮箱验证码
async def api_post_code(email: str, code: str, cookies) -> dict:
    name = email.split("@")[0]

    json_data = {
        "email": email,
        "name": name,
        "settingDisplayLanguageId": "2",
        "settingMateLanguageId": "2",
        "token": int(code),
    }

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "X-Xsrf-Token": cookies["XSRF-TOKEN"],
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.post(
            url=code_api, headers=headers, json=json_data, cookies=cookies
        )
        if response.status_code == 200:
            result = response.json()
            cookies = response.cookies.jar
            cookies_dict = {cookie.name: unquote(cookie.value) for cookie in cookies}
            return result, cookies_dict
        if response.status_code == 404:
            return {"code": 404}, {}
        if response.status_code == 419:
            return {"code": 419}, {}
        return {"code": response.status_code}, {}


# 获取预登录token
async def api_get_login_token():
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(get_login_token_api)
        cookies = response.cookies.jar
        cookies_dict = {cookie.name: unquote(cookie.value) for cookie in cookies}
        return cookies_dict


# 签到操作
async def api_check_in(cookies: dict):
    json_data = {"coinQuestId": 1}

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "X-Xsrf-Token": cookies["XSRF-TOKEN"],
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.post(
            url=check_in_api, headers=headers, json=json_data, cookies=cookies
        )
        if response.status_code == 200:
            result: dict = response.json()
            cookies = response.cookies.jar
            cookies_dict: dict = {
                cookie.name: unquote(cookie.value) for cookie in cookies
            }
            return result, cookies_dict
        if response.status_code == 404:
            return {"code": 404}, {}
        if response.status_code == 400:
            return {"code": 400}, {}
        return {"code": response.status_code}, {}


# 通过remember获取token
async def api_get_token_by_remember(cookies: dict):

    headers = {"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(
            get_login_token_api, cookies=cookies, headers=headers
        )
        cookies = response.cookies.jar
        cookies_dict = {cookie.name: unquote(cookie.value) for cookie in cookies}
        return cookies_dict


# 点赞功能
async def api_upvote(emojiId: int, replyId: int, UUID: str, cookies: dict):

    json_data = {"emojiId": emojiId, "replyId": replyId, "mateId": UUID}

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "X-Xsrf-Token": cookies["XSRF-TOKEN"],
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.post(
            url=upvote_api, headers=headers, json=json_data, cookies=cookies
        )
        if response.status_code == 200:
            result: dict = response.json()
            cookies = response.cookies.jar
            cookies_dict: dict = {
                cookie.name: unquote(cookie.value) for cookie in cookies
            }
            return result, cookies_dict
        if response.status_code == 404:
            return {"code": 404}, {}
        if response.status_code == 400:
            return {"code": 400}, {}
        return {"code": response.status_code}, {}


# 通过token获取账户mate信息
async def api_get_mate_page(cookies: dict) -> dict:
    """
    通过token获取用户的最新动态。

    参数:
        cookies (dict): 存有token的cookies

    返回:
        dict: 包含最新动态的字典。如果请求失败，则返回None。
    """
    url = get_mate_page
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "X-Xsrf-Token": cookies["XSRF-TOKEN"],
        }
    params = {
        "sort[field]": "id",
        "sort[order]": "desc",
        "pagination[page]": "1",
        "pagination[perPage]": "999"
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=10)) as client:
        response = await client.get(url=url, params=params, headers=headers, cookies=cookies)
        if response.status_code == 200:
            result = response.json()
            cookies = response.cookies.jar
            cookies_dict = {cookie.name: unquote(cookie.value) for cookie in cookies}
            return result, cookies_dict
        else:
            return {'code': response.status_code}, {}

