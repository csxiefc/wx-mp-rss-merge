@echo off
echo ========================================
echo 微信公众号RSS合并服务 - 清理脚本
echo ========================================

echo 清理Python缓存文件...
if exist __pycache__ rmdir /s /q __pycache__
if exist src\__pycache__ rmdir /s /q src\__pycache__
if exist src\api\__pycache__ rmdir /s /q src\api\__pycache__
if exist src\core\__pycache__ rmdir /s /q src\core\__pycache__
if exist src\utils\__pycache__ rmdir /s /q src\utils\__pycache__

echo 清理临时文件...
if exist *.log del *.log
if exist *.tmp del *.tmp
if exist *.temp del *.temp
if exist result.html del result.html
if exist result.json del result.json

echo 清理旧存储文件...
if exist storage\*.json (
    echo 保留最新的result.json，删除其他文件...
    for %%f in (storage\*.json) do (
        if not "%%~nxf"=="result.json" del "%%f"
    )
)

echo 清理测试文件...
if exist testres\*.txt del testres\*.txt
if exist testres\*.json del testres\*.json

echo 清理完成！
pause 