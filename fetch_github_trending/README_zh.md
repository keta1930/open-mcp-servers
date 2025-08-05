# GitHub Trending MCP Server

一个专门用于分析GitHub上热门项目的MCP服务器。此服务器帮助AI助手发现、分析和理解GitHub上的热门项目及其实现。

## 功能特性

- 🌟 获取GitHub热门项目列表（支持日/周/月时间范围）
- 🔍 支持按编程语言过滤项目
- 📚 获取指定仓库的README文档内容
- 📊 提取项目详细信息（星数、Fork数、编程语言等）

## 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd github-trending-mcp
   ```

2. **安装依赖**
   ```bash
   # 使用uv安装依赖
   uv sync
   
   # 或安装所需包
   uv add requests beautifulsoup4 fastmcp
   ```

## MCP配置

**配置示例：**
```json
{
  "mcpServers": {
    "github_trending": {
      "command": "/path/to/your/project/.venv/Scripts/python.exe",
      "args": [
        "/path/to/your/project/main_zh.py"
      ]
    }
  }
}
```

## 工具说明

### get_github_trending(since, language)
获取GitHub热门项目列表

**参数：**
- `since` (可选): 时间范围
  - `"daily"` - 今日热门（默认）
  - `"weekly"` - 本周热门
  - `"monthly"` - 本月热门
- `language` (可选): 编程语言过滤，例如 `"python"`、`"javascript"`、`"go"` 等，默认为空（所有语言）

**使用示例：**
```
# 获取今日所有语言的热门项目
请获取今日GitHub热门项目

# 获取本周Python项目
请获取本周GitHub热门的Python项目

# 获取本月JavaScript项目
请获取本月GitHub热门的JavaScript项目
```

**返回信息：**
- 项目名称和GitHub链接
- 项目描述
- 编程语言
- 总星数和Fork数
- 时间段内的星数增长

### get_repository_readme(repositories)
获取指定GitHub仓库的README文档内容

**参数：**
- `repositories`: 仓库名称列表，格式为 `["owner/repo-name"]`

**使用示例：**
```
请获取以下仓库的README文档：microsoft/markitdown, openai/gpt-4
```

**返回信息：**
- 完整的README文档内容
- 内容超过50KB时自动截断
- 支持多种README文件格式（.md, .txt等）