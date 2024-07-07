from distutils.core import setup
from pathlib import Path
from setuptools import find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="nonebot_plugin_anymate",  # 包名
    version="1.4.0.1",  # 版本号
    description="QQ上使用的anymate网站小工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="QuickLAW",
    author_email="yewillwork@outlook.com",
    url="https://github.com/QuickLAW/nonebot-plugin-anymate",
    install_requires=[
        "nonebot2",
        "pytz",
        "httpx",
        "pydantic",
        "nonebot-adapter-onebot",
        "aiosqlite",
        "nonebot-plugin-send-anything-anywhere",
    ],
    license="BSD 3-Clause License",
    packages=find_packages(),
    platforms=["~onebot.v11"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
)
