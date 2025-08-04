#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python学习助手 - 单文件版本
包含所有依赖模块的独立版本
"""

# ========== 依赖模块 ==========
# === api_key_manager.py ===
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API密钥管理模块
提供API密钥的读取、验证和管理功能
支持配置文件优先，环境变量兜底的策略
"""

import os
import json
from typing import Optional, Dict
from pathlib import Path


class APIKeyManager:
    """API密钥管理器"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化API密钥管理器
        
        Args:
            config_dir: 配置目录路径，如果为None则使用默认路径
        """
        if config_dir is None:
            # 获取项目根目录下的config目录
            current_dir = Path(__file__).parent
            self.config_dir = current_dir.parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        self.api_keys_file = self.config_dir / "api_keys.json"
        self._api_keys_cache = None
    
    def _load_api_keys_from_file(self) -> Dict[str, str]:
        """
        从配置文件加载API密钥
        
        Returns:
            API密钥字典
        """
        if not self.api_keys_file.exists():
            return {}
        
        try:
            with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 过滤掉空值和非字符串值
            api_keys = {}
            for key, value in data.items():
                if isinstance(value, str) and value.strip():
                    api_keys[key] = value.strip()
            
            return api_keys
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 读取API密钥配置文件失败: {e}")
            return {}
    
    def _get_api_key_from_env(self, key_name: str) -> Optional[str]:
        """
        从环境变量获取API密钥
        
        Args:
            key_name: 环境变量名
            
        Returns:
            API密钥或None
        """
        return os.getenv(key_name)
    
    def get_moonshot_api_key(self) -> Optional[str]:
        """
        获取Moonshot API密钥
        优先从配置文件读取，如果不存在则从环境变量读取
        
        Returns:
            API密钥或None
        """
        # 先尝试从配置文件读取
        api_keys = self._load_api_keys_from_file()
        moonshot_key = api_keys.get('moonshot_api_key')
        
        if moonshot_key:
            return moonshot_key
        
        # 如果配置文件中没有，则从环境变量读取
        return self._get_api_key_from_env('MOONSHOT_API_KEY')
    
    def get_openai_api_key(self) -> Optional[str]:
        """
        获取OpenAI API密钥
        优先从配置文件读取，如果不存在则从环境变量读取
        
        Returns:
            API密钥或None
        """
        # 先尝试从配置文件读取
        api_keys = self._load_api_keys_from_file()
        openai_key = api_keys.get('openai_api_key')
        
        if openai_key:
            return openai_key
        
        # 如果配置文件中没有，则从环境变量读取
        return self._get_api_key_from_env('OPENAI_API_KEY')
    
    def get_api_key(self, service: str) -> Optional[str]:
        """
        通用API密钥获取方法
        
        Args:
            service: 服务名称 ('moonshot' 或 'openai')
            
        Returns:
            API密钥或None
        """
        if service.lower() == 'moonshot':
            return self.get_moonshot_api_key()
        elif service.lower() == 'openai':
            return self.get_openai_api_key()
        else:
            raise ValueError(f"不支持的服务: {service}")
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        验证API密钥格式是否正确
        
        Args:
            api_key: API密钥
            
        Returns:
            是否有效
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        # 基本格式验证
        api_key = api_key.strip()
        if len(api_key) < 20:  # API密钥通常比较长
            return False
        
        # 检查是否包含明显的占位符
        invalid_patterns = ['your_api_key', 'placeholder', 'example', 'test']
        for pattern in invalid_patterns:
            if pattern in api_key.lower():
                return False
        
        return True
    
    def save_api_key(self, service: str, api_key: str) -> bool:
        """
        保存API密钥到配置文件
        
        Args:
            service: 服务名称 ('moonshot' 或 'openai')
            api_key: API密钥
            
        Returns:
            是否保存成功
        """
        if not self.validate_api_key(api_key):
            print(f"错误: API密钥格式无效")
            return False
        
        try:
            # 确保配置目录存在
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # 读取现有配置
            if self.api_keys_file.exists():
                with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            
            # 更新API密钥
            key_name = f"{service.lower()}_api_key"
            data[key_name] = api_key
            
            # 保存到文件
            with open(self.api_keys_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {service} API密钥已保存到配置文件")
            return True
            
        except Exception as e:
            print(f"错误: 保存API密钥失败: {e}")
            return False
    
    def check_api_key_availability(self) -> Dict[str, bool]:
        """
        检查各种API密钥的可用性
        
        Returns:
            各服务API密钥的可用性状态
        """
        result = {}
        
        # 检查Moonshot API密钥
        moonshot_key = self.get_moonshot_api_key()
        result['moonshot'] = bool(moonshot_key and self.validate_api_key(moonshot_key))
        
        # 检查OpenAI API密钥
        openai_key = self.get_openai_api_key()
        result['openai'] = bool(openai_key and self.validate_api_key(openai_key))
        
        return result
    
    def print_api_key_status(self):
        """打印API密钥状态信息"""
        print("\n🔑 API密钥状态")
        print("=" * 40)
        
        # 检查配置文件是否存在
        if self.api_keys_file.exists():
            print(f"✅ 配置文件存在: {self.api_keys_file}")
        else:
            print(f"⚠️  配置文件不存在: {self.api_keys_file}")
        
        # 检查各服务的API密钥状态
        status = self.check_api_key_availability()
        
        print(f"\n📊 密钥可用性:")
        for service, available in status.items():
            status_icon = "✅" if available else "❌"
            print(f"  {status_icon} {service.capitalize()}: {'可用' if available else '不可用'}")
        
        # 提供配置建议
        if not any(status.values()):
            print(f"\n💡 配置建议:")
            print(f"  1. 编辑配置文件: {self.api_keys_file}")
            print(f"  2. 或设置环境变量: MOONSHOT_API_KEY")
    
    def create_example_config(self) -> bool:
        """
        创建示例配置文件
        
        Returns:
            是否创建成功
        """
        try:
            # 确保配置目录存在
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # 示例配置内容
            example_config = {
                "moonshot_api_key": "",
                "openai_api_key": "",
                "note": "请在此处填入您的API密钥。如果留空，程序将从系统环境变量中读取。",
                "instructions": {
                    "moonshot": "从 https://platform.moonshot.cn/ 获取",
                    "openai": "从 https://platform.openai.com/ 获取"
                }
            }
            
            # 如果文件已存在，不覆盖
            if self.api_keys_file.exists():
                print(f"⚠️  配置文件已存在: {self.api_keys_file}")
                return False
            
            # 写入示例配置
            with open(self.api_keys_file, 'w', encoding='utf-8') as f:
                json.dump(example_config, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 示例配置文件已创建: {self.api_keys_file}")
            return True
            
        except Exception as e:
            print(f"错误: 创建示例配置文件失败: {e}")
            return False


def test_api_key_manager():
    """测试API密钥管理器"""
    print("=== API密钥管理器测试 ===")
    
    # 创建管理器实例
    manager = APIKeyManager()
    
    # 打印状态信息
    manager.print_api_key_status()
    
    # 测试获取API密钥
    moonshot_key = manager.get_moonshot_api_key()
    print(f"\n🔍 测试结果:")
    print(f"  Moonshot API密钥: {'已配置' if moonshot_key else '未配置'}")
    
    print("\n✅ 测试完成")


if __name__ == "__main__":
    test_api_key_manager()


# === main.py ===
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python学习助手 - 智能终端应用
支持多轮对话、代码高亮、语法检查和交互式学习
增强版：集成高级时间管理功能
"""

import os
import sys
import json
import time
import datetime
import traceback
import subprocess
from typing import Dict, List, Optional
from openai import OpenAI

# 导入时间管理模块
try:
    from .time_manager import TimeManager, EnhancedConversationHistory
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    try:
        from time_manager import TimeManager, EnhancedConversationHistory
    except ImportError:
        # 如果时间管理模块不可用，使用原始实现
        TimeManager = None
        EnhancedConversationHistory = None

# 导入API密钥管理模块
try:
    from .api_key_manager import APIKeyManager
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    try:
        from api_key_manager import APIKeyManager
    except ImportError:
        # 如果API密钥管理模块不可用，使用原始实现
        APIKeyManager = None


class Colors:
    """ANSI颜色代码"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 明亮前景色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class PythonSyntaxHighlighter:
    """Python代码语法高亮器"""
    
    KEYWORDS = {
        'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 
        'finally', 'with', 'import', 'from', 'as', 'return', 'yield', 'break', 
        'continue', 'pass', 'and', 'or', 'not', 'in', 'is', 'lambda', 'global', 
        'nonlocal', 'assert', 'del', 'raise', 'async', 'await'
    }
    
    BUILTINS = {
        'print', 'len', 'range', 'list', 'dict', 'set', 'tuple', 'str', 'int', 
        'float', 'bool', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
        'min', 'max', 'sum', 'abs', 'round', 'sorted', 'reversed', 'enumerate',
        'zip', 'map', 'filter', 'any', 'all', 'open', 'input'
    }
    
    @classmethod
    def highlight(cls, code: str) -> str:
        """给Python代码添加语法高亮"""
        lines = code.split('\n')
        highlighted_lines = []
        
        for line in lines:
            highlighted_line = line
            
            # 高亮关键字
            for keyword in cls.KEYWORDS:
                highlighted_line = highlighted_line.replace(
                    f' {keyword} ', f' {Colors.BLUE}{keyword}{Colors.RESET} '
                )
                if highlighted_line.startswith(keyword + ' '):
                    highlighted_line = f'{Colors.BLUE}{keyword}{Colors.RESET}' + highlighted_line[len(keyword):]
            
            # 高亮内置函数
            for builtin in cls.BUILTINS:
                highlighted_line = highlighted_line.replace(
                    f'{builtin}(', f'{Colors.CYAN}{builtin}{Colors.RESET}('
                )
            
            # 高亮字符串
            import re
            # 简单的字符串高亮（单引号和双引号）
            highlighted_line = re.sub(
                r'(["\'])([^"\']*)\1', 
                f'{Colors.GREEN}\\1\\2\\1{Colors.RESET}', 
                highlighted_line
            )
            
            # 高亮注释
            if '#' in highlighted_line:
                comment_pos = highlighted_line.find('#')
                highlighted_line = (highlighted_line[:comment_pos] + 
                                  f'{Colors.BRIGHT_BLACK}{highlighted_line[comment_pos:]}{Colors.RESET}')
            
            highlighted_lines.append(highlighted_line)
        
        return '\n'.join(highlighted_lines)


class ConversationHistory:
    """对话历史管理"""
    
    def __init__(self, max_history: int = 50, sessions_dir: str = None):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.session_start = datetime.datetime.now()
        self.sessions_dir = sessions_dir or os.path.join(os.path.dirname(__file__), '..', 'sessions')
        
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
            print(f"{Colors.RED}保存会话失败: {e}{Colors.RESET}")
            return None
    
    def load_session(self, filename: str):
        """加载对话会话"""
        try:
            filepath = os.path.join(self.sessions_dir, filename) if not os.path.isabs(filename) else filename
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            self.history = session_data.get('history', [])
            print(f"{Colors.GREEN}成功加载会话: {filename}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}加载会话失败: {e}{Colors.RESET}")


class PythonLearningAssistant:
    """Python学习助手主类（增强时间管理版）"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), '..', 'config')
        self.client = self._initialize_client()
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化时间管理器
        timezone = self.config.get('timezone', None)
        self.time_manager = TimeManager(timezone) if TimeManager else None
        
        # 选择使用增强的对话历史管理器或原始版本
        if EnhancedConversationHistory and self.time_manager:
            self.history = EnhancedConversationHistory(
                max_history=self.config.get('max_history', 50),
                sessions_dir=os.path.join(os.path.dirname(__file__), '..', 'sessions'),
                timezone=timezone
            )
        else:
            self.history = ConversationHistory(
                sessions_dir=os.path.join(os.path.dirname(__file__), '..', 'sessions')
            )
        
        self.running = True
        self.code_execution_globals = {}
        
        # 系统提示词
        self.system_prompt = self.config.get('system_prompt', self._get_default_system_prompt())
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        config_file = os.path.join(self.config_dir, 'config.json')
        default_config = {
            "model": "kimi-k2-0711-preview",
            "temperature": 0.3,
            "max_tokens": 2048,
            "max_history": 50,
            "code_timeout": 10,
            "auto_save_sessions": True
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            print(f"{Colors.YELLOW}警告: 加载配置文件失败，使用默认配置: {e}{Colors.RESET}")
        
        return default_config
    
    def _get_default_system_prompt(self) -> str:
        """获取默认系统提示词"""
        return """你是一个专业的Python编程学习助手。你的任务是帮助用户学习Python编程知识，提供清晰易懂的解释和实用的代码示例。

请遵循以下原则：
1. 使用简洁明了的中文回答
2. 提供可运行的代码示例
3. 解释代码的工作原理
4. 推荐最佳实践
5. 根据用户水平调整解释深度
6. 鼓励动手实践
7. 提供相关的学习资源

当用户询问Python相关问题时，请：
- 先给出简要回答
- 提供代码示例（如果适用）
- 解释关键概念
- 建议进一步学习的方向

如果用户需要代码执行，使用code_runner工具来演示。"""
    
    def _initialize_client(self) -> OpenAI:
        """初始化OpenAI客户端"""
        # 使用API密钥管理器获取密钥
        api_key = None
        
        if APIKeyManager:
            # 如果API密钥管理器可用，使用它
            api_key_manager = APIKeyManager(self.config_dir)
            api_key = api_key_manager.get_moonshot_api_key()
            
            if not api_key:
                print(f"{Colors.RED}错误: 未找到Moonshot API密钥{Colors.RESET}")
                print(f"{Colors.YELLOW}请通过以下方式之一配置API密钥：{Colors.RESET}")
                print(f"  1. 编辑配置文件: {api_key_manager.api_keys_file}")
                print(f"  2. 设置环境变量: MOONSHOT_API_KEY")
                print(f"\n{Colors.BRIGHT_BLUE}配置文件示例：{Colors.RESET}")
                print(f"  {{")
                print(f"    \"moonshot_api_key\": \"your_api_key_here\",")
                print(f"    \"openai_api_key\": \"\"")
                print(f"  }}")
                
                # 显示当前API密钥状态
                api_key_manager.print_api_key_status()
                sys.exit(1)
        else:
            # 如果API密钥管理器不可用，使用原始方法
            api_key = os.getenv("MOONSHOT_API_KEY")
            if not api_key:
                print(f"{Colors.RED}错误: 请设置MOONSHOT_API_KEY环境变量{Colors.RESET}")
                sys.exit(1)
        
        return OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )
    
    def _get_tools_definition(self) -> List[Dict]:
        """获取工具定义"""
        return [
            {
                "function": {
                    "name": "web_search",
                    "description": "搜索网络信息，获取最新的Python相关资料和文档",
                    "parameters": {
                        "properties": {
                            "classes": {
                                "description": "搜索领域，专注于特定类型的内容",
                                "items": {
                                    "enum": ["all", "academic", "code", "library"],
                                    "type": "string"
                                },
                                "type": "array"
                            },
                            "query": {
                                "description": "搜索关键词",
                                "type": "string"
                            }
                        },
                        "required": ["query"],
                        "type": "object"
                    }
                },
                "type": "function"
            },
            {
                "function": {
                    "name": "code_runner",
                    "description": "Python代码执行器，支持安全运行Python代码并返回执行结果",
                    "parameters": {
                        "properties": {
                            "code": {
                                "description": "需要执行的Python代码",
                                "type": "string"
                            }
                        },
                        "required": ["code"],
                        "type": "object"
                    }
                },
                "type": "function"
            }
        ]
    
    def print_welcome(self):
        """打印欢迎信息"""
        welcome_text = f"""
{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}
{Colors.BOLD}{Colors.BRIGHT_YELLOW}    🐍 Python学习助手 - 智能终端应用 🐍{Colors.RESET}
{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}

{Colors.BRIGHT_GREEN}功能特性:{Colors.RESET}
  • 🎯 智能问答 - 专业Python知识解答
  • 💻 代码执行 - 实时运行和测试代码
  • 🎨 语法高亮 - 美观的代码显示
  • 📚 学习指导 - 个性化学习建议
  • 💾 会话保存 - 学习进度记录

{Colors.BRIGHT_YELLOW}使用指南:{Colors.RESET}
  • 输入Python相关问题开始学习
  • 使用 {Colors.CYAN}/help{Colors.RESET} 查看所有命令
  • 使用 {Colors.CYAN}/quit{Colors.RESET} 退出程序
  • 使用 {Colors.CYAN}/clear{Colors.RESET} 清屏
  • 使用 {Colors.CYAN}/save{Colors.RESET} 保存会话

{Colors.BRIGHT_MAGENTA}让我们开始Python学习之旅吧！{Colors.RESET}
{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}
"""
        print(welcome_text)
    
    def print_help(self):
        """打印帮助信息"""
        help_text = f"""
{Colors.BRIGHT_BLUE}📖 命令帮助{Colors.RESET}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}

{Colors.BRIGHT_GREEN}基本命令:{Colors.RESET}
  {Colors.YELLOW}/help{Colors.RESET}     - 显示此帮助信息
  {Colors.YELLOW}/quit{Colors.RESET}     - 退出程序
  {Colors.YELLOW}/exit{Colors.RESET}     - 退出程序（同/quit）
  {Colors.YELLOW}/clear{Colors.RESET}    - 清屏

{Colors.BRIGHT_GREEN}会话管理:{Colors.RESET}
  {Colors.YELLOW}/save{Colors.RESET}     - 保存当前会话
  {Colors.YELLOW}/load{Colors.RESET}     - 加载历史会话
  {Colors.YELLOW}/history{Colors.RESET}  - 显示对话历史
  {Colors.YELLOW}/stats{Colors.RESET}    - 显示会话统计信息
  {Colors.YELLOW}/time{Colors.RESET}     - 显示时间信息
  {Colors.YELLOW}/apikey{Colors.RESET}   - 显示API密钥状态

{Colors.BRIGHT_GREEN}学习功能:{Colors.RESET}
  {Colors.YELLOW}/examples{Colors.RESET} - 显示Python代码示例
  {Colors.YELLOW}/topics{Colors.RESET}   - 显示学习主题建议
  {Colors.YELLOW}/run <代码>{Colors.RESET} - 执行Python代码

{Colors.BRIGHT_GREEN}使用技巧:{Colors.RESET}
  • 直接输入Python问题开始对话
  • 代码会自动高亮显示
  • 支持多轮对话上下文
  • 可以要求执行代码示例

{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
"""
        print(help_text)
    
    def print_examples(self):
        """打印Python代码示例"""
        examples = [
            ("变量和数据类型", "name = 'Python'\nage = 30\nprint(f'语言: {name}, 年龄: {age}年')"),
            ("列表操作", "fruits = ['苹果', '香蕉', '橙子']\nfruits.append('葡萄')\nprint(fruits)"),
            ("循环语句", "for i in range(5):\n    print(f'第{i+1}次循环')"),
            ("函数定义", "def greet(name):\n    return f'你好, {name}!'\n\nprint(greet('Python学习者'))"),
            ("字典操作", "student = {'姓名': '小明', '年龄': 18, '成绩': 95}\nprint(student['姓名'])"),
        ]
        
        print(f"\n{Colors.BRIGHT_BLUE}🔥 Python代码示例{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        for i, (title, code) in enumerate(examples, 1):
            print(f"\n{Colors.BRIGHT_YELLOW}{i}. {title}{Colors.RESET}")
            print(f"{Colors.DIM}┌{'─'*40}┐{Colors.RESET}")
            for line in code.split('\n'):
                highlighted_line = PythonSyntaxHighlighter.highlight(line)
                print(f"{Colors.DIM}│{Colors.RESET} {highlighted_line}")
            print(f"{Colors.DIM}└{'─'*40}┘{Colors.RESET}")
    
    def print_topics(self):
        """打印学习主题建议"""
        topics = [
            "🐍 Python基础语法",
            "📊 数据类型和变量",
            "🔄 控制流程（if/for/while）",
            "🎯 函数和模块",
            "📚 面向对象编程",
            "🗂️ 文件操作",
            "🌐 网络编程",
            "📈 数据分析（pandas/numpy）",
            "🖼️ GUI编程（tkinter）",
            "🕷️ 网页爬虫"
        ]
        
        print(f"\n{Colors.BRIGHT_BLUE}📖 Python学习主题{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        for topic in topics:
            print(f"  {topic}")
        
        print(f"\n{Colors.BRIGHT_GREEN}💡 提示: 选择一个主题，我可以为你详细讲解！{Colors.RESET}")
    
    def print_history(self):
        """打印对话历史"""
        print(f"\n{Colors.BRIGHT_BLUE}📜 对话历史 (最近10条){Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
        
        recent_history = self.history.get_context_messages(10)
        for i, msg in enumerate(recent_history, 1):
            role_color = Colors.BRIGHT_GREEN if msg['role'] == 'user' else Colors.BRIGHT_BLUE
            role_name = '用户' if msg['role'] == 'user' else '助手'
            content_preview = msg['content'][:80] + '...' if len(msg['content']) > 80 else msg['content']
            print(f"{role_color}{i:2d}. {role_name}:{Colors.RESET} {content_preview}")
        
        if hasattr(self.history, 'history') and len(self.history.history) > 10:
            print(f"\n{Colors.DIM}显示最近10条，总共{len(self.history.history)}条消息{Colors.RESET}")
    
    def print_session_stats(self):
        """打印会话统计信息"""
        print(f"\n{Colors.BRIGHT_BLUE}📊 会话统计信息{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
        
        if hasattr(self.history, 'get_session_summary'):
            # 使用增强版的统计功能
            summary = self.history.get_session_summary()
            
            # 时间信息
            time_info = summary.get('time_info', {})
            print(f"\n{Colors.BRIGHT_GREEN}⏰ 时间信息:{Colors.RESET}")
            print(f"  会话开始: {time_info.get('start_time', '未知')}")
            print(f"  当前时间: {time_info.get('end_time', '未知')}")
            print(f"  持续时间: {time_info.get('duration_formatted', '未知')}")
            
            # 统计信息
            stats = summary.get('statistics', {})
            print(f"\n{Colors.BRIGHT_GREEN}📈 对话统计:{Colors.RESET}")
            print(f"  总消息数: {stats.get('total_messages', 0)}")
            print(f"  用户消息: {stats.get('user_messages', 0)}")
            print(f"  助手回复: {stats.get('assistant_messages', 0)}")
            print(f"  执行命令: {stats.get('commands_executed', 0)}")
            print(f"  代码运行: {stats.get('code_executions', 0)}")
            
            # 学习主题
            topics = stats.get('topics_covered', [])
            if topics:
                print(f"\n{Colors.BRIGHT_GREEN}📚 学习主题:{Colors.RESET}")
                for topic in topics:
                    print(f"  • {topic}")
            
            # 学习进度
            progress = summary.get('learning_progress', {})
            print(f"\n{Colors.BRIGHT_GREEN}🎯 学习分析:{Colors.RESET}")
            print(f"  探索主题数: {progress.get('topics_explored', 0)}")
            print(f"  学习深度: {progress.get('learning_depth', '未知')}")
            print(f"  实践练习: {'是' if progress.get('hands_on_practice') else '否'}")
            print(f"  参与度: {progress.get('engagement_level', '未知')}")
            
        else:
            # 使用基础版的统计功能
            total_messages = len(self.history.history) if hasattr(self.history, 'history') else 0
            print(f"  总消息数: {total_messages}")
            
            if hasattr(self.history, 'session_start'):
                if hasattr(self.history.session_start, 'strftime'):
                    start_time = self.history.session_start.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    start_time = str(self.history.session_start)
                print(f"  会话开始: {start_time}")
                
                elapsed = datetime.datetime.now() - self.history.session_start
                hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if hours > 0:
                    duration = f"{hours}小时{minutes}分钟"
                elif minutes > 0:
                    duration = f"{minutes}分钟{seconds}秒"
                else:
                    duration = f"{seconds}秒"
                print(f"  持续时间: {duration}")
    
    def print_time_info(self):
        """打印时间信息"""
        print(f"\n{Colors.BRIGHT_BLUE}⏰ 时间信息{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        if self.time_manager:
            current_time = self.time_manager.now()
            print(f"  当前时间: {self.time_manager.format_datetime(current_time)}")
            print(f"  ISO格式: {self.time_manager.iso_format(current_time)}")
            print(f"  时区: {current_time.tzinfo}")
            print(f"  时间戳: {self.time_manager.timestamp()}")
            
            if hasattr(self.history, 'session_start_time'):
                elapsed = self.time_manager.elapsed_time(self.history.session_start_time)
                print(f"  会话时长: {self.time_manager.format_duration(elapsed)}")
        else:
            # 使用基础时间功能
            current_time = datetime.datetime.now()
            print(f"  当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  ISO格式: {current_time.isoformat()}")
            
            if hasattr(self.history, 'session_start'):
                elapsed = current_time - self.history.session_start
                total_seconds = int(elapsed.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                if hours > 0:
                    duration = f"{hours}小时{minutes}分钟{seconds}秒"
                elif minutes > 0:
                    duration = f"{minutes}分钟{seconds}秒"
                else:
                    duration = f"{seconds}秒"
                print(f"  会话时长: {duration}")
    
    def handle_load_command(self):
        """处理加载会话命令"""
        print(f"\n{Colors.BRIGHT_BLUE}📁 可用的会话文件{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        # 列出sessions目录中的文件
        sessions_dir = getattr(self.history, 'sessions_dir', 'sessions')
        if not os.path.exists(sessions_dir):
            print(f"{Colors.YELLOW}⚠️  sessions目录不存在{Colors.RESET}")
            return
        
        session_files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
        if not session_files:
            print(f"{Colors.YELLOW}⚠️  没有找到会话文件{Colors.RESET}")
            return
        
        # 显示文件列表
        for i, filename in enumerate(session_files, 1):
            filepath = os.path.join(sessions_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                created_time = session_data.get('created_time', '未知时间')
                message_count = len(session_data.get('history', []))
                print(f"  {Colors.GREEN}{i}. {filename}{Colors.RESET}")
                print(f"     创建时间: {created_time}")
                print(f"     消息数量: {message_count}条")
                print()
            except Exception as e:
                print(f"  {Colors.RED}{i}. {filename} (读取失败: {e}){Colors.RESET}")
        
        # 提示用户选择
        print(f"{Colors.BRIGHT_YELLOW}请输入要加载的文件编号 (1-{len(session_files)}) 或文件名:{Colors.RESET}")
        try:
            user_choice = input(f"{Colors.CYAN}选择> {Colors.RESET}").strip()
            
            if user_choice.isdigit():
                choice_num = int(user_choice)
                if 1 <= choice_num <= len(session_files):
                    filename = session_files[choice_num - 1]
                else:
                    print(f"{Colors.RED}❌ 无效的编号{Colors.RESET}")
                    return
            else:
                if user_choice.endswith('.json'):
                    filename = user_choice
                else:
                    filename = user_choice + '.json'
                
                if filename not in session_files:
                    print(f"{Colors.RED}❌ 文件不存在: {filename}{Colors.RESET}")
                    return
            
            # 加载会话
            if hasattr(self.history, 'load_session'):
                self.history.load_session(filename)
            else:
                print(f"{Colors.RED}❌ 当前历史记录对象不支持加载功能{Colors.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}取消加载{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ 加载失败: {e}{Colors.RESET}")
    
    def execute_local_code(self, code: str) -> str:
        """本地执行Python代码"""
        try:
            # 创建临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # 执行代码并捕获输出
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.config.get('code_timeout', 10)
            )
            
            # 清理临时文件
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"错误: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return f"代码执行超时（{self.config.get('code_timeout', 10)}秒限制）"
        except Exception as e:
            return f"执行错误: {str(e)}"
    
    def format_ai_response(self, content: str) -> str:
        """格式化AI响应内容"""
        lines = content.split('\n')
        formatted_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```python') or line.strip().startswith('```'):
                in_code_block = not in_code_block
                if line.strip().startswith('```python'):
                    formatted_lines.append(f"{Colors.BRIGHT_BLUE}📝 代码示例:{Colors.RESET}")
                    formatted_lines.append(f"{Colors.DIM}┌{'─'*50}┐{Colors.RESET}")
                elif line.strip() == '```' and not in_code_block:
                    formatted_lines.append(f"{Colors.DIM}└{'─'*50}┘{Colors.RESET}")
                continue
            
            if in_code_block:
                highlighted_line = PythonSyntaxHighlighter.highlight(line)
                formatted_lines.append(f"{Colors.DIM}│{Colors.RESET} {highlighted_line}")
            else:
                # 格式化普通文本
                if line.strip().startswith('#'):
                    formatted_lines.append(f"{Colors.BRIGHT_GREEN}{line}{Colors.RESET}")
                elif line.strip().startswith('*') or line.strip().startswith('-'):
                    formatted_lines.append(f"{Colors.CYAN}{line}{Colors.RESET}")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def process_user_input(self, user_input: str) -> bool:
        """处理用户输入"""
        user_input = user_input.strip()
        
        # 处理命令
        if user_input.startswith('/'):
            command = user_input[1:].lower()
            
            if command in ['quit', 'exit']:
                print(f"{Colors.BRIGHT_YELLOW}👋 感谢使用Python学习助手！继续加油学习！{Colors.RESET}")
                return False
            
            elif command == 'help':
                self.print_help()
                return True
            
            elif command == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print_welcome()
                return True
            
            elif command == 'save':
                filename = self.history.save_session()
                if filename:
                    print(f"{Colors.GREEN}✅ 会话已保存到: {filename}{Colors.RESET}")
                return True
            
            elif command == 'examples':
                self.print_examples()
                return True
            
            elif command == 'topics':
                self.print_topics()
                return True
            
            elif command == 'history':
                self.print_history()
                return True
            
            elif command == 'load':
                self.handle_load_command()
                return True
            
            elif command == 'stats':
                self.print_session_stats()
                return True
            
            elif command == 'time':
                self.print_time_info()
                return True
            
            elif command == 'apikey':
                self.handle_apikey_command()
                return True
            
            elif command.startswith('run '):
                code = user_input[5:]  # 移除'/run '
                print(f"{Colors.BRIGHT_BLUE}🚀 执行代码:{Colors.RESET}")
                highlighted_code = PythonSyntaxHighlighter.highlight(code)
                print(f"{Colors.DIM}┌{'─'*50}┐{Colors.RESET}")
                for line in highlighted_code.split('\n'):
                    print(f"{Colors.DIM}│{Colors.RESET} {line}")
                print(f"{Colors.DIM}└{'─'*50}┘{Colors.RESET}")
                
                result = self.execute_local_code(code)
                print(f"{Colors.BRIGHT_GREEN}📤 输出结果:{Colors.RESET}")
                print(result)
                return True
            
            elif command == 'run':
                print(f"{Colors.YELLOW}💡 用法: /run <Python代码>{Colors.RESET}")
                print(f"{Colors.CYAN}示例: /run print('Hello, World!'){Colors.RESET}")
                return True
            
            else:
                print(f"{Colors.RED}❌ 未知命令: {command}。使用 /help 查看帮助。{Colors.RESET}")
                return True
        
        # 处理普通对话
        if not user_input:
            return True
        
        # 添加用户消息到历史
        self.history.add_message('user', user_input)
        
        # 显示思考状态
        print(f"{Colors.BRIGHT_BLUE}🤔 正在思考...{Colors.RESET}")
        
        try:
            # 准备消息
            messages = [{'role': 'system', 'content': self.system_prompt}]
            messages.extend(self.history.get_context_messages(8))
            
            # 发送请求
            response = self.client.chat.completions.create(
                model=self.config.get('model', 'kimi-k2-0711-preview'),
                messages=messages,
                tools=self._get_tools_definition(),
                temperature=self.config.get('temperature', 0.3),
                max_tokens=self.config.get('max_tokens', 2048),
                top_p=1,
                stream=False
            )
            
            # 处理响应
            assistant_message = response.choices[0].message
            
            if assistant_message.content:
                formatted_response = self.format_ai_response(assistant_message.content)
                print(f"\n{Colors.BRIGHT_MAGENTA}🤖 助手回答:{Colors.RESET}")
                print(formatted_response)
                
                # 添加助手消息到历史
                self.history.add_message('assistant', assistant_message.content)
            
            # 处理工具调用
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    if function_name == 'code_runner':
                        code = json.loads(tool_call.function.arguments)['code']
                        print(f"\n{Colors.BRIGHT_BLUE}🔧 执行代码:{Colors.RESET}")
                        highlighted_code = PythonSyntaxHighlighter.highlight(code)
                        print(f"{Colors.DIM}┌{'─'*50}┐{Colors.RESET}")
                        for line in highlighted_code.split('\n'):
                            print(f"{Colors.DIM}│{Colors.RESET} {line}")
                        print(f"{Colors.DIM}└{'─'*50}┘{Colors.RESET}")
                        
                        result = self.execute_local_code(code)
                        print(f"{Colors.BRIGHT_GREEN}📤 执行结果:{Colors.RESET}")
                        print(result)
        
        except Exception as e:
            print(f"{Colors.RED}❌ 请求失败: {e}{Colors.RESET}")
            print(f"{Colors.BRIGHT_BLACK}💡 请检查网络连接和API密钥配置{Colors.RESET}")
        
        return True
    
    def handle_apikey_command(self):
        """处理API密钥管理命令"""
        if not APIKeyManager:
            print(f"{Colors.RED}错误: APIKeyManager模块不可用{Colors.RESET}")
            return

        api_key_manager = APIKeyManager(self.config_dir)
        api_key_manager.print_api_key_status()
    
    def run(self):
        """运行主程序循环"""
        self.print_welcome()
        
        try:
            while self.running:
                # 显示提示符
                prompt = f"{Colors.BRIGHT_CYAN}🐍 Python学习 > {Colors.RESET}"
                try:
                    user_input = input(prompt)
                except KeyboardInterrupt:
                    print(f"\n{Colors.BRIGHT_YELLOW}👋 检测到Ctrl+C，程序退出！{Colors.RESET}")
                    break
                except EOFError:
                    print(f"\n{Colors.BRIGHT_YELLOW}👋 程序退出！{Colors.RESET}")
                    break
                
                # 处理输入
                if not self.process_user_input(user_input):
                    break
                
                print()  # 添加空行分隔
        
        except Exception as e:
            print(f"{Colors.RED}程序异常: {e}{Colors.RESET}")
            traceback.print_exc()
        
        finally:
            # 自动保存会话
            if self.config.get('auto_save_sessions', True) and len(self.history.history) > 1:
                filename = self.history.save_session()
                if filename:
                    print(f"{Colors.GREEN}📁 会话已自动保存到: {filename}{Colors.RESET}")


def main():
    """主函数"""
    try:
        app = PythonLearningAssistant()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}👋 程序退出！{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}启动失败: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# === time_manager.py ===
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

# ========== 主程序 ==========
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