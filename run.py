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

# 设置标准输出编码为UTF-8，解决Windows下的编码问题
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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
        print("🔧 检测到缺少依赖包，正在安装...")
        for package in missing_packages:
            print(f"   安装 {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"   ❌ {package} 安装失败")
                print(f"   💡 请手动安装: pip install {package}")
                return False
        print("✅ 所有依赖安装完成！")
    
    return True

def check_api_key():
    """检查API密钥"""
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("⚠️  警告: 未设置 MOONSHOT_API_KEY 环境变量")
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
            print(f"❌ 缺少目录: {directory}")
            return False
    
    for file_path in required_files:
        if not file_path.exists():
            print(f"❌ 缺少文件: {file_path}")
            return False
    
    return True

def main():
    """主函数"""
    print("🐍 Python学习助手启动器")
    print("=" * 40)
    
    # 检查项目结构
    if not check_project_structure():
        print("❌ 项目结构不完整，请检查文件")
        sys.exit(1)
    
    # 检查依赖
    if not check_and_install_dependencies():
        print("❌ 依赖安装失败，程序退出")
        sys.exit(1)
    
    # 检查API密钥
    if not check_api_key():
        print("❌ API密钥未配置，程序退出")
        sys.exit(1)
    
    # 启动主程序
    print("🚀 启动Python学习助手...")
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, str(SRC_DIR))
        from main import main as run_assistant
        run_assistant()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 程序异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()