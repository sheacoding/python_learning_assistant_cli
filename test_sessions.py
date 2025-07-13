#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话保存和学习记录功能测试
"""

import os
import sys
import json
import datetime
from pathlib import Path

def safe_print(text):
    """安全打印，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.replace("✅", "[OK]").replace("❌", "[FAIL]").replace("🔍", "[TEST]")
        print(clean_text)

def test_session_directory():
    """测试会话目录"""
    safe_print("🔍 测试1: 会话目录检查")
    
    sessions_dir = Path("sessions")
    if sessions_dir.exists():
        safe_print(f"✅ 会话目录存在: {sessions_dir.absolute()}")
        
        # 检查目录权限
        if os.access(sessions_dir, os.W_OK):
            safe_print("✅ 会话目录可写")
        else:
            safe_print("❌ 会话目录不可写")
            return False
    else:
        safe_print("❌ 会话目录不存在，尝试创建...")
        try:
            sessions_dir.mkdir(exist_ok=True)
            safe_print("✅ 会话目录创建成功")
        except Exception as e:
            safe_print(f"❌ 会话目录创建失败: {e}")
            return False
    
    return True

def test_conversation_history_basic():
    """测试基本对话历史功能"""
    safe_print("\n🔍 测试2: 基本对话历史功能")
    
    try:
        # 添加src到路径
        sys.path.insert(0, 'src')
        from main import ConversationHistory
        
        # 创建历史管理器
        history = ConversationHistory(sessions_dir='sessions')
        safe_print("✅ ConversationHistory 创建成功")
        
        # 测试添加消息
        history.add_message('user', '测试用户消息1')
        history.add_message('assistant', '测试助手回复1')
        history.add_message('user', '测试用户消息2')
        history.add_message('assistant', '测试助手回复2')
        
        safe_print(f"✅ 添加了4条消息，当前历史长度: {len(history.history)}")
        
        # 测试获取上下文
        context = history.get_context_messages(3)
        if len(context) == 3:
            safe_print("✅ 上下文获取正常")
        else:
            safe_print(f"❌ 上下文获取异常，期望3条，实际{len(context)}条")
            return False
        
        return history
        
    except Exception as e:
        safe_print(f"❌ ConversationHistory 测试失败: {e}")
        return None

def test_session_save_load(history):
    """测试会话保存和加载"""
    safe_print("\n🔍 测试3: 会话保存和加载")
    
    if not history:
        safe_print("❌ 无法测试：历史对象为空")
        return False
    
    try:
        # 保存会话
        saved_file = history.save_session()
        if saved_file and os.path.exists(saved_file):
            safe_print(f"✅ 会话保存成功: {saved_file}")
            
            # 验证文件内容
            with open(saved_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            required_keys = ['session_start', 'session_end', 'history']
            for key in required_keys:
                if key in session_data:
                    safe_print(f"✅ 会话文件包含必需字段: {key}")
                else:
                    safe_print(f"❌ 会话文件缺少字段: {key}")
                    return False
            
            # 检查历史数据
            if len(session_data['history']) == 4:
                safe_print("✅ 会话历史数据完整")
            else:
                safe_print(f"❌ 会话历史数据不完整，期望4条，实际{len(session_data['history'])}条")
                return False
            
            # 测试加载会话
            new_history = ConversationHistory(sessions_dir='sessions')
            filename_only = os.path.basename(saved_file)
            new_history.load_session(filename_only)
            
            if len(new_history.history) == 4:
                safe_print("✅ 会话加载成功")
            else:
                safe_print(f"❌ 会话加载失败，期望4条，实际{len(new_history.history)}条")
                return False
            
            # 清理测试文件
            os.remove(saved_file)
            safe_print("✅ 测试文件已清理")
            
            return True
            
        else:
            safe_print("❌ 会话保存失败")
            return False
            
    except Exception as e:
        safe_print(f"❌ 会话保存/加载测试失败: {e}")
        return False

def test_message_metadata():
    """测试消息元数据功能"""
    safe_print("\n🔍 测试4: 消息元数据功能")
    
    try:
        sys.path.insert(0, 'src')
        from main import ConversationHistory
        
        history = ConversationHistory(sessions_dir='sessions')
        
        # 添加带元数据的消息
        metadata = {
            'topic': 'Python列表',
            'difficulty': 'beginner',
            'code_executed': True
        }
        
        history.add_message('user', '什么是Python列表？', metadata)
        
        # 检查消息结构
        last_message = history.history[-1]
        expected_fields = ['role', 'content', 'timestamp', 'metadata']
        
        for field in expected_fields:
            if field in last_message:
                safe_print(f"✅ 消息包含字段: {field}")
            else:
                safe_print(f"❌ 消息缺少字段: {field}")
                return False
        
        # 检查元数据
        if last_message['metadata'] == metadata:
            safe_print("✅ 元数据保存正确")
        else:
            safe_print("❌ 元数据保存错误")
            return False
        
        # 检查时间戳格式
        try:
            datetime.datetime.fromisoformat(last_message['timestamp'])
            safe_print("✅ 时间戳格式正确")
        except ValueError:
            safe_print("❌ 时间戳格式错误")
            return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 消息元数据测试失败: {e}")
        return False

def test_history_limit():
    """测试历史记录长度限制"""
    safe_print("\n🔍 测试5: 历史记录长度限制")
    
    try:
        sys.path.insert(0, 'src')
        from main import ConversationHistory
        
        # 创建限制为5条的历史管理器
        history = ConversationHistory(max_history=5, sessions_dir='sessions')
        
        # 添加10条消息
        for i in range(10):
            history.add_message('user', f'测试消息 {i+1}')
        
        if len(history.history) == 5:
            safe_print("✅ 历史记录长度限制正常工作")
            
            # 检查是否保留了最新的5条
            last_message = history.history[-1]
            if '测试消息 10' in last_message['content']:
                safe_print("✅ 保留了最新的消息")
            else:
                safe_print("❌ 未正确保留最新消息")
                return False
        else:
            safe_print(f"❌ 历史记录长度限制失效，期望5条，实际{len(history.history)}条")
            return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 历史记录长度限制测试失败: {e}")
        return False

def test_config_integration():
    """测试配置集成"""
    safe_print("\n🔍 测试6: 配置集成")
    
    try:
        # 检查配置文件
        config_file = Path("config/config.json")
        if not config_file.exists():
            safe_print("❌ 配置文件不存在")
            return False
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查会话相关配置
        session_configs = ['max_history', 'auto_save_sessions']
        for key in session_configs:
            if key in config:
                safe_print(f"✅ 配置包含: {key} = {config[key]}")
            else:
                safe_print(f"❌ 配置缺少: {key}")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 配置集成测试失败: {e}")
        return False

def test_auto_save_functionality():
    """测试自动保存功能"""
    safe_print("\n🔍 测试7: 自动保存功能检查")
    
    try:
        # 检查主程序中的自动保存逻辑
        with open('src/main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'auto_save_sessions' in content:
            safe_print("✅ 主程序包含自动保存配置")
        else:
            safe_print("❌ 主程序缺少自动保存配置")
            return False
        
        if 'save_session()' in content:
            safe_print("✅ 主程序包含保存会话调用")
        else:
            safe_print("❌ 主程序缺少保存会话调用")
            return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 自动保存功能检查失败: {e}")
        return False

def test_session_file_format():
    """测试会话文件格式"""
    safe_print("\n🔍 测试8: 会话文件格式验证")
    
    try:
        sys.path.insert(0, 'src')
        from main import ConversationHistory
        
        history = ConversationHistory(sessions_dir='sessions')
        
        # 添加各种类型的消息
        test_messages = [
            ('user', '你好，我想学习Python'),
            ('assistant', '很高兴帮助你学习Python！'),
            ('user', '/examples'),
            ('assistant', '这里是一些Python示例代码...'),
        ]
        
        for role, content in test_messages:
            metadata = {'message_type': 'normal' if not content.startswith('/') else 'command'}
            history.add_message(role, content, metadata)
        
        # 保存并验证格式
        saved_file = history.save_session()
        
        if saved_file:
            with open(saved_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # 验证JSON格式正确性
            safe_print("✅ 会话文件JSON格式正确")
            
            # 验证必需字段
            required_fields = ['session_start', 'session_end', 'history']
            all_present = all(field in session_data for field in required_fields)
            
            if all_present:
                safe_print("✅ 会话文件包含所有必需字段")
            else:
                safe_print("❌ 会话文件缺少必需字段")
                return False
            
            # 验证历史记录格式
            for i, msg in enumerate(session_data['history']):
                msg_fields = ['role', 'content', 'timestamp', 'metadata']
                if all(field in msg for field in msg_fields):
                    safe_print(f"✅ 消息{i+1}格式正确")
                else:
                    safe_print(f"❌ 消息{i+1}格式错误")
                    return False
            
            # 清理测试文件
            os.remove(saved_file)
            safe_print("✅ 测试文件已清理")
            
            return True
        else:
            safe_print("❌ 会话文件保存失败")
            return False
        
    except Exception as e:
        safe_print(f"❌ 会话文件格式测试失败: {e}")
        return False

def main():
    """主测试函数"""
    safe_print("Python学习助手 - 会话保存和学习记录功能测试")
    safe_print("=" * 60)
    
    # 切换到正确的工作目录
    if not os.path.exists('src/main.py'):
        safe_print("❌ 请在python_learning_assistant目录下运行此测试")
        return
    
    tests = [
        ("会话目录检查", test_session_directory),
        ("基本对话历史功能", test_conversation_history_basic),
        ("消息元数据功能", test_message_metadata),
        ("历史记录长度限制", test_history_limit),
        ("配置集成", test_config_integration),
        ("自动保存功能检查", test_auto_save_functionality),
        ("会话文件格式验证", test_session_file_format),
    ]
    
    results = []
    history_obj = None
    
    for test_name, test_func in tests:
        safe_print(f"\n{'='*60}")
        if test_name == "基本对话历史功能":
            result = test_func()
            if isinstance(result, bool):
                results.append((test_name, result))
            else:
                # 这是ConversationHistory对象
                history_obj = result
                results.append((test_name, result is not None))
        elif test_name == "会话保存和加载" and history_obj:
            result = test_session_save_load(history_obj)
            results.append((test_name, result))
        else:
            result = test_func()
            results.append((test_name, result))
    
    # 如果有历史对象，测试保存加载
    if history_obj:
        safe_print(f"\n{'='*60}")
        result = test_session_save_load(history_obj)
        results.append(("会话保存和加载", result))
    
    # 显示测试结果
    safe_print(f"\n{'='*60}")
    safe_print("测试结果汇总:")
    safe_print("-" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        safe_print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    safe_print("-" * 60)
    safe_print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        safe_print("🎉 所有会话保存和学习记录功能正常工作！")
    else:
        safe_print("⚠️  部分功能存在问题，请检查失败的测试项目")
    
    safe_print("=" * 60)

if __name__ == "__main__":
    main()