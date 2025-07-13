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
