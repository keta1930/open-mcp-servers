# GitHub Trending MCP Server

A specialized MCP server for analyzing trending projects on GitHub. This server helps AI assistants to discover, analyze and understand trending GitHub projects and their implementations.

## Features

- 🌟 Fetch GitHub trending project list (supports daily/weekly/monthly time ranges)
- 🔍 Filter projects by programming language
- 📚 Get README documentation content for specified repositories
- 📊 Extract detailed project information (stars, forks, programming languages, etc.)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd github-trending-mcp
   ```

2. **Install dependencies**
   ```bash
   # Using uv to install dependencies
   uv sync
   
   # Or install required packages
   uv add requests beautifulsoup4 fastmcp
   ```

## MCP Configuration

**Configuration Example:**
```json
{
  "mcpServers": {
    "github_trending": {
      "command": "/path/to/your/project/.venv/Scripts/python.exe",
      "args": [
        "/path/to/your/project/main_en.py"
      ]
    }
  }
}
```

## Tool Documentation

### get_github_trending(since, language)
Get GitHub trending project list

**Parameters:**
- `since` (optional): Time range
  - `"daily"` - Today's trending (default)
  - `"weekly"` - This week's trending
  - `"monthly"` - This month's trending
- `language` (optional): Programming language filter, e.g. `"python"`, `"javascript"`, `"go"`, default is empty (all languages)

**Usage Examples:**
```
# Get today's trending projects for all languages
Please get today's GitHub trending projects

# Get this week's Python projects
Please get this week's GitHub trending Python projects

# Get this month's JavaScript projects
Please get this month's GitHub trending JavaScript projects
```

**Returns:**
- Project names and GitHub links
- Project descriptions
- Programming languages
- Total stars and fork counts
- Star growth within the time period

### get_repository_readme(repositories)
Get README documentation content for specified GitHub repositories

**Parameters:**
- `repositories`: List of repository names in format `["owner/repo-name"]`

**Usage Examples:**
```
Please get the README documentation for: microsoft/markitdown, openai/gpt-4
```

**Returns:**
- Complete README documentation content
- Automatic truncation when content exceeds 50KB
- Support for various README file formats (.md, .txt, etc.)