@echo off
echo 启动微信公众号RSS合并服务（开发环境）...
echo.

echo 设置开发环境变量...
set ENVIRONMENT=development

echo.
echo 安全配置说明：
echo - API密钥: your-secret-api-key-2024
echo - 频率限制: 每分钟10次请求
echo - 生成接口需要API密钥认证
echo.

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
echo 启动Flask服务（开发环境）...
python run.py

pause 