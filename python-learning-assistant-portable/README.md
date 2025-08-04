# Python学习助手

一个功能丰富的Python学习终端应用，支持智能问答、代码执行、语法高亮和多轮对话。

## 🚀 功能特性

- **🎯 智能问答** - 专业Python知识解答
- **💻 代码执行** - 实时运行和测试代码
- **🎨 语法高亮** - 美观的代码显示
- **📚 学习指导** - 个性化学习建议
- **💾 会话保存** - 学习进度记录
- **🔧 可配置** - 支持自定义配置

## 📁 项目结构

```
python_learning_assistant/
├── src/                    # 源代码目录
│   └── main.py            # 主应用程序
├── config/                # 配置文件目录
│   └── config.json        # 应用配置
├── docs/                  # 文档目录
│   ├── README.md          # 项目说明
│   ├── USAGE.md           # 使用指南
│   ├── CONFIG.md          # 配置说明
│   └── INSTALL.md         # 安装指南
├── examples/              # 示例代码目录
│   ├── basic_examples.py  # 基础示例
│   └── advanced_examples.py # 高级示例
├── sessions/              # 会话保存目录
├── requirements.txt       # 依赖包列表
├── pyproject.toml         # 现代化项目配置（推荐）
├── setup.py              # 传统安装脚本
├── run.py                # 启动脚本
├── test.py               # 测试脚本
├── LICENSE               # 开源许可证
└── README.md             # 项目说明
```

## 🛠 快速开始

### 方法一：使用 uv（推荐）

**uv** 是现代、快速的 Python 包管理器，提供极速的依赖管理体验。

#### 自动安装

**Windows:**
```cmd
setup.bat
```

**Unix/Linux/macOS:**
```bash
./setup.sh
```

#### 手动安装

1. **安装 uv**
   ```bash
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Unix/Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **同步依赖**
   ```bash
   uv sync
   ```

3. **运行应用**
   ```bash
   uv run python run.py
   ```

**优势：**
- ⚡ 比 pip 快 10-100 倍
- 🔒 自动依赖锁定确保环境一致
- 📦 自动虚拟环境管理
- 🔧 内置开发工具支持

### 方法二：传统 pip 方式

1. **进入项目目录**
   ```bash
   cd python_learning_assistant
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Unix/Linux/macOS
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install openai requests
   ```
   
   或者：
   ```bash
   pip install -r requirements.txt
   ```

4. **设置API密钥**
   ```bash
   # Windows
   set MOONSHOT_API_KEY=your_api_key_here
   
   # Linux/Mac
   export MOONSHOT_API_KEY=your_api_key_here
   ```

5. **运行应用**
   ```bash
   python run.py
   ```

### 方法三：包安装

如果你的环境支持现代Python打包工具：

```bash
# 使用 pyproject.toml（推荐）
pip install -e .

# 或使用传统 setup.py
python setup.py develop
```

然后可以通过命令行直接启动：
```bash
python-learning-assistant
```

## 💡 使用指南

### 基本命令

- `/help` - 显示帮助信息
- `/quit` 或 `/exit` - 退出程序
- `/clear` - 清屏
- `/save` - 保存当前会话
- `/history` - 显示对话历史

### 学习功能

- `/examples` - 显示Python代码示例
- `/topics` - 显示学习主题建议
- `/run <code>` - 执行Python代码

### 使用技巧

- 直接输入Python问题开始对话
- 代码会自动高亮显示
- 支持多轮对话上下文
- 可以要求执行代码示例

## ⚙️ 配置说明

编辑 `config/config.json` 文件可以自定义应用行为：

```json
{
  "model": "kimi-k2-0711-preview",
  "temperature": 0.3,
  "max_tokens": 2048,
  "max_history": 50,
  "code_timeout": 10,
  "auto_save_sessions": true
}
```

详细配置说明请参考 [CONFIG.md](docs/CONFIG.md)

## 📝 示例

### 基础使用

```
🐍 Python学习 > 什么是列表推导式？

🤖 助手回答:
列表推导式是Python中一种简洁的创建列表的方法...

📝 代码示例:
┌──────────────────────────────────────────────────┐
│ numbers = [1, 2, 3, 4, 5]
│ squares = [x**2 for x in numbers]
│ print(squares)  # [1, 4, 9, 16, 25]
└──────────────────────────────────────────────────┘
```

### 代码执行

```
🐍 Python学习 > /run for i in range(3): print(f"Hello {i}")

🚀 执行代码:
┌──────────────────────────────────────────────────┐
│ for i in range(3): print(f"Hello {i}")
└──────────────────────────────────────────────────┘

📤 输出结果:
Hello 0
Hello 1
Hello 2
```

## 🧪 测试

运行测试脚本验证项目完整性：

```bash
python test.py
```

## 📚 文档

- [使用指南](docs/USAGE.md) - 详细的使用说明
- [配置说明](docs/CONFIG.md) - 配置文件详解
- [安装指南](docs/INSTALL.md) - 各种安装方式
- [UV 项目管理指南](UV_GUIDE.md) - uv 包管理器使用指南

## 🔧 开发

### 添加新功能

1. 在 `src/main.py` 中添加新的命令处理
2. 更新配置文件（如需要）
3. 添加相应的文档

### 自定义提示词

编辑 `config/config.json` 中的 `system_prompt` 字段来自定义AI助手的行为。

### 运行示例

```bash
# 运行基础示例
python examples/basic_examples.py

# 运行高级示例
python examples/advanced_examples.py
```

## 📋 系统要求

- Python 3.7 或更高版本
- 网络连接（用于AI API调用）
- 支持ANSI颜色的终端（用于语法高亮）

## 🔑 API密钥

本项目使用Moonshot AI的API服务。你需要：

1. 注册Moonshot AI账户
2. 获取API密钥
3. 设置环境变量 `MOONSHOT_API_KEY`

## 🐛 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **API密钥未设置**
   ```bash
   echo $MOONSHOT_API_KEY  # Linux/Mac
   echo %MOONSHOT_API_KEY%  # Windows
   ```

3. **编码问题**
   - 确保终端支持UTF-8编码
   - Windows用户可能需要使用Windows Terminal

### 获取帮助

1. 查看 [使用指南](docs/USAGE.md)
2. 运行 `python test.py` 进行诊断
3. 检查项目Issue页面

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 🌟 特性规划

- [ ] 支持更多AI模型
- [ ] 图形界面版本
- [ ] 插件系统
- [ ] 多语言支持
- [ ] 代码补全功能

## 📧 联系

如有问题或建议，请提交Issue。