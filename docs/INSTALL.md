# 安装指南

## 现代化安装方式（推荐）

### 使用 pip 和 pyproject.toml

Python学习助手现在使用现代化的 `pyproject.toml` 配置文件，推荐使用以下方式安装：

```bash
# 开发模式安装（推荐）
pip install -e .

# 或者正常安装
pip install .
```

## 传统安装方式

### 使用 setup.py

如果你的环境不支持 `pyproject.toml`，可以使用传统的 setup.py：

```bash
# 开发模式安装
python setup.py develop

# 或者正常安装
python setup.py install
```

## 从源码安装

### 1. 克隆或下载项目

```bash
# 如果是git仓库
git clone <repository-url>
cd python-learning-assistant

# 或者直接下载解压后进入目录
cd python-learning-assistant
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt

# 或者直接安装项目
pip install -e .
```

### 4. 设置环境变量

```bash
# Windows
set MOONSHOT_API_KEY=your_api_key_here

# Linux/Mac
export MOONSHOT_API_KEY=your_api_key_here
```

### 5. 运行应用

```bash
# 使用启动脚本
python run.py

# 或者直接运行主程序
python src/main.py

# 如果已安装为包
python-learning-assistant
```

## 验证安装

运行测试脚本验证安装是否成功：

```bash
python test.py
```

## 故障排除

### 依赖问题

如果遇到依赖安装问题：

```bash
# 升级pip
python -m pip install --upgrade pip

# 强制重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 权限问题

如果遇到权限问题：

```bash
# 使用用户级安装
pip install --user -e .
```

### Python版本

确保使用Python 3.7或更高版本：

```bash
python --version
```

## 卸载

如果需要卸载：

```bash
# 如果使用pip安装
pip uninstall python-learning-assistant

# 如果使用开发模式安装
pip uninstall python-learning-assistant
```

## 开发者安装

对于开发者，推荐使用开发模式安装：

```bash
# 安装开发依赖
pip install -e .[dev]

# 或者
pip install -e .
pip install pytest flake8 black
```

这样可以直接修改源码并立即生效，无需重新安装。