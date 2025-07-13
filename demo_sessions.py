#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建会话保存功能演示
"""

import os
import sys
import json
import datetime
from pathlib import Path

def create_sample_session():
    """创建示例会话文件"""
    
    # 确保sessions目录存在
    sessions_dir = Path("sessions")
    sessions_dir.mkdir(exist_ok=True)
    
    # 创建示例会话数据
    session_data = {
        "session_start": "2024-01-15T10:30:00.123456",
        "session_end": "2024-01-15T11:15:30.654321", 
        "history": [
            {
                "role": "user",
                "content": "你好，我想学习Python",
                "timestamp": "2024-01-15T10:30:05.123456",
                "metadata": {
                    "session_type": "learning",
                    "topic": "introduction"
                }
            },
            {
                "role": "assistant", 
                "content": "你好！很高兴帮助你学习Python。Python是一门非常适合初学者的编程语言。我们可以从基础语法开始学习。",
                "timestamp": "2024-01-15T10:30:08.234567",
                "metadata": {
                    "response_type": "greeting",
                    "contains_suggestion": True
                }
            },
            {
                "role": "user",
                "content": "什么是Python变量？",
                "timestamp": "2024-01-15T10:32:15.345678", 
                "metadata": {
                    "topic": "variables",
                    "difficulty": "beginner"
                }
            },
            {
                "role": "assistant",
                "content": "Python变量是用来存储数据的容器。你可以把变量想象成一个盒子，里面可以放不同类型的东西：\n\n```python\nname = \"小明\"  # 字符串变量\nage = 18      # 整数变量\nheight = 1.75 # 浮点数变量\nis_student = True  # 布尔变量\n```\n\n变量的特点：\n1. 不需要声明类型\n2. 可以随时改变值\n3. 名称要有意义",
                "timestamp": "2024-01-15T10:32:18.456789",
                "metadata": {
                    "response_type": "explanation",
                    "contains_code": True,
                    "topic": "variables"
                }
            },
            {
                "role": "user", 
                "content": "/run name = '张三'; print(f'你好，{name}！')",
                "timestamp": "2024-01-15T10:35:20.567890",
                "metadata": {
                    "command": True,
                    "code_execution": True,
                    "topic": "variables"
                }
            },
            {
                "role": "assistant",
                "content": "🚀 执行代码:\n┌──────────────────────────────────────────────────┐\n│ name = '张三'; print(f'你好，{name}！')\n└──────────────────────────────────────────────────┘\n\n📤 输出结果:\n你好，张三！",
                "timestamp": "2024-01-15T10:35:22.678901",
                "metadata": {
                    "response_type": "code_result",
                    "execution_successful": True
                }
            },
            {
                "role": "user",
                "content": "太棒了！能给我更多关于字符串的例子吗？", 
                "timestamp": "2024-01-15T10:37:45.789012",
                "metadata": {
                    "follow_up": True,
                    "topic": "strings",
                    "enthusiasm": "high"
                }
            },
            {
                "role": "assistant",
                "content": "当然可以！字符串是Python中非常重要的数据类型。这里有一些常用的字符串操作：\n\n```python\n# 字符串连接\nfirst_name = \"张\"\nlast_name = \"三\"\nfull_name = first_name + last_name\nprint(full_name)  # 输出：张三\n\n# 字符串格式化\nage = 25\nmessage = f\"我叫{full_name}，今年{age}岁\"\nprint(message)\n\n# 字符串方法\ntext = \"Hello World\"\nprint(text.upper())     # 转大写：HELLO WORLD\nprint(text.lower())     # 转小写：hello world\nprint(text.replace(\"World\", \"Python\"))  # 替换：Hello Python\n```\n\n你想试试运行这些例子吗？",
                "timestamp": "2024-01-15T10:37:50.890123",
                "metadata": {
                    "response_type": "explanation",
                    "contains_code": True,
                    "topic": "strings",
                    "includes_question": True
                }
            },
            {
                "role": "user",
                "content": "/save",
                "timestamp": "2024-01-15T11:15:25.901234",
                "metadata": {
                    "command": True,
                    "session_action": "save"
                }
            },
            {
                "role": "assistant",
                "content": "✅ 会话已保存到: sessions/python_learning_session_20240115_103000.json\n\n📊 本次学习总结：\n• 学习时长：45分钟\n• 涉及主题：Python入门、变量、字符串\n• 代码执行：1次\n• 互动次数：9次\n\n继续加油学习！👍",
                "timestamp": "2024-01-15T11:15:30.012345", 
                "metadata": {
                    "response_type": "session_summary",
                    "session_stats": {
                        "duration_minutes": 45,
                        "topics_covered": ["introduction", "variables", "strings"],
                        "code_executions": 1,
                        "interactions": 9
                    }
                }
            }
        ]
    }
    
    # 保存示例会话
    sample_file = sessions_dir / "sample_learning_session.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    print(f"示例会话文件已创建: {sample_file}")
    return sample_file

def analyze_session_file(filepath):
    """分析会话文件内容"""
    print(f"\n=== 会话文件分析: {filepath} ===")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        session_data = json.load(f)
    
    # 基本信息
    start_time = datetime.datetime.fromisoformat(session_data['session_start'])
    end_time = datetime.datetime.fromisoformat(session_data['session_end'])
    duration = end_time - start_time
    
    print(f"会话开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"会话结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"会话持续时间: {duration}")
    print(f"消息总数: {len(session_data['history'])}")
    
    # 分析消息类型
    user_messages = 0
    assistant_messages = 0
    commands = 0
    code_executions = 0
    topics = set()
    
    for msg in session_data['history']:
        if msg['role'] == 'user':
            user_messages += 1
            if msg.get('metadata', {}).get('command'):
                commands += 1
            if msg.get('metadata', {}).get('code_execution'):
                code_executions += 1
        else:
            assistant_messages += 1
        
        # 收集主题
        topic = msg.get('metadata', {}).get('topic')
        if topic:
            topics.add(topic)
    
    print(f"\n消息统计:")
    print(f"  用户消息: {user_messages}")
    print(f"  助手回复: {assistant_messages}")
    print(f"  命令执行: {commands}")
    print(f"  代码运行: {code_executions}")
    
    print(f"\n学习主题:")
    for topic in sorted(topics):
        print(f"  • {topic}")
    
    # 分析学习进度
    print(f"\n学习特征分析:")
    
    # 代码相关消息
    code_related = sum(1 for msg in session_data['history'] 
                      if msg.get('metadata', {}).get('contains_code'))
    print(f"  包含代码的消息: {code_related}")
    
    # 跟进问题
    follow_ups = sum(1 for msg in session_data['history'] 
                    if msg.get('metadata', {}).get('follow_up'))
    print(f"  跟进问题: {follow_ups}")
    
    # 难度分布
    difficulties = [msg.get('metadata', {}).get('difficulty') 
                   for msg in session_data['history'] 
                   if msg.get('metadata', {}).get('difficulty')]
    if difficulties:
        print(f"  难度级别: {set(difficulties)}")

def main():
    """主函数"""
    print("Python学习助手 - 会话保存功能演示")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('config/config.json'):
        print("请在python_learning_assistant目录下运行此脚本")
        return
    
    # 创建示例会话
    sample_file = create_sample_session()
    
    # 分析会话文件
    analyze_session_file(sample_file)
    
    print(f"\n=" * 50)
    print("会话保存功能演示完成！")
    print(f"示例文件位置: {sample_file}")
    print("您可以查看该文件了解会话数据的完整结构。")

if __name__ == "__main__":
    main()