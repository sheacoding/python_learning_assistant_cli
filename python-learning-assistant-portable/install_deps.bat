@echo off
chcp 65001 > nul
echo 安装Python依赖包...
pip install -r requirements.txt
echo 安装完成！
pause
