#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python学习助手测试脚本
用于验证项目结构和基本功能
"""

import os
import sys
import json
from pathlib import Path

def safe_print(text):
    """安全打印，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 移除特殊字符，只保留基本内容
        clean_text = text.replace("✅", "[OK]").replace("❌", "[FAIL]").replace("🐍", "Python")
        print(clean_text)

def test_project_structure():
    """测试项目结构"""
    safe_print("=== 测试项目结构 ===")
    
    # 检查目录
    directories = ['src', 'config', 'docs', 'examples', 'sessions']
    for directory in directories:
        if os.path.exists(directory):
            safe_print(f"[OK] 目录存在: {directory}")
        else:
            safe_print(f"[FAIL] 目录缺失: {directory}")
    
    # 检查关键文件
    files = [
        'src/main.py',
        'config/config.json',
        'requirements.txt',
        'run.py',
        'setup.py',
        'README.md'
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            safe_print(f"[OK] 文件存在: {file_path}")
        else:
            safe_print(f"[FAIL] 文件缺失: {file_path}")
    
    print()

def test_config_file():
    """测试配置文件"""
    safe_print("=== 测试配置文件 ===")
    
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        safe_print("[OK] 配置文件加载成功")
        safe_print(f"   模型: {config.get('model', 'N/A')}")
        safe_print(f"   温度: {config.get('temperature', 'N/A')}")
        safe_print(f"   最大tokens: {config.get('max_tokens', 'N/A')}")
        safe_print(f"   自动保存: {config.get('auto_save_sessions', 'N/A')}")
        
    except Exception as e:
        safe_print(f"[FAIL] 配置文件加载失败: {e}")
    
    print()

def test_examples():
    """测试示例代码"""
    safe_print("=== 测试示例代码 ===")
    
    # 测试基础示例
    try:
        sys.path.insert(0, 'examples')
        import basic_examples
        safe_print("[OK] 基础示例导入成功")
        
        # 测试一个简单函数
        if hasattr(basic_examples, 'basic_variables_and_types'):
            safe_print("[OK] 基础变量示例函数存在")
        else:
            safe_print("[FAIL] 基础变量示例函数不存在")
            
    except Exception as e:
        safe_print(f"[FAIL] 基础示例导入失败: {e}")
    
    # 测试高级示例
    try:
        import advanced_examples
        safe_print("[OK] 高级示例导入成功")
        
        if hasattr(advanced_examples, 'advanced_decorators'):
            safe_print("[OK] 高级装饰器示例函数存在")
        else:
            safe_print("[FAIL] 高级装饰器示例函数不存在")
            
    except Exception as e:
        safe_print(f"[FAIL] 高级示例导入失败: {e}")
    
    print()

def test_syntax_highlighter():
    """测试语法高亮器"""
    safe_print("=== 测试语法高亮器 ===")
    
    try:
        sys.path.insert(0, 'src')
        from main import PythonSyntaxHighlighter
        
        # 测试代码高亮
        test_code = """def hello_world():
    print("Hello, World!")
    return True"""
        
        highlighted = PythonSyntaxHighlighter.highlight(test_code)
        safe_print("[OK] 语法高亮器工作正常")
        safe_print("高亮测试:")
        safe_print(highlighted)
        
    except Exception as e:
        safe_print(f"[FAIL] 语法高亮器测试失败: {e}")
    
    print()

def test_conversation_history():
    """测试对话历史管理"""
    safe_print("=== 测试对话历史管理 ===")
    
    try:
        sys.path.insert(0, 'src')
        from main import ConversationHistory
        
        # 创建历史管理器
        history = ConversationHistory(sessions_dir='sessions')
        safe_print("[OK] 对话历史管理器创建成功")
        
        # 添加测试消息
        history.add_message('user', '测试用户消息')
        history.add_message('assistant', '测试助手回复')
        
        # 获取上下文
        context = history.get_context_messages(2)
        if len(context) == 2:
            safe_print("[OK] 对话上下文获取正常")
        else:
            safe_print("[FAIL] 对话上下文获取异常")
        
        # 测试保存会话
        filename = history.save_session()
        if filename and os.path.exists(filename):
            safe_print("[OK] 会话保存成功")
            # 清理测试文件
            os.remove(filename)
        else:
            safe_print("[FAIL] 会话保存失败")
        
    except Exception as e:
        safe_print(f"[FAIL] 对话历史管理测试失败: {e}")
    
    print()

def test_dependencies():
    """测试依赖包"""
    safe_print("=== 测试依赖包 ===")
    
    dependencies = ['openai', 'requests']
    
    for dep in dependencies:
        try:
            __import__(dep)
            safe_print(f"[OK] 依赖包可用: {dep}")
        except ImportError:
            safe_print(f"[FAIL] 依赖包缺失: {dep}")
    
    print()

def main():
    """主测试函数"""
    safe_print("Python学习助手 - 项目测试")
    print("=" * 50)
    
    test_project_structure()
    test_config_file()
    test_examples()
    test_syntax_highlighter()
    test_conversation_history()
    test_dependencies()
    
    print("=" * 50)
    safe_print("测试完成!")

if __name__ == "__main__":
    main()