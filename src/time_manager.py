#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间管理增强模块
提供准确的时间获取、格式化和时区处理功能
仅使用Python标准库，不依赖pytz
"""

import datetime
import time
from typing import Optional, Union, Dict, List
import json
import os

class TimeManager:
    """时间管理器 - 提供统一的时间处理功能（仅使用标准库）"""
    
    def __init__(self, timezone: str = None):
        """
        初始化时间管理器
        
        Args:
            timezone: 时区名称，支持 'UTC' 或 None（本地时区）
                     由于不依赖pytz，仅支持基本时区
        """
        self.timezone = self._get_timezone(timezone)
        self.start_time = self.now()
    
    def _get_timezone(self, timezone_name: Optional[str]) -> datetime.timezone:
        """获取时区对象（仅使用标准库）"""
        if timezone_name is None:
            # 使用系统本地时区
            return datetime.datetime.now().astimezone().tzinfo
        elif timezone_name.upper() == 'UTC':
            return datetime.timezone.utc
        elif timezone_name in ['Asia/Shanghai', 'Asia/Beijing']:
            # 手动定义中国时区 UTC+8
            return datetime.timezone(datetime.timedelta(hours=8))
        elif timezone_name == 'US/Eastern':
            # 手动定义美东时区 UTC-5 (不考虑夏令时)
            return datetime.timezone(datetime.timedelta(hours=-5))
        elif timezone_name == 'Europe/London':
            # 手动定义英国时区 UTC+0
            return datetime.timezone.utc
        else:
            # 如果时区名称不支持，使用本地时区
            return datetime.datetime.now().astimezone().tzinfo
    
    def now(self) -> datetime.datetime:
        """获取当前时间（带时区信息）"""
        return datetime.datetime.now(self.timezone)
    
    def utc_now(self) -> datetime.datetime:
        """获取当前UTC时间"""
        return datetime.datetime.now(datetime.timezone.utc)
    
    def timestamp(self) -> float:
        """获取当前时间戳"""
        return time.time()
    
    def format_datetime(self, dt: Optional[datetime.datetime] = None, 
                       format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        格式化日期时间
        
        Args:
            dt: 要格式化的datetime对象，如果为None则使用当前时间
            format_str: 格式字符串
            
        Returns:
            格式化后的时间字符串
        """
        if dt is None:
            dt = self.now()
        return dt.strftime(format_str)
    
    def iso_format(self, dt: Optional[datetime.datetime] = None, 
                   include_microseconds: bool = True) -> str:
        """
        返回ISO格式的时间字符串
        
        Args:
            dt: 要格式化的datetime对象，如果为None则使用当前时间
            include_microseconds: 是否包含微秒
            
        Returns:
            ISO格式的时间字符串
        """
        if dt is None:
            dt = self.now()
        
        if include_microseconds:
            return dt.isoformat()
        else:
            # 移除微秒部分
            dt_no_micro = dt.replace(microsecond=0)
            return dt_no_micro.isoformat()
    
    def parse_iso(self, iso_string: str) -> datetime.datetime:
        """
        解析ISO格式的时间字符串
        
        Args:
            iso_string: ISO格式的时间字符串
            
        Returns:
            datetime对象
        """
        try:
            return datetime.datetime.fromisoformat(iso_string)
        except ValueError as e:
            raise ValueError(f"无法解析时间字符串 '{iso_string}': {e}")
    
    def elapsed_time(self, start_time: Optional[datetime.datetime] = None) -> datetime.timedelta:
        """
        计算经过的时间
        
        Args:
            start_time: 起始时间，如果为None则使用创建TimeManager时的时间
            
        Returns:
            时间差
        """
        if start_time is None:
            start_time = self.start_time
        return self.now() - start_time
    
    def elapsed_seconds(self, start_time: Optional[datetime.datetime] = None) -> float:
        """
        计算经过的秒数
        
        Args:
            start_time: 起始时间，如果为None则使用创建TimeManager时的时间
            
        Returns:
            经过的秒数
        """
        return self.elapsed_time(start_time).total_seconds()
    
    def format_duration(self, duration: Union[datetime.timedelta, float]) -> str:
        """
        格式化时间长度为可读字符串
        
        Args:
            duration: 时间长度（timedelta对象或秒数）
            
        Returns:
            格式化的时间长度字符串
        """
        if isinstance(duration, (int, float)):
            duration = datetime.timedelta(seconds=duration)
        
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}小时{minutes}分钟{seconds}秒"
        elif minutes > 0:
            return f"{minutes}分钟{seconds}秒"
        else:
            return f"{seconds}秒"
    
    def session_filename(self, prefix: str = "session", extension: str = "json") -> str:
        """
        生成基于时间的会话文件名
        
        Args:
            prefix: 文件名前缀
            extension: 文件扩展名
            
        Returns:
            文件名
        """
        timestamp = self.format_datetime(format_str="%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    def add_timezone_info(self, dt: datetime.datetime) -> datetime.datetime:
        """
        为无时区信息的datetime对象添加时区信息
        
        Args:
            dt: datetime对象
            
        Returns:
            带时区信息的datetime对象
        """
        if dt.tzinfo is None:
            return dt.replace(tzinfo=self.timezone)
        return dt
    
    def to_local_time(self, dt: datetime.datetime) -> datetime.datetime:
        """
        将datetime对象转换为本地时间
        
        Args:
            dt: datetime对象
            
        Returns:
            本地时间的datetime对象
        """
        if dt.tzinfo is None:
            # 假设是UTC时间
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        
        return dt.astimezone(self.timezone)
    
    def session_summary(self, start_time: Optional[datetime.datetime] = None) -> dict:
        """
        生成会话时间摘要
        
        Args:
            start_time: 会话开始时间，如果为None则使用创建TimeManager时的时间
            
        Returns:
            包含时间信息的字典
        """
        if start_time is None:
            start_time = self.start_time
        
        end_time = self.now()
        duration = end_time - start_time
        
        return {
            'start_time': self.iso_format(start_time),
            'end_time': self.iso_format(end_time),
            'duration_seconds': duration.total_seconds(),
            'duration_formatted': self.format_duration(duration),
            'timezone': str(self.timezone)
        }


class EnhancedConversationHistory:
    """增强的对话历史管理类 - 集成了高级时间管理"""
    
    def __init__(self, max_history: int = 50, sessions_dir: str = None, 
                 timezone: str = None):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.time_manager = TimeManager(timezone)
        self.session_start_time = self.time_manager.now()
        self.sessions_dir = sessions_dir or os.path.join(os.path.dirname(__file__), '..', 'sessions')
        
        # 确保会话目录存在
        os.makedirs(self.sessions_dir, exist_ok=True)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加消息到历史记录（增强时间处理）"""
        current_time = self.time_manager.now()
        
        message = {
            'role': role,
            'content': content,
            'timestamp': self.time_manager.iso_format(current_time),
            'timestamp_formatted': self.time_manager.format_datetime(current_time),
            'elapsed_seconds': self.time_manager.elapsed_seconds(self.session_start_time),
            'metadata': metadata or {}
        }
        
        # 添加时间相关的元数据
        if metadata is None:
            metadata = {}
        
        metadata.update({
            'session_elapsed': self.time_manager.format_duration(
                self.time_manager.elapsed_time(self.session_start_time)
            ),
            'message_time': self.time_manager.format_datetime(current_time, "%H:%M:%S")
        })
        
        message['metadata'] = metadata
        self.history.append(message)
        
        # 限制历史记录长度
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context_messages(self, context_length: int = 10) -> List[Dict]:
        """获取最近的对话上下文"""
        return [{'role': msg['role'], 'content': msg['content']} 
                for msg in self.history[-context_length:]]
    
    def save_session(self, filename: str = None) -> Optional[str]:
        """保存对话会话（增强时间信息）"""
        if not filename:
            filename = self.time_manager.session_filename("python_learning_session")
        
        # 生成详细的会话时间摘要
        time_summary = self.time_manager.session_summary(self.session_start_time)
        
        # 计算会话统计信息
        session_stats = self._calculate_session_stats()
        
        session_data = {
            'session_info': {
                'start_time': time_summary['start_time'],
                'end_time': time_summary['end_time'],
                'duration_seconds': time_summary['duration_seconds'],
                'duration_formatted': time_summary['duration_formatted'],
                'timezone': time_summary['timezone'],
                'created_by': 'Python学习助手 v1.0.0',
                'format_version': '1.0'
            },
            'session_stats': session_stats,
            'history': self.history
        }
        
        try:
            filepath = os.path.join(self.sessions_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            return filepath
        except Exception as e:
            print(f"保存会话失败: {e}")
            return None
    
    def load_session(self, filename: str) -> bool:
        """加载对话会话（增强时间处理）"""
        try:
            filepath = os.path.join(self.sessions_dir, filename) if not os.path.isabs(filename) else filename
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # 加载历史记录
            self.history = session_data.get('history', [])
            
            # 恢复会话开始时间
            if 'session_info' in session_data:
                start_time_str = session_data['session_info'].get('start_time')
                if start_time_str:
                    self.session_start_time = self.time_manager.parse_iso(start_time_str)
            
            print(f"成功加载会话: {filename}")
            
            # 显示会话信息
            if 'session_info' in session_data:
                info = session_data['session_info']
                print(f"  会话时长: {info.get('duration_formatted', '未知')}")
                print(f"  消息数量: {len(self.history)}")
            
            return True
        except Exception as e:
            print(f"加载会话失败: {e}")
            return False
    
    def _calculate_session_stats(self) -> Dict:
        """计算会话统计信息"""
        user_messages = 0
        assistant_messages = 0
        commands = 0
        code_executions = 0
        topics = set()
        difficulties = []
        
        for msg in self.history:
            if msg['role'] == 'user':
                user_messages += 1
                metadata = msg.get('metadata', {})
                if metadata.get('command'):
                    commands += 1
                if metadata.get('code_execution'):
                    code_executions += 1
            else:
                assistant_messages += 1
            
            # 收集主题和难度
            metadata = msg.get('metadata', {})
            topic = metadata.get('topic')
            if topic:
                topics.add(topic)
            
            difficulty = metadata.get('difficulty')
            if difficulty:
                difficulties.append(difficulty)
        
        return {
            'total_messages': len(self.history),
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'commands_executed': commands,
            'code_executions': code_executions,
            'topics_covered': list(topics),
            'difficulty_distribution': {
                level: difficulties.count(level) 
                for level in set(difficulties)
            } if difficulties else {},
            'average_response_time': self._calculate_average_response_time()
        }
    
    def _calculate_average_response_time(self) -> Optional[float]:
        """计算平均响应时间"""
        response_times = []
        
        for i in range(1, len(self.history)):
            prev_msg = self.history[i-1]
            curr_msg = self.history[i]
            
            # 如果是用户消息后跟助手消息
            if prev_msg['role'] == 'user' and curr_msg['role'] == 'assistant':
                try:
                    prev_time = self.time_manager.parse_iso(prev_msg['timestamp'])
                    curr_time = self.time_manager.parse_iso(curr_msg['timestamp'])
                    response_time = (curr_time - prev_time).total_seconds()
                    response_times.append(response_time)
                except:
                    continue
        
        if response_times:
            return sum(response_times) / len(response_times)
        return None
    
    def get_session_summary(self) -> Dict:
        """获取会话摘要"""
        time_summary = self.time_manager.session_summary(self.session_start_time)
        session_stats = self._calculate_session_stats()
        
        return {
            'time_info': time_summary,
            'statistics': session_stats,
            'learning_progress': self._analyze_learning_progress()
        }
    
    def _analyze_learning_progress(self) -> Dict:
        """分析学习进度"""
        if not self.history:
            return {'status': 'no_activity'}
        
        topics = set()
        difficulties = []
        has_code_practice = False
        
        for msg in self.history:
            metadata = msg.get('metadata', {})
            
            topic = metadata.get('topic')
            if topic:
                topics.add(topic)
            
            difficulty = metadata.get('difficulty')
            if difficulty:
                difficulties.append(difficulty)
            
            if metadata.get('code_execution'):
                has_code_practice = True
        
        # 分析学习深度
        if 'advanced' in difficulties:
            depth = 'advanced'
        elif 'intermediate' in difficulties:
            depth = 'intermediate'
        elif 'beginner' in difficulties:
            depth = 'beginner'
        else:
            depth = 'unknown'
        
        return {
            'topics_explored': len(topics),
            'learning_depth': depth,
            'hands_on_practice': has_code_practice,
            'engagement_level': 'high' if len(self.history) > 10 else 'moderate' if len(self.history) > 5 else 'low'
        }


def test_time_manager():
    """测试时间管理器功能"""
    print("=== 时间管理器功能测试 ===")
    
    # 创建时间管理器
    tm = TimeManager()
    
    print(f"当前时间: {tm.format_datetime()}")
    print(f"ISO格式: {tm.iso_format()}")
    print(f"UTC时间: {tm.format_datetime(tm.utc_now())}")
    print(f"时间戳: {tm.timestamp()}")
    
    # 测试时间差
    import time
    time.sleep(1)
    elapsed = tm.elapsed_time()
    print(f"经过时间: {tm.format_duration(elapsed)}")
    
    # 测试文件名生成
    filename = tm.session_filename("test_session")
    print(f"会话文件名: {filename}")
    
    print("✅ 时间管理器测试完成")


if __name__ == "__main__":
    test_time_manager()