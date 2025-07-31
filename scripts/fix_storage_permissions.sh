#!/bin/bash

echo "========================================"
echo "存储目录权限修复脚本"
echo "========================================"

# 获取当前用户ID
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)

echo "当前用户ID: $CURRENT_UID:$CURRENT_GID"

echo "创建必要目录..."
mkdir -p ./storage ./logs ./config

echo "设置目录权限..."
chmod 755 ./storage ./logs ./config

echo "设置目录所有者..."
# 尝试设置所有者为当前用户
chown -R $CURRENT_UID:$CURRENT_GID ./storage ./logs 2>/dev/null || echo "无法设置所有者"

echo "检查目录权限..."
ls -la ./storage ./logs

echo "创建测试文件..."
echo '{"test": "data", "timestamp": "'$(date -Iseconds)'"}' > ./storage/test.json
chmod 644 ./storage/test.json

echo "检查文件权限..."
ls -la ./storage/

echo "测试文件写入..."
if [ -w ./storage/test.json ]; then
    echo "✅ 文件写入权限正常"
else
    echo "❌ 文件写入权限异常"
fi

echo "清理测试文件..."
rm -f ./storage/test.json

echo "✅ 权限修复完成！"
echo
echo "现在可以启动Docker Compose服务："
echo "docker-compose up -d" 