@echo off
echo =====================================
echo 简儿QQ机器人 WebSocket问题自动修复
echo =====================================
echo.

echo 检查编译环境...
python -c "import sys; print(f'Python版本: {sys.version}')" 2>nul
echo.

echo 正在卸载冲突的WebSocket包...
pip uninstall websockets gevent-websocket bottle-websocket websocket-client -y

echo.
echo 正在重新安装兼容版本（使用预编译包）...
pip install "websockets>=10.0,<11.0" --only-binary=all --no-compile
pip install "websocket-client>=1.8.0" --only-binary=all
pip install "aiohttp>=3.8.0" --only-binary=all --no-compile

echo.
echo 验证修复结果...
python -c "import websockets; print('✓ websockets库正常'); print(f'版本: {websockets.__version__}')" 2>nul
if %errorlevel% neq 0 (
    echo ✗ websockets库导入失败
    echo 正在尝试安装Microsoft Visual C++ Build Tools...
    echo 请按照以下步骤操作：
    echo 1. 访问：https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo 2. 下载并安装 Microsoft C++ Build Tools
    echo 3. 或者运行：pip install --only-binary=all aiohttp
    goto error
)

python -c "import websocket; print('✓ websocket-client库正常')" 2>nul
if %errorlevel% neq 0 (
    echo ✗ websocket-client库导入失败
    goto error
)

python -c "import aiohttp; print('✓ aiohttp库正常')" 2>nul
if %errorlevel% neq 0 (
    echo ! aiohttp库可能需要C++编译环境
    echo 建议安装预编译版本：pip install --only-binary=all aiohttp
)

echo.
echo =====================================
echo ✅ WebSocket问题修复完成！
echo =====================================
echo.
echo 现在可以尝试启动程序：
echo python main.py
echo.
goto end

:error
echo.
echo =====================================
echo ❌ 修复过程中出现错误！
echo =====================================
echo.
echo 请尝试以下解决方案：
echo.
echo 方案1：安装Microsoft Visual C++ Build Tools
echo 1. 访问：https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo 2. 下载并安装 "C++ build tools" 工作负载
echo.
echo 方案2：使用预编译包
echo pip install --upgrade pip
echo pip install --only-binary=all aiohttp websockets
echo.
echo 方案3：使用conda环境
echo conda install -c conda-forge aiohttp websockets
echo.

:end
pause