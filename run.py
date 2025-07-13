#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python学习助手启动脚本
自动检查依赖并启动应用
"""

import sys
import subprocess
import importlib.util
import os
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
CONFIG_DIR = PROJECT_ROOT / "config"

def check_and_install_dependencies():
    """检查并安装依赖"""
    required_packages = {
        'openai': 'openai>=1.0.0',
        'requests': 'requests>=2.28.0'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(pip_name)
    
    if missing_packages:
        try:
            print("🔧 检测到缺少依赖包，正在安装...")
        except UnicodeEncodeError:
            print("检测到缺少依赖包，正在安装...")
        for package in missing_packages:
            try:
                print(f"   安装 {package}...")
            except UnicodeEncodeError:
                print(f"   安装 {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                try:
                    print(f"   ✅ {package} 安装成功")
                except UnicodeEncodeError:
                    print(f"   {package} 安装成功")
            except subprocess.CalledProcessError:
                try:
                    print(f"   ❌ {package} 安装失败")
                    print(f"   💡 请手动安装: pip install {package}")
                except UnicodeEncodeError:
                    print(f"   {package} 安装失败")
                    print(f"   请手动安装: pip install {package}")
                return False
        try:
            print("✅ 所有依赖安装完成！")
        except UnicodeEncodeError:
            print("所有依赖安装完成！")
    
    return True

def check_api_key():
    """检查API密钥"""
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        try:
            print("⚠️  警告: 未设置 MOONSHOT_API_KEY 环境变量")
            print("请设置环境变量后重试:")
            print("   Windows: set MOONSHOT_API_KEY=your_api_key")
            print("   Linux/Mac: export MOONSHOT_API_KEY=your_api_key")
        except UnicodeEncodeError:
            print("警告: 未设置 MOONSHOT_API_KEY 环境变量")
            print("请设置环境变量后重试:")
            print("   Windows: set MOONSHOT_API_KEY=your_api_key")
            print("   Linux/Mac: export MOONSHOT_API_KEY=your_api_key")
        return False
    return True

def check_project_structure():
    """检查项目结构"""
    required_dirs = [SRC_DIR, CONFIG_DIR]
    required_files = [
        SRC_DIR / "main.py",
        CONFIG_DIR / "config.json",
        PROJECT_ROOT / "requirements.txt"
    ]
    
    for directory in required_dirs:
        if not directory.exists():
            try:
                print(f"❌ 缺少目录: {directory}")
            except UnicodeEncodeError:
                print(f"缺少目录: {directory}")
            return False
    
    for file_path in required_files:
        if not file_path.exists():
            try:
                print(f"❌ 缺少文件: {file_path}")
            except UnicodeEncodeError:
                print(f"缺少文件: {file_path}")
            return False
    
    return True

def main():
    """主函数"""
    try:
        print("🐍 Python学习助手启动器")
    except UnicodeEncodeError:
        print("Python学习助手启动器")
    print("=" * 40)
    
    # 检查项目结构
    if not check_project_structure():
        try:
            print("❌ 项目结构不完整，请检查文件")
        except UnicodeEncodeError:
            print("项目结构不完整，请检查文件")
        sys.exit(1)
    
    # 检查依赖
    if not check_and_install_dependencies():
        try:
            print("❌ 依赖安装失败，程序退出")
        except UnicodeEncodeError:
            print("依赖安装失败，程序退出")
        sys.exit(1)
    
    # 检查API密钥
    if not check_api_key():
        try:
            print("❌ API密钥未配置，程序退出")
        except UnicodeEncodeError:
            print("API密钥未配置，程序退出")
        sys.exit(1)
    
    # 启动主程序
    try:
        print("🚀 启动Python学习助手...")
    except UnicodeEncodeError:
        print("启动Python学习助手...")
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, str(SRC_DIR))
        from main import main as run_assistant
        run_assistant()
    except ImportError as e:
        try:
            print(f"❌ 导入失败: {e}")
        except UnicodeEncodeError:
            print(f"导入失败: {e}")
        sys.exit(1)
    except Exception as e:
        try:
            print(f"❌ 程序异常: {e}")
        except UnicodeEncodeError:
            print(f"程序异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()