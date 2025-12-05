@echo off
chcp 65001 >nul
echo ========================================
echo   登录自动化测试 - 快速开始
echo ========================================
echo.

:menu
echo 请选择操作:
echo 1. 安装依赖包
echo 2. 生成测试数据Excel
echo 3. 运行所有测试
echo 4. 运行测试并生成报告
echo 5. 仅查看Allure报告
echo 0. 退出
echo.
set /p choice=请输入选项 (0-5): 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto generate
if "%choice%"=="3" goto test
if "%choice%"=="4" goto test_report
if "%choice%"=="5" goto report
if "%choice%"=="0" goto end
echo 无效选项，请重新选择
goto menu

:install
echo.
echo 正在安装依赖包...
pip install -r requirements.txt
echo.
echo 依赖包安装完成！
pause
goto menu

:generate
echo.
echo 正在生成测试数据Excel文件...
python generate_test_data.py
echo.
pause
goto menu

:test
echo.
echo 正在运行测试...
pytest
echo.
echo 测试执行完成！
pause
goto menu

:test_report
echo.
echo 正在运行测试...
pytest
echo.
echo 正在生成Allure报告...
allure generate reports/allure -o reports/allure-report --clean
echo.
echo 正在打开Allure报告...
allure open reports/allure-report
goto menu

:report
echo.
echo 正在生成并打开Allure报告...
allure generate reports/allure -o reports/allure-report --clean
allure open reports/allure-report
goto menu

:end
echo.
echo 再见！
exit
