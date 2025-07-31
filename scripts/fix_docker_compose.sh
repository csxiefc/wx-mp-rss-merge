#!/bin/bash

echo "========================================"
echo "Docker Compose修复脚本"
echo "========================================"

echo "停止并删除容器..."
docker-compose down

echo "删除旧镜像..."
docker rmi wx-mp-rss-merge:latest 2>/dev/null || true

echo "重新构建镜像..."
docker build -t wx-mp-rss-merge:latest .

if [ $? -eq 0 ]; then
    echo
    echo "✅ 构建成功！正在启动服务..."
    echo
    
    echo "选择启动方式:"
    echo "1. 基本启动"
    echo "2. 带GitHub令牌启动"
    echo "3. 修复权限后启动"
    echo
    
    read -p "请输入选择 (1-3): " choice
    
    case $choice in
        1)
            docker-compose up -d
            ;;
        2)
            read -p "请输入GitHub令牌: " github_token
            export GITHUB_TOKEN="$github_token"
            docker-compose up -d
            ;;
        3)
            echo "修复权限..."
            # 确保目录存在并有正确权限
            mkdir -p ./storage ./logs
            chmod 755 ./storage ./logs
            chown -R 1000:1000 ./storage ./logs 2>/dev/null || true
            
            read -p "请输入GitHub令牌: " github_token
            export GITHUB_TOKEN="$github_token"
            docker-compose up -d
            ;;
        *)
            docker-compose up -d
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo
        echo "✅ 服务启动成功！"
        echo
        echo "查看服务状态:"
        echo "docker-compose ps"
        echo
        echo "查看日志:"
        echo "docker-compose logs wx-mp-rss-merge"
        echo
        echo "访问服务:"
        echo "http://localhost:8002"
        echo
        echo "测试API:"
        echo "curl http://localhost:8002/health"
        echo
        echo "测试生成JSON:"
        echo "curl http://localhost:8002/generate"
    else
        echo
        echo "❌ 服务启动失败！"
        echo "请检查配置或查看日志。"
    fi
else
    echo
    echo "❌ 构建失败！"
    echo "请检查网络连接或Docker配置。"
fi 