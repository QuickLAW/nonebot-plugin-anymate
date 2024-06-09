from distutils.core import setup
from setuptools import find_packages

with open("README", "r") as f:
  long_description = f.read()

setup(name='nonebot_plugin_anymate',  # 包名
      version='1.1.2',  # 版本号
      description='Nonebot上使用的anymate网站小工具',
      long_description=long_description,
      author='QuickLAW',
      author_email='yewillwork@outlook.com',
      url='https://github.com/QuickLAW',
      install_requires=[],
      license='BSD 3-Clause License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
      )
