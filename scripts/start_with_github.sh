#!/bin/bash

echo "========================================"
echo "微信公众号RSS合并服务 - GitHub版本"
echo "========================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖包..."
if ! python3 -c "import github" &> /dev/null; then
    echo "安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 检查GitHub令牌
if [ -z "$GITHUB_TOKEN" ]; then
    echo "警告: 未设置GITHUB_TOKEN环境变量"
    echo "GitHub上传功能将被禁用"
    echo "设置方法: export GITHUB_TOKEN=your_token"
    echo
fi

# 检查配置文件
if [ ! -f "config/config.yaml" ]; then
    echo "错误: 配置文件不存在，请检查config/config.yaml"
    exit 1
fi

echo "启动服务..."
echo "服务地址: http://localhost:8002"
echo "API接口: http://localhost:8002/generate"
echo

# 启动服务
python3 run.py 