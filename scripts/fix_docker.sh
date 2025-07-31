#!/bin/bash

echo "========================================"
echo "Docker快速修复脚本"
echo "========================================"

echo "停止并删除旧容器..."
docker stop wx-mp-rss-merge 2>/dev/null || true
docker rm wx-mp-rss-merge 2>/dev/null || true

echo "删除旧镜像..."
docker rmi wx-mp-rss-merge:latest 2>/dev/null || true

echo "重新构建镜像..."
docker build -t wx-mp-rss-merge:latest .

if [ $? -eq 0 ]; then
    echo
    echo "✅ 构建成功！正在启动容器..."
    echo
    
    echo "选择运行方式:"
    echo "1. 基本运行"
    echo "2. 带GitHub令牌运行"
    echo "3. 带环境变量运行"
    echo "4. 测试权限运行"
    echo
    
    read -p "请输入选择 (1-4): " run_choice
    
    case $run_choice in
        1)
            docker run -d -p 8002:8002 --name wx-mp-rss-merge wx-mp-rss-merge:latest
            ;;
        2)
            read -p "请输入GitHub令牌: " github_token
            docker run -d -p 8002:8002 -e GITHUB_TOKEN="$github_token" --name wx-mp-rss-merge wx-mp-rss-merge:latest
            ;;
        3)
            read -p "请输入GitHub令牌: " github_token
            read -p "请输入数据库主机 (默认: 106.13.63.117): " db_host
            db_host=${db_host:-106.13.63.117}
            docker run -d -p 8002:8002 -e GITHUB_TOKEN="$github_token" -e DB_HOST="$db_host" --name wx-mp-rss-merge wx-mp-rss-merge:latest
            ;;
        4)
            echo "启动测试容器..."
            docker run -d -p 8002:8002 --name wx-mp-rss-merge-test wx-mp-rss-merge:latest
            sleep 5
            echo "执行权限测试..."
            docker exec wx-mp-rss-merge-test python test_permissions.py
            echo "查看容器日志..."
            docker logs wx-mp-rss-merge-test
            echo "停止测试容器..."
            docker stop wx-mp-rss-merge-test
            docker rm wx-mp-rss-merge-test
            ;;
        *)
            docker run -d -p 8002:8002 --name wx-mp-rss-merge wx-mp-rss-merge:latest
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo
        echo "✅ 容器启动成功！"
        echo
        echo "查看容器状态:"
        echo "docker ps"
        echo
        echo "查看容器日志:"
        echo "docker logs wx-mp-rss-merge"
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
        echo "❌ 容器启动失败！"
        echo "请检查端口是否被占用或查看日志。"
    fi
else
    echo
    echo "❌ 构建失败！"
    echo "请检查网络连接或Docker配置。"
fi 