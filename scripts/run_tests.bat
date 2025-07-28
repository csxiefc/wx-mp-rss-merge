@echo off
echo 运行微信公众号RSS合并服务测试...
echo.

echo 1. 测试模块导入...
python -c "from src.core.database import DatabaseManager; print('✓ DatabaseManager 导入成功')"
if %errorlevel% neq 0 (
    echo ✗ DatabaseManager 导入失败
    pause
    exit /b 1
)

echo 2. 测试数据库连接...
python tests/test_database.py
if %errorlevel% neq 0 (
    echo ✗ 数据库连接测试失败
    pause
    exit /b 1
)

echo 3. 测试完整流程...
python tests/test_integration.py
if %errorlevel% neq 0 (
    echo ✗ 完整流程测试失败
    pause
    exit /b 1
)

echo.
echo 所有测试通过！
pause 