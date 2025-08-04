#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动构建脚本 - 创建单文件Python应用
"""

import os
import sys
import shutil
from pathlib import Path

def create_single_file():
    """创建单文件应用"""
    
    print("📦 创建单文件Python应用...")
    
    # 读取主程序
    with open('run.py', 'r', encoding='utf-8') as f:
        main_code = f.read()
    
    # 读取依赖模块
    modules_code = []
    src_dir = Path('src')
    if src_dir.exists():
        for py_file in src_dir.glob('*.py'):
            if py_file.name != '__init__.py':
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    # 添加模块分隔注释
                    modules_code.append(f"# === {py_file.name} ===")
                    modules_code.append(code)
                    modules_code.append("")
    
    # 创建合并后的单文件
    combined_code = []
    combined_code.append("#!/usr/bin/env python3")
    combined_code.append("# -*- coding: utf-8 -*-")
    combined_code.append('"""')
    combined_code.append("Python学习助手 - 单文件版本")
    combined_code.append("包含所有依赖模块的独立版本")
    combined_code.append('"""')
    combined_code.append("")
    
    # 添加依赖模块代码
    if modules_code:
        combined_code.append("# ========== 依赖模块 ==========")
        combined_code.extend(modules_code)
        combined_code.append("# ========== 主程序 ==========")
    
    # 添加主程序代码
    combined_code.append(main_code)
    
    # 写入单文件应用
    output_file = 'python-learning-assistant-standalone.py'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(combined_code))
    
    print(f"✅ 单文件应用已创建: {output_file}")
    
    # 创建批处理启动脚本
    bat_content = """@echo off
chcp 65001 > nul
echo 启动Python学习助手...
python python-learning-assistant-standalone.py
pause
"""
    
    with open('start-standalone.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    print("✅ 启动脚本已创建: start-standalone.bat")

if __name__ == "__main__":
    create_single_file()
