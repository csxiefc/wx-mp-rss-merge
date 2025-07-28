#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微信公众号RSS合并服务安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# 读取requirements文件
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="wx-mp-rss-merge",
    version="1.0.0",
    author="Developer",
    author_email="developer@example.com",
    description="微信公众号RSS合并服务",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/wx-mp-rss-merge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "wx-mp-rss=run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json"],
    },
) 