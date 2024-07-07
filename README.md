<div align="center">

# nonebot-plugin-anymate

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-anymate.svg" alt="license">
</a>
<a href="https://pypi.org/project/nonebot-plugin-anymate/">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-anymate.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

AnymateTools是一款[NoneBot](https://nonebot.dev/)上使用的插件，可以便捷的通过此插件来浏览[Anymate](https://www.any-mate.com/)网站的部分内容。


## 📖 介绍

安装此插件后，在群聊/私聊可以使用，添加角色到数据库之后，可以查看角色信息，查看角色动态，催更（角色暂时还收不到），查看发现页动态等功能。可以通过群聊便捷的催促作者更新。


## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| UTC | 否 | "Asia/Shanghai" | 设置时区 |
| DB_DIR | 否 | "./data/anymate/data.db" | 数据库默认存放位置及名称 |

## 🎉 使用
### 指令表
| 指令 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|
| /anyhelp | 否 | 群聊/私聊 | 列出所有可用指令 |
| /信息 <角色> | 否 | 群聊/私聊 | 展示指定角色的信息 |
| /动态 <角色名> [数量] | 否 | 群聊/私聊 | 展示指定角色指定数量的最新动态 |
| /搜索 <角色名> [数量] | 否 | 群聊/私聊 | 搜索角色并展示指定数量的结果 |
| /添加角色 <UUID> | 否 | 群聊/私聊 | 将指定角色添加入插件数据库 |
| /催更 <角色名> | 否 | 群聊/私聊 | 催更啦！ |
| /发现 [数量] | 否 | 群聊/私聊 | 展示指定数量的发现页帖子 |
| /anylogin | 否 | 群聊/私聊 | 进入登录流程 |
| /any签到 | 否 | 群聊/私聊 | 手动实现每日签到 |


<details open>
<summary>使用方法</summary>

1. 先使用"/搜索 <角色名>"的指令查找对应的角色，可以获取到角色的UUID
<img src="https://github.com/QuickLAW/nonebot-plugin-anymate/blob/main/img/101.jpg"  width="300" />

指令：

    /搜索 白璃

2. 使用"/添加角色 <UUID>"来将指定角色添加到数据库中
<img src="https://github.com/QuickLAW/nonebot-plugin-anymate/blob/main/img/102.jpg"  width="300" />

指令：

    /添加角色 5093d34b-3b29-4822-abd1-d39402faa6cf

3. 之后就可以对指定角色使用"催更"、"动态"、"信息"等功能啦
<img src="https://github.com/QuickLAW/nonebot-plugin-anymate/blob/main/img/103.jpg"  width="300" />

指令：

    /催更 白璃

</details>
