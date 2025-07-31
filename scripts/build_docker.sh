#!/bin/bash

echo "========================================"
echo "Docker快速构建脚本"
echo "========================================"

echo "选择构建方式:"
echo "1. 标准构建 (推荐)"
echo "2. 轻量级构建 (更快)"
echo "3. 使用缓存构建"
echo "4. 强制重新构建"
echo

read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo "开始标准构建..."
        docker build -t wx-mp-rss-merge:latest .
        ;;
    2)
        echo "开始轻量级构建..."
        docker build -f Dockerfile.light -t wx-mp-rss-merge:light .
        ;;
    3)
        echo "开始使用缓存构建..."
        docker build --no-cache=false -t wx-mp-rss-merge:latest .
        ;;
    4)
        echo "开始强制重新构建..."
        docker build --no-cache -t wx-mp-rss-merge:latest .
        ;;
    *)
        echo "无效选择，使用标准构建..."
        docker build -t wx-mp-rss-merge:latest .
        ;;
esac

if [ $? -eq 0 ]; then
    echo
    echo "✅ 构建成功！"
    echo
    echo "运行容器:"
    echo "docker run -d -p 8002:8002 --name wx-mp-rss wx-mp-rss-merge:latest"
    echo
    echo "运行容器（带环境变量）:"
    echo "docker run -d -p 8002:8002 -e GITHUB_TOKEN=your_token --name wx-mp-rss wx-mp-rss-merge:latest"
else
    echo
    echo "❌ 构建失败！"
    echo "请检查网络连接或尝试其他构建方式。"
fi 