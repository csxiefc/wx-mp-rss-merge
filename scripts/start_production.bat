@echo off
echo 启动微信公众号RSS合并服务（生产环境）...
echo.

echo 设置生产环境变量...
set ENVIRONMENT=production

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo Python未安装或未配置到PATH中
    pause
    exit /b 1
)

echo.
echo 安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 依赖安装失败
    pause
    exit /b 1
)

echo.
echo 启动Flask服务（生产环境）...
python run.py

pause 