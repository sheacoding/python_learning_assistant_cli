# 配置说明

## 配置文件位置

配置文件位于 `config/config.json`

## 配置选项

### 基本配置

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

### 详细说明

#### `model`
- **类型**: 字符串
- **默认值**: `"kimi-k2-0711-preview"`
- **说明**: 使用的AI模型名称

#### `temperature`
- **类型**: 浮点数
- **范围**: 0.0 - 2.0
- **默认值**: `0.3`
- **说明**: 控制回答的随机性，值越低越确定

#### `max_tokens`
- **类型**: 整数
- **默认值**: `2048`
- **说明**: AI回答的最大token数量

#### `max_history`
- **类型**: 整数
- **默认值**: `50`
- **说明**: 保留的最大对话历史条数

#### `code_timeout`
- **类型**: 整数
- **默认值**: `10`
- **说明**: 代码执行超时时间（秒）

#### `auto_save_sessions`
- **类型**: 布尔值
- **默认值**: `true`
- **说明**: 是否自动保存会话

### 高级配置

#### 自定义系统提示词

```json
{
  "system_prompt": "你是一个专业的Python编程学习助手..."
}
```

你可以自定义系统提示词来调整AI助手的行为风格。

#### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `MOONSHOT_API_KEY` | Moonshot API密钥 | 是 |

### 配置示例

#### 初学者配置
```json
{
  "model": "kimi-k2-0711-preview",
  "temperature": 0.1,
  "max_tokens": 1500,
  "max_history": 30,
  "code_timeout": 15,
  "auto_save_sessions": true,
  "system_prompt": "你是一个耐心的Python编程学习助手，专门帮助初学者学习Python。请使用简单易懂的语言，提供详细的解释和基础的代码示例。"
}
```

#### 高级用户配置
```json
{
  "model": "kimi-k2-0711-preview",
  "temperature": 0.5,
  "max_tokens": 3000,
  "max_history": 100,
  "code_timeout": 30,
  "auto_save_sessions": true,
  "system_prompt": "你是一个专业的Python编程助手，可以讨论高级主题和最佳实践。提供深入的技术解释和复杂的代码示例。"
}
```

#### 快速响应配置
```json
{
  "model": "kimi-k2-0711-preview",
  "temperature": 0.3,
  "max_tokens": 1000,
  "max_history": 20,
  "code_timeout": 5,
  "auto_save_sessions": false,
  "system_prompt": "提供简洁明了的Python编程回答，重点突出关键信息。"
}
```

## 配置文件管理

### 备份配置
建议定期备份配置文件：
```bash
cp config/config.json config/config.json.backup
```

### 重置配置
如果配置文件损坏，删除它后程序会使用默认配置：
```bash
rm config/config.json
```

### 验证配置
程序启动时会自动验证配置文件，如果有错误会显示警告信息并使用默认值。

## 故障排除

### 配置文件格式错误
- **问题**: JSON格式不正确
- **解决**: 使用JSON验证工具检查语法
- **工具**: [JSONLint](https://jsonlint.com/)

### 参数值无效
- **问题**: 参数值超出有效范围
- **解决**: 参考上述说明调整参数值

### 权限问题
- **问题**: 无法读取配置文件
- **解决**: 检查文件权限，确保可读

## 最佳实践

1. **渐进调整**: 一次只修改一个参数
2. **测试验证**: 修改后测试功能是否正常
3. **备份配置**: 修改前备份原配置
4. **文档记录**: 记录修改原因和效果