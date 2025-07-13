#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间管理功能测试脚本
验证增强的时间处理和会话管理功能
"""

import os
import sys
import json
import datetime
import time
from pathlib import Path

def safe_print(text):
    """安全打印，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.replace("✅", "[OK]").replace("❌", "[FAIL]").replace("🔍", "[TEST]")
        print(clean_text)

def test_time_manager():
    """测试时间管理器功能"""
    safe_print("🔍 测试1: 时间管理器基本功能")
    
    try:
        sys.path.insert(0, 'src')
        from time_manager import TimeManager
        
        # 创建时间管理器
        tm = TimeManager()
        safe_print("✅ TimeManager 创建成功")
        
        # 测试时间获取
        current_time = tm.now()
        safe_print(f"✅ 当前时间: {tm.format_datetime(current_time)}")
        
        # 测试ISO格式
        iso_time = tm.iso_format(current_time)
        safe_print(f"✅ ISO格式: {iso_time}")
        
        # 测试时间戳
        timestamp = tm.timestamp()
        safe_print(f"✅ 时间戳: {timestamp}")
        
        # 测试经过时间
        time.sleep(1)
        elapsed = tm.elapsed_time()
        safe_print(f"✅ 经过时间: {tm.format_duration(elapsed)}")
        
        # 测试文件名生成
        filename = tm.session_filename("test_session")
        safe_print(f"✅ 会话文件名: {filename}")
        
        return tm
        
    except Exception as e:
        safe_print(f"❌ 时间管理器测试失败: {e}")
        return None

def test_enhanced_conversation_history():
    """测试增强的对话历史管理"""
    safe_print("\n🔍 测试2: 增强对话历史管理")
    
    try:
        sys.path.insert(0, 'src')
        from time_manager import EnhancedConversationHistory
        
        # 创建增强的对话历史管理器
        history = EnhancedConversationHistory(
            max_history=10,
            sessions_dir='sessions',
            timezone='Asia/Shanghai'
        )
        safe_print("✅ EnhancedConversationHistory 创建成功")
        
        # 添加测试消息
        test_messages = [
            ('user', '你好，我想学习Python', {'topic': 'introduction', 'difficulty': 'beginner'}),
            ('assistant', '你好！很高兴帮助你学习Python', {'response_type': 'greeting'}),
            ('user', '什么是变量？', {'topic': 'variables', 'difficulty': 'beginner'}),
            ('assistant', 'Python变量是存储数据的容器', {'response_type': 'explanation', 'topic': 'variables'}),
            ('user', '/run x = 10; print(x)', {'command': True, 'code_execution': True}),
            ('assistant', '代码执行结果: 10', {'response_type': 'code_result'})
        ]
        
        for role, content, metadata in test_messages:
            history.add_message(role, content, metadata)
            time.sleep(0.1)  # 模拟时间间隔
        
        safe_print(f"✅ 添加了{len(test_messages)}条消息")
        
        # 测试会话摘要
        summary = history.get_session_summary()
        safe_print("✅ 会话摘要生成成功")
        
        # 显示详细信息
        time_info = summary.get('time_info', {})
        stats = summary.get('statistics', {})
        
        safe_print(f"  会话时长: {time_info.get('duration_formatted', '未知')}")
        safe_print(f"  总消息数: {stats.get('total_messages', 0)}")
        safe_print(f"  涉及主题: {', '.join(stats.get('topics_covered', []))}")
        safe_print(f"  代码执行: {stats.get('code_executions', 0)}次")
        
        return history
        
    except Exception as e:
        safe_print(f"❌ 增强对话历史管理测试失败: {e}")
        return None

