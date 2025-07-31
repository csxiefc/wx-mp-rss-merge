@echo off
echo ========================================
echo 微信公众号RSS合并服务 - GitHub版本
echo ========================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
pip show PyGithub >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查GitHub令牌
if "%GITHUB_TOKEN%"=="" (
    echo 警告: 未设置GITHUB_TOKEN环境变量
    echo GitHub上传功能将被禁用
    echo 设置方法: set GITHUB_TOKEN=your_token
    echo.
)

REM 检查配置文件
if not exist "config\config.yaml" (
    echo 错误: 配置文件不存在，请检查config\config.yaml
    pause
    exit /b 1
)

echo 启动服务...
echo 服务地址: http://localhost:8002
echo API接口: http://localhost:8002/generate
echo.

REM 启动服务
python run.py

pause 