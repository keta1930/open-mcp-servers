# GitHub Trending MCP Server

A specialized MCP server for analyzing trending projects on GitHub. This server helps AI assistants discover, analyze, and understand trending projects on GitHub along with their implementations.

## (1) Features

- 🌟 Retrieve GitHub trending project lists (supports time range/programming language filtering)
- 📚 Get README documentation content for specified repositories

## (2) Tool Documentation

### get_github_trending(since, language)
Retrieve GitHub trending project list

**Parameters:**
- `since` (optional): Time range
  - `"daily"` - Today's trending (default)
  - `"weekly"` - This week's trending
  - `"monthly"` - This month's trending
- `language` (optional): Programming language filter, e.g., `"python"`, `"javascript"`, `"go"`, etc. Default is empty (all languages)

**Usage Examples:**
```
Please get today's GitHub trending projects

Please get this week's trending Python projects on GitHub

Please get this month's trending JavaScript projects on GitHub
```

**Return Information:**
- Project name and GitHub link
- Project description
- Programming language
- Total stars and forks
- Star growth within the time period

### get_repository_readme(repositories)
Get README documentation content for specified GitHub repositories

**Parameters:**
- `repositories`: List of repository names in format `["owner/repo-name"]`

**Usage Examples:**
```
Please get README documentation for the following repositories: microsoft/markitdown, openai/gpt-4
```

**Return Information:**
- Complete README documentation content
- Automatically truncated when content exceeds 50KB
- Supports multiple README file formats (.md, .txt, etc.)

## (3) Installation Steps

1. **Clone the project**
   ```bash
   git clone https://github.com/keta1930/open-mcp-servers.git
   cd github-trending-mcp
   ```

2. **Install dependencies**
   ```bash
   # Install dependencies using uv
   uv sync
   
   # Or install required packages
   uv add requests beautifulsoup4 fastmcp
   ```

## (4) MCP Configuration

**Configuration Example:**
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