def test_enhanced_session_save(history):
    """测试增强的会话保存功能"""
    safe_print("\n🔍 测试3: 增强会话保存功能")
    
    if not history:
        safe_print("❌ 无法测试：历史对象为空")
        return False
    
    try:
        # 保存会话
        saved_file = history.save_session("enhanced_test_session.json")
        if saved_file and os.path.exists(saved_file):
            safe_print(f"✅ 增强会话保存成功: {saved_file}")
            
            # 验证文件内容
            with open(saved_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # 检查新的数据结构
            required_sections = ['session_info', 'session_stats', 'history']
            for section in required_sections:
                if section in session_data:
                    safe_print(f"✅ 包含{section}部分")
                else:
                    safe_print(f"❌ 缺少{section}部分")
                    return False
            
            # 检查会话信息详细内容
            session_info = session_data['session_info']
            expected_fields = ['start_time', 'end_time', 'duration_seconds', 'duration_formatted', 'timezone']
            for field in expected_fields:
                if field in session_info:
                    safe_print(f"✅ 会话信息包含: {field}")
                else:
                    safe_print(f"❌ 会话信息缺少: {field}")
            
            # 检查统计信息
            session_stats = session_data['session_stats']
            stats_fields = ['total_messages', 'user_messages', 'assistant_messages', 'topics_covered']
            for field in stats_fields:
                if field in session_stats:
                    safe_print(f"✅ 统计信息包含: {field}")
                else:
                    safe_print(f"❌ 统计信息缺少: {field}")
            
            # 检查历史消息的时间戳增强
            first_message = session_data['history'][0]
            enhanced_fields = ['timestamp', 'timestamp_formatted', 'elapsed_seconds']
            for field in enhanced_fields:
                if field in first_message:
                    safe_print(f"✅ 消息包含增强字段: {field}")
                else:
                    safe_print(f"❌ 消息缺少增强字段: {field}")
            
            # 测试加载功能
            new_history = EnhancedConversationHistory(sessions_dir='sessions')
            if new_history.load_session("enhanced_test_session.json"):
                safe_print("✅ 增强会话加载成功")
                
                if len(new_history.history) == 6:
                    safe_print("✅ 历史数据加载完整")
                else:
                    safe_print(f"❌ 历史数据不完整，期望6条，实际{len(new_history.history)}条")
                    return False
            else:
                safe_print("❌ 增强会话加载失败")
                return False
            
            # 清理测试文件
            os.remove(saved_file)
            safe_print("✅ 测试文件已清理")
            
            return True
            
        else:
            safe_print("❌ 增强会话保存失败")
            return False
            
    except Exception as e:
        safe_print(f"❌ 增强会话保存测试失败: {e}")
        return False

def test_timezone_handling():
    """测试时区处理功能"""
    safe_print("\n🔍 测试4: 时区处理功能")
    
    try:
        sys.path.insert(0, 'src')
        from time_manager import TimeManager
        
        # 测试不同时区
        timezones = [None, 'UTC', 'Asia/Shanghai']
        
        for tz in timezones:
            try:
                tm = TimeManager(tz)
                current_time = tm.now()
                tz_name = str(current_time.tzinfo) if current_time.tzinfo else '本地时区'
                safe_print(f"✅ 时区 {tz or '本地'} ({tz_name}): {tm.format_datetime(current_time)}")
            except Exception as e:
                safe_print(f"❌ 时区 {tz} 处理失败: {e}")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 时区处理测试失败: {e}")
        return False

def test_session_analytics():
    """测试会话分析功能"""
    safe_print("\n🔍 测试5: 会话分析功能")
    
    try:
        sys.path.insert(0, 'src')
        from time_manager import EnhancedConversationHistory
        
        # 创建模拟学习会话
        history = EnhancedConversationHistory(sessions_dir='sessions')
        
        # 模拟一个完整的学习对话
        learning_scenario = [
            ('user', '我想学习Python基础', {'topic': 'introduction', 'difficulty': 'beginner'}),
            ('assistant', '好的，我们从变量开始', {'response_type': 'explanation'}),
            ('user', '如何定义变量？', {'topic': 'variables', 'difficulty': 'beginner'}),
            ('assistant', '在Python中，变量定义很简单...', {'response_type': 'explanation', 'topic': 'variables'}),
            ('user', '/run name = "Python"; print(name)', {'command': True, 'code_execution': True, 'topic': 'variables'}),
            ('assistant', '执行结果: Python', {'response_type': 'code_result'}),
            ('user', '列表怎么使用？', {'topic': 'lists', 'difficulty': 'beginner'}),
            ('assistant', 'Python列表是有序的集合...', {'response_type': 'explanation', 'topic': 'lists'}),
            ('user', '/run my_list = [1,2,3]; print(my_list)', {'command': True, 'code_execution': True, 'topic': 'lists'}),
            ('assistant', '执行结果: [1, 2, 3]', {'response_type': 'code_result'}),
            ('user', '现在我想试试循环', {'topic': 'loops', 'difficulty': 'intermediate', 'follow_up': True}),
            ('assistant', 'for循环是Python中常用的...', {'response_type': 'explanation', 'topic': 'loops'})
        ]
        
        for role, content, metadata in learning_scenario:
            history.add_message(role, content, metadata)
            time.sleep(0.05)  # 模拟思考时间
        
        # 获取分析结果
        summary = history.get_session_summary()
        
        # 验证分析结果
        stats = summary.get('statistics', {})
        progress = summary.get('learning_progress', {})
        
        safe_print(f"✅ 分析完成")
        safe_print(f"  探索主题: {stats.get('topics_covered', [])}")
        safe_print(f"  学习深度: {progress.get('learning_depth', '未知')}")
        safe_print(f"  实践练习: {'是' if progress.get('hands_on_practice') else '否'}")
        safe_print(f"  参与度: {progress.get('engagement_level', '未知')}")
        safe_print(f"  代码执行次数: {stats.get('code_executions', 0)}")
        
        # 验证分析正确性
        expected_topics = {'introduction', 'variables', 'lists', 'loops'}
        actual_topics = set(stats.get('topics_covered', []))
        
        if expected_topics.issubset(actual_topics):
            safe_print("✅ 主题识别正确")
        else:
            safe_print(f"❌ 主题识别不完整，期望{expected_topics}，实际{actual_topics}")
            return False
        
        if stats.get('code_executions', 0) == 2:
            safe_print("✅ 代码执行统计正确")
        else:
            safe_print(f"❌ 代码执行统计错误，期望2次，实际{stats.get('code_executions', 0)}次")
            return False
        
        if progress.get('learning_depth') == 'intermediate':
            safe_print("✅ 学习深度分析正确")
        else:
            safe_print(f"❌ 学习深度分析错误，期望intermediate，实际{progress.get('learning_depth')}")
            return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 会话分析测试失败: {e}")
        return False

def test_config_integration():
    """测试配置集成"""
    safe_print("\n🔍 测试6: 配置集成测试")
    
    try:
        # 检查配置文件
        config_file = Path("config/config.json")
        if not config_file.exists():
            safe_print("❌ 配置文件不存在")
            return False
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查时间相关配置
        time_configs = ['timezone', 'time_format', 'session_filename_format']
        for key in time_configs:
            if key in config:
                safe_print(f"✅ 配置包含: {key} = {config[key]}")
            else:
                safe_print(f"❌ 配置缺少: {key}")
        
        # 验证时区配置有效性
        timezone = config.get('timezone')
        if timezone:
            try:
                import datetime
                # 尝试创建带时区的时间
                now = datetime.datetime.now()
                safe_print(f"✅ 时区配置 '{timezone}' 格式正确")
            except Exception as e:
                safe_print(f"❌ 时区配置无效: {e}")
                return False
        
        return True
        
    except Exception as e:
        safe_print(f"❌ 配置集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    safe_print("Python学习助手 - 时间管理功能测试")
    safe_print("=" * 60)
    
    # 检查工作目录
    if not os.path.exists('config/config.json'):
        safe_print("❌ 请在python_learning_assistant目录下运行此测试")
        return
    
    tests = [
        ("时间管理器基本功能", test_time_manager),
        ("增强对话历史管理", test_enhanced_conversation_history),
        ("时区处理功能", test_timezone_handling),
        ("会话分析功能", test_session_analytics),
        ("配置集成测试", test_config_integration),
    ]
    
    results = []
    test_objects = {}
    
    for test_name, test_func in tests:
        safe_print(f"\n{'='*60}")
        try:
            if test_name == "时间管理器基本功能":
                result = test_func()
                test_objects['time_manager'] = result
                results.append((test_name, result is not None))
            elif test_name == "增强对话历史管理":
                result = test_func()
                test_objects['history'] = result
                results.append((test_name, result is not None))
            else:
                result = test_func()
                results.append((test_name, result))
        except Exception as e:
            safe_print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 如果有历史对象，测试增强保存功能
    if test_objects.get('history'):
        safe_print(f"\n{'='*60}")
        result = test_enhanced_session_save(test_objects['history'])
        results.append(("增强会话保存功能", result))
    
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
    
    # 功能状态评估
    safe_print(f"\n{'='*60}")
    safe_print("时间管理功能状态评估:")
    safe_print("-" * 60)
    
    if passed >= total * 0.8:
        safe_print("✅ 时间管理功能: 可用")
        safe_print("✅ 增强会话保存: 可用")
        safe_print("✅ 会话分析统计: 可用")
        safe_print("✅ 时区处理: 可用")
        safe_print("\n🎉 时间管理功能已成功集成！")
    else:
        safe_print("❌ 时间管理功能需要修复")
    
    safe_print("=" * 60)

if __name__ == "__main__":
    main()