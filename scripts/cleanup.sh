#!/bin/bash

echo "========================================"
echo "微信公众号RSS合并服务 - 清理脚本"
echo "========================================"

echo "清理Python缓存文件..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

echo "清理临时文件..."
rm -f *.log *.tmp *.temp result.html result.json 2>/dev/null || true

echo "清理旧存储文件..."
if [ -d "storage" ]; then
    echo "保留最新的result.json，删除其他文件..."
    find storage -name "*.json" ! -name "result.json" -delete 2>/dev/null || true
fi

echo "清理测试文件..."
if [ -d "testres" ]; then
    rm -f testres/*.txt testres/*.json 2>/dev/null || true
fi

echo "清理完成！" 