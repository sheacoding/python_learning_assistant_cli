# Python学习助手 - UV 项目管理指南

本项目使用 [uv](https://github.com/astral-sh/uv) 作为现代 Python 包管理工具，提供快速、可靠的依赖管理和虚拟环境支持。

## 🚀 快速开始

### 1. 安装 uv

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Unix/Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 自动安装项目

**Windows:**
```cmd
setup.bat
```

**Unix/Linux/macOS:**
```bash
./setup.sh
```

### 3. 手动安装步骤

```bash
# 创建虚拟环境并安装依赖
uv sync

# 安装开发依赖
uv sync --extra dev
```

## 📦 项目结构

```
python_learning_assistant/
├── .venv/                    # uv 创建的虚拟环境
├── src/                      # 源代码
│   ├── main.py              # 主程序
│   ├── api_key_manager.py   # API密钥管理
│   └── time_manager.py      # 时间管理模块
├── config/                   # 配置文件
├── docs/                     # 文档
├── examples/                 # 示例代码
├── sessions/                 # 会话存储
├── pyproject.toml           # 项目配置和依赖
├── uv.lock                  # 依赖版本锁定文件
├── setup.bat                # Windows 自动安装脚本
└── setup.sh                 # Unix/Linux 自动安装脚本
```

## 🔧 常用命令

### 运行项目
```bash
# 使用 uv 运行
uv run python run.py

# 或者激活虚拟环境后运行
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Unix/Linux

python run.py
```

### 开发工具
```bash
# 运行测试
uv run pytest

# 代码格式化
uv run black src/ examples/ test*.py run.py

# 代码检查
uv run flake8 src/ examples/ test*.py run.py

# 类型检查
uv run mypy src/
```

### 依赖管理
```bash
# 添加新的依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 移除依赖
uv remove package-name

# 更新依赖
uv sync --upgrade

# 查看依赖树
uv tree
```

### 虚拟环境管理
```bash
# 查看虚拟环境信息
uv venv --show

# 激活虚拟环境
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Unix/Linux

# 退出虚拟环境
deactivate
```

## 📋 项目依赖

### 运行时依赖
- `openai>=1.0.0` - OpenAI API 客户端
- `requests>=2.28.0` - HTTP 请求库

### 开发依赖
- `pytest>=7.0.0` - 测试框架
- `black>=23.0.0` - 代码格式化工具
- `flake8>=6.0.0` - 代码检查工具
- `mypy>=1.0.0` - 类型检查工具

## 🎯 使用优势

### 1. **超快速度**
- uv 比 pip 快 10-100 倍
- 依赖解析和安装都极其快速

### 2. **可靠性**
- 确定性的依赖解析
- 锁定文件确保环境一致性

### 3. **简单易用**
- 单个命令完成所有操作
- 自动管理虚拟环境

### 4. **完整生态**
- 兼容 pip 和 PyPI
- 支持现代 Python 项目标准

## 🚀 分发给其他用户

当您要分发这个项目给其他用户时，他们只需要：

1. **克隆项目**
2. **安装 uv**
3. **运行安装脚本**

```bash
# 克隆项目
git clone <repository-url>
cd python_learning_assistant

# Windows
setup.bat

# Unix/Linux/macOS
./setup.sh
```

就这么简单！uv 会自动处理：
- 创建虚拟环境
- 安装正确版本的依赖
- 配置开发环境

## 🔧 故障排除

### 常见问题

1. **uv 命令不存在**
   - 确保 uv 已正确安装
   - 重新启动终端或命令提示符

2. **依赖安装失败**
   - 检查网络连接
   - 尝试使用 `uv sync --offline` 使用缓存

3. **虚拟环境激活失败**
   - 确保使用正确的激活命令
   - 检查虚拟环境路径

### 获取帮助

```bash
# 查看 uv 帮助
uv --help

# 查看特定命令帮助
uv sync --help
```

## 📝 额外配置

### 配置文件位置
- 主配置：`config/config.json`
- API密钥：`config/api_keys.json`
- 项目配置：`pyproject.toml`

### 环境变量
- `MOONSHOT_API_KEY` - Moonshot API 密钥
- `UV_LINK_MODE=copy` - 如果需要复制而不是硬链接

---

通过使用 uv，这个项目现在拥有了现代化的 Python 包管理体验，让用户可以快速、可靠地设置和运行项目！
