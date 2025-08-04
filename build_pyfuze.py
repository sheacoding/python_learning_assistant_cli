#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用pyfuze构建Python学习助手
pyfuze是一个轻量级的Python打包工具
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

def check_pyfuze():
    """检查pyfuze是否已安装"""
    try:
        # 先尝试直接调用pyfuze命令
        result = subprocess.run(['pyfuze', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pyfuze已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    try:
        # 再尝试通过python -m调用
        result = subprocess.run([sys.executable, '-m', 'pyfuze', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pyfuze已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ pyfuze未安装")
    return False

def install_pyfuze():
    """安装pyfuze"""
    print("🔧 正在安装pyfuze...")
    try:
        # 从GitHub安装pyfuze
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            'git+https://github.com/TanixLu/pyfuze.git'
        ])
        print("✅ pyfuze安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ pyfuze安装失败: {e}")
        return False

def create_pyfuze_config():
    """创建pyfuze配置文件"""
    config = {
        "name": "python-learning-assistant",
        "version": "1.0.0",
        "description": "Python学习助手 - 智能终端应用",
        "author": "Python学习助手团队",
        "entry_point": "run.py",
        "icon": None,
        "console": True,
        "include_files": [
            "src/",
            "config/",
            "sessions/",
            "examples/",
            "docs/",
            "requirements.txt",
            "README.md"
        ],
        "exclude_files": [
            "__pycache__/",
            "*.pyc",
            ".git/",
            ".venv/",
            "build/",
            "dist/"
        ],
        "hidden_imports": [
            "openai",
            "requests",
            "json",
            "datetime",
            "pathlib",
            "subprocess",
            "importlib.util",
            "time_manager",
            "api_key_manager"
        ],
        "optimize": True,
        "strip": False,
        "upx": False
    }
    
    config_file = "pyfuze.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已创建pyfuze配置文件: {config_file}")
    return config_file

def build_with_pyfuze():
    """使用pyfuze构建"""
    print("🔨 开始使用pyfuze构建...")
    
    try:
        # 先尝试直接调用pyfuze命令
        cmd = ['pyfuze', 'build', '--config', 'pyfuze.json']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ pyfuze构建成功！")
        print(result.stdout)
        
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ 直接调用pyfuze失败: {e}")
        
        try:
            # 再尝试通过python -m调用
            cmd = [sys.executable, '-m', 'pyfuze', 'build', '--config', 'pyfuze.json']
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print("✅ pyfuze构建成功！")
            print(result.stdout)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ pyfuze构建失败: {e}")
            if e.stderr:
                print(f"错误输出: {e.stderr}")
            if e.stdout:
                print(f"标准输出: {e.stdout}")
            return False

def create_manual_build():
    """创建手动构建脚本（如果pyfuze不可用）"""
    print("📝 创建手动构建脚本...")
    
    # 简化的单文件构建脚本
    build_script = '''#!/usr/bin/env python3
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
        f.write('\\n'.join(combined_code))
    
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
'''
    
    with open('manual_build.py', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    print("✅ 手动构建脚本已创建: manual_build.py")

def create_portable_package():
    """创建便携版包"""
    print("📦 创建便携版包...")
    
    portable_dir = Path("python-learning-assistant-portable")
    
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir()
    
    # 复制所有必要文件
    files_to_copy = [
        "run.py",
        "src/",
        "config/",
        "sessions/",
        "examples/",
        "docs/",
        "requirements.txt",
        "README.md"
    ]
    
    for item in files_to_copy:
        src = Path(item)
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, portable_dir / item)
            else:
                shutil.copy2(src, portable_dir / item)
    
    # 创建启动脚本
    start_script = portable_dir / "start.bat"
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write('''@echo off
chcp 65001 > nul
echo 启动Python学习助手...
python run.py
pause
''')
    
    # 创建安装依赖脚本
    install_script = portable_dir / "install_deps.bat"
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write('''@echo off
chcp 65001 > nul
echo 安装Python依赖包...
pip install -r requirements.txt
echo 安装完成！
pause
''')
    
    # 创建说明文件
    readme = portable_dir / "使用说明.txt"
    with open(readme, 'w', encoding='utf-8') as f:
        f.write('''Python学习助手 - 便携版

使用方法：
1. 首次使用请运行 install_deps.bat 安装依赖
2. 双击 start.bat 启动程序
3. 或者直接运行: python run.py

环境要求：
- Python 3.7+
- 网络连接（用于安装依赖和API调用）

配置说明：
- 在config/api_keys.json中配置API密钥
- 或设置环境变量MOONSHOT_API_KEY

文件说明：
- run.py: 主程序入口
- src/: 源代码目录
- config/: 配置文件
- sessions/: 学习记录保存
- examples/: 代码示例
- docs/: 文档说明

如有问题，请查看README.md文件
''')
    
    print(f"✅ 便携版包已创建: {portable_dir}")

def main():
    """主函数"""
    print("🐍 Python学习助手 - pyfuze构建工具")
    print("=" * 60)
    
    # 检查pyfuze是否安装
    if not check_pyfuze():
        print("🔧 尝试安装pyfuze...")
        if not install_pyfuze():
            print("❌ 无法安装pyfuze，将使用备用方案")
            create_manual_build()
            create_portable_package()
            print("\n💡 备用方案已准备就绪:")
            print("  1. 运行 python manual_build.py 创建单文件版本")
            print("  2. 使用 python-learning-assistant-portable/ 便携版")
            return
    
    # 创建pyfuze配置
    config_file = create_pyfuze_config()
    
    # 使用pyfuze构建
    if build_with_pyfuze():
        print("\n🎉 pyfuze构建完成！")
        
        # 检查输出文件
        dist_dir = Path("dist")
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            if exe_files:
                print(f"📁 可执行文件: {exe_files[0]}")
            else:
                print("📁 构建输出在 dist/ 目录中")
        
        # 同时创建便携版
        create_portable_package()
        
        print("\n💡 使用说明:")
        print("  - 如果有exe文件，直接运行即可")
        print("  - 便携版需要Python环境，但包含所有源码")
        
    else:
        print("❌ pyfuze构建失败，使用备用方案")
        create_manual_build()
        create_portable_package()

if __name__ == "__main__":
    main()