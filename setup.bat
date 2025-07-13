@echo off
echo.
echo ==========================================
echo Python学习助手 - 自动安装脚本
echo ==========================================
echo.

:: 检查 uv 是否已安装
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 uv 工具！
    echo 请访问 https://docs.astral.sh/uv/getting-started/installation/ 安装 uv
    echo.
    echo Windows 快速安装命令：
    echo powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    pause
    exit /b 1
)

echo [1/3] 检查 uv 版本...
uv --version

echo.
echo [2/3] 创建虚拟环境并安装依赖...
uv sync

echo.
echo [3/3] 安装开发依赖...
uv sync --extra dev

echo.
echo ==========================================
echo 🎉 安装完成！
echo ==========================================
echo.
echo 使用方法：
echo   启动程序： uv run python run.py
echo   运行测试： uv run pytest
echo   代码格式化： uv run black src/ examples/ test*.py run.py
echo   代码检查： uv run flake8 src/ examples/ test*.py run.py
echo   类型检查： uv run mypy src/
echo.
echo 或者激活虚拟环境后直接使用：
echo   .venv\Scripts\activate
echo   python run.py
echo.
pause
