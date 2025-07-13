#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python学习助手安装脚本
注意：推荐使用 pyproject.toml 进行现代化项目配置
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Python学习助手 - 一个功能丰富的Python学习终端应用"

# 读取requirements文件
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["openai>=1.0.0", "requests>=2.28.0"]

setup(
    name="python-learning-assistant",
    version="1.0.0",
    author="Python学习助手开发团队",
    author_email="",
    description="一个功能丰富的Python学习终端应用",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/python-learning-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "python-learning-assistant=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.json", "docs/*.md", "examples/*.py"],
    },
    license="MIT",  # 使用简单的license字段而不是分类器
)