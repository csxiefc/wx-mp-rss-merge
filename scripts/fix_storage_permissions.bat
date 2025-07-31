@echo off
echo ========================================
echo 存储目录权限修复脚本
echo ========================================

echo 创建必要目录...
if not exist storage mkdir storage
if not exist logs mkdir logs
if not exist config mkdir config

echo 设置目录权限...
icacls storage /grant Everyone:F /T
icacls logs /grant Everyone:F /T
icacls config /grant Everyone:F /T

echo 检查目录权限...
dir storage
dir logs

echo 创建测试文件...
echo {"test": "data", "timestamp": "%date% %time%"} > storage\test.json

echo 检查文件权限...
dir storage\test.json

echo 测试文件写入...
if exist storage\test.json (
    echo ✅ 文件写入权限正常
) else (
    echo ❌ 文件写入权限异常
)

echo 清理测试文件...
del storage\test.json

echo ✅ 权限修复完成！
echo.
echo 现在可以启动Docker Compose服务：
echo docker-compose up -d
pause 