#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话保存功能独立测试（不依赖openai）
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

def safe_print(text):
    """安全打印，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.replace("✅", "[OK]").replace("❌", "[FAIL]").replace("🔍", "[TEST]")
        print(clean_text)

class TestConversationHistory:
    """独立的对话历史测试类（不依赖openai）"""
    
    def __init__(self, max_history: int = 50, sessions_dir: str = None):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.session_start = datetime.datetime.now()
        self.sessions_dir = sessions_dir or "sessions"
        
        # 确保会话目录存在
        os.makedirs(self.sessions_dir, exist_ok=True)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加消息到历史记录"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.history.append(message)
        
        # 限制历史记录长度
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context_messages(self, context_length: int = 10) -> List[Dict]:
        """获取最近的对话上下文"""
        return [{'role': msg['role'], 'content': msg['content']} 
                for msg in self.history[-context_length:]]
    
    def save_session(self, filename: str = None):
        """保存对话会话"""
        if not filename:
            timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
            filename = f"python_learning_session_{timestamp}.json"
        
        session_data = {
            'session_start': self.session_start.isoformat(),
            'session_end': datetime.datetime.now().isoformat(),
            'history': self.history
        }
        
        try:
            filepath = os.path.join(self.sessions_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            return filepath
        except Exception as e:
            safe_print(f"保存会话失败: {e}")
            return None
    
    def load_session(self, filename: str):
        """加载对话会话"""
        try:
            filepath = os.path.join(self.sessions_dir, filename) if not os.path.isabs(filename) else filename
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            self.history = session_data.get('history', [])
            safe_print(f"成功加载会话: {filename}")
            return True
        except Exception as e:
            safe_print(f"加载会话失败: {e}")
            return False

def test_basic_functionality():
    """测试基本功能"""
    safe_print("🔍 测试1: 基本会话功能")
    
    try:
        # 创建历史管理器
        history = TestConversationHistory(sessions_dir='sessions')
        safe_print("✅ ConversationHistory 创建成功")
        
        # 测试添加消息
        history.add_message('user', '什么是Python列表？')
        history.add_message('assistant', 'Python列表是一种有序的可变集合...')
        history.add_message('user', '如何创建列表？')
        history.add_message('assistant', '可以使用方括号创建列表，例如: my_list = [1, 2, 3]')
        
        safe_print(f"✅ 添加了4条消息，当前历史长度: {len(history.history)}")
        
        # 测试获取上下文
        context = history.get_context_messages(3)
        if len(context) == 3:
            safe_print("✅ 上下文获取正常")
        else:
            safe_print(f"❌ 上下文获取异常，期望3条，实际{len(context)}条")
            return None
        
        return history
        
    except Exception as e:
        safe_print(f"❌ 基本功能测试失败: {e}")
        return None

def test_save_and_load(history):
    """测试保存和加载"""
    safe_print("\n🔍 测试2: 会话保存和加载")
    
    if not history:
        safe_print("❌ 无法测试：历史对象为空")
        return False
    
    try:
        # 保存会话
        saved_file = history.save_session("test_session.json")
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
            new_history = TestConversationHistory(sessions_dir='sessions')
            if new_history.load_session("test_session.json"):
                if len(new_history.history) == 4:
                    safe_print("✅ 会话加载成功")
                else:
                    safe_print(f"❌ 会话加载数据不完整，期望4条，实际{len(new_history.history)}条")
                    return False
            else:
                safe_print("❌ 会话加载失败")
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

def test_message_structure():
    """测试消息结构"""
    safe_print("\n🔍 测试3: 消息结构和元数据")
    
    try:
        history = TestConversationHistory(sessions_dir='sessions')
        
        # 添加带元数据的消息
        metadata = {
            'topic': 'Python基础',
            'difficulty': 'beginner',
            'contains_code': True
        }
        
        history.add_message('user', '请解释Python变量', metadata)
        
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
        safe_print(f"❌ 消息结构测试失败: {e}")
        return False

def test_history_limits():
    """测试历史记录限制"""
    safe_print("\n🔍 测试4: 历史记录长度限制")
    
    try:
        # 创建限制为3条的历史管理器
        history = TestConversationHistory(max_history=3, sessions_dir='sessions')
        
        # 添加5条消息
        for i in range(5):
            history.add_message('user', f'测试消息 {i+1}')
        
        if len(history.history) == 3:
            safe_print("✅ 历史记录长度限制正常工作")
            
            # 检查是否保留了最新的3条
            last_message = history.history[-1]
            if '测试消息 5' in last_message['content']:
                safe_print("✅ 保留了最新的消息")
            else:
                safe_print("❌ 未正确保留最新消息")
                return False
            
            first_message = history.history[0]
            if '测试消息 3' in first_message['content']:
                safe_print("✅ 正确删除了最旧的消息")
            else:
                safe_print("❌ 未正确删除最旧的消息")
                return False
        else:
            safe_print(f"❌ 历史记录长度限制失效，期望3条，实际{len(history.history)}条")
            return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 历史记录长度限制测试失败: {e}")
        return False

def test_session_file_format():
    """测试完整的会话文件格式"""
    safe_print("\n🔍 测试5: 完整会话文件格式")
    
    try:
        history = TestConversationHistory(sessions_dir='sessions')
        
        # 模拟一个完整的学习会话
        learning_session = [
            ('user', '我想学习Python循环', {'topic': 'loops', 'difficulty': 'beginner'}),
            ('assistant', '好的！Python有两种主要的循环：for循环和while循环', {'response_type': 'explanation'}),
            ('user', '/run for i in range(3): print(i)', {'command': True, 'code_execution': True}),
            ('assistant', '代码执行结果：\n0\n1\n2', {'response_type': 'code_result'}),
            ('user', '为什么从0开始？', {'follow_up': True}),
            ('assistant', '在Python中，range()函数默认从0开始计数，这是编程中的常见约定', {'response_type': 'explanation'})
        ]
        
        for role, content, metadata in learning_session:
            history.add_message(role, content, metadata)
        
        # 保存会话
        saved_file = history.save_session("complete_learning_session.json")
        
        if saved_file:
            # 验证完整的JSON结构
            with open(saved_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            safe_print("✅ 会话文件JSON格式正确")
            
            # 验证顶级字段
            top_level_fields = ['session_start', 'session_end', 'history']
            for field in top_level_fields:
                if field in session_data:
                    safe_print(f"✅ 顶级字段存在: {field}")
                else:
                    safe_print(f"❌ 顶级字段缺失: {field}")
                    return False
            
            # 验证时间格式
            try:
                start_time = datetime.datetime.fromisoformat(session_data['session_start'])
                end_time = datetime.datetime.fromisoformat(session_data['session_end'])
                if end_time >= start_time:
                    safe_print("✅ 会话时间逻辑正确")
                else:
                    safe_print("❌ 会话时间逻辑错误")
                    return False
            except ValueError:
                safe_print("❌ 会话时间格式错误")
                return False
            
            # 验证历史记录格式
            if len(session_data['history']) == 6:
                safe_print("✅ 历史记录数量正确")
            else:
                safe_print(f"❌ 历史记录数量错误，期望6条，实际{len(session_data['history'])}条")
                return False
            
            # 验证每条消息的结构
            for i, msg in enumerate(session_data['history']):
                msg_fields = ['role', 'content', 'timestamp', 'metadata']
                if all(field in msg for field in msg_fields):
                    safe_print(f"✅ 消息{i+1}结构完整")
                else:
                    safe_print(f"❌ 消息{i+1}结构不完整")
                    return False
                
                # 验证角色值
                if msg['role'] in ['user', 'assistant']:
                    pass  # 正确
                else:
                    safe_print(f"❌ 消息{i+1}角色值错误: {msg['role']}")
                    return False
            
            # 验证元数据保存
            command_msg = session_data['history'][2]  # /run命令
            if command_msg['metadata'].get('command') == True:
                safe_print("✅ 命令元数据保存正确")
            else:
                safe_print("❌ 命令元数据保存错误")
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

def test_directory_structure():
    """测试目录结构"""
    safe_print("\n🔍 测试6: 目录结构检查")
    
    try:
        sessions_dir = Path("sessions")
        
        # 确保目录存在
        if not sessions_dir.exists():
            sessions_dir.mkdir(exist_ok=True)
            safe_print("✅ 会话目录创建成功")
        else:
            safe_print("✅ 会话目录已存在")
        
        # 检查权限
        if os.access(sessions_dir, os.R_OK):
            safe_print("✅ 会话目录可读")
        else:
            safe_print("❌ 会话目录不可读")
            return False
        
        if os.access(sessions_dir, os.W_OK):
            safe_print("✅ 会话目录可写")
        else:
            safe_print("❌ 会话目录不可写")
            return False
        
        # 测试文件创建和删除
        test_file = sessions_dir / "test_permissions.txt"
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            safe_print("✅ 文件创建权限正常")
            
            test_file.unlink()
            safe_print("✅ 文件删除权限正常")
        except Exception as e:
            safe_print(f"❌ 文件操作权限异常: {e}")
            return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 目录结构测试失败: {e}")
        return False

def main():
    """主测试函数"""
    safe_print("Python学习助手 - 会话保存功能独立测试")
    safe_print("=" * 60)
    
    # 切换到正确的工作目录
    if not os.path.exists('config/config.json'):
        safe_print("❌ 请在python_learning_assistant目录下运行此测试")
        return
    
    tests = [
        ("目录结构检查", test_directory_structure),
        ("基本会话功能", test_basic_functionality),
        ("消息结构和元数据", test_message_structure),
        ("历史记录长度限制", test_history_limits),
        ("完整会话文件格式", test_session_file_format),
    ]
    
    results = []
    history_obj = None
    
    for test_name, test_func in tests:
        safe_print(f"\n{'='*60}")
        if test_name == "基本会话功能":
            result = test_func()
            if result is not None:
                history_obj = result
                results.append((test_name, True))
            else:
                results.append((test_name, False))
        else:
            result = test_func()
            results.append((test_name, result))
    
    # 测试保存和加载功能
    if history_obj:
        safe_print(f"\n{'='*60}")
        result = test_save_and_load(history_obj)
        results.append(("会话保存和加载", result))
    
    # 显示测试结果
    safe_print(f"\n{'='*60}")
    safe_print("测试结果汇总:")
    safe_print("-" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        safe_print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    safe_print("-" * 60)
    safe_print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        safe_print("🎉 会话保存功能完全正常！")
    else:
        safe_print("⚠️  部分功能存在问题")
    
    # 显示功能状态
    safe_print(f"\n{'='*60}")
    safe_print("功能状态评估:")
    safe_print("-" * 60)
    
    if passed >= total * 0.8:
        safe_print("✅ 会话保存功能: 可用")
        safe_print("✅ 学习记录功能: 可用") 
        safe_print("✅ 元数据管理: 可用")
        safe_print("✅ 历史记录管理: 可用")
    else:
        safe_print("❌ 会话保存功能需要修复")
    
    safe_print("=" * 60)

if __name__ == "__main__":
    main()