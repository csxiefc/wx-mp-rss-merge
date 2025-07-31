#!/bin/bash

echo "========================================"
echo "权限修复脚本"
echo "========================================"

echo "创建必要目录..."
mkdir -p ./storage ./logs ./config

echo "设置目录权限..."
chmod 755 ./storage ./logs ./config

echo "设置目录所有者（如果可能）..."
# 尝试设置所有者，如果失败则忽略
chown -R 1000:1000 ./storage ./logs 2>/dev/null || echo "无法设置所有者，继续..."

echo "检查目录权限..."
ls -la ./storage ./logs

echo "创建测试文件..."
echo '{"test": "data"}' > ./storage/test.json
chmod 644 ./storage/test.json

echo "检查文件权限..."
ls -la ./storage/

echo "清理测试文件..."
rm -f ./storage/test.json

echo "✅ 权限修复完成！"
echo
echo "现在可以启动Docker Compose服务："
echo "docker-compose up -d" 