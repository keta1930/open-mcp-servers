#!/usr/bin/env python3
"""
GitHub Trending MCP Server

一个专门用于分析GitHub上热门项目的MCP服务器。
此服务器帮助AI助手发现、分析和理解GitHub上的热门项目及其实现。

使用流程：
1. 首先调用 get_github_trending 来发现热门仓库（可指定时间范围和编程语言）
2. 然后调用 get_repository_readme 来获取选定仓库的详细文档
3. 分析和总结项目的实现和方法
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List
from datetime import datetime
from fastmcp import FastMCP

# 创建MCP server实例
mcp = FastMCP("GitHub Trending Analyzer")


@mcp.tool()
def get_github_trending(since: str = "daily", language: str = "") -> str:
    """
    获取GitHub trending榜单

    此工具爬取GitHub trending页面，提取趋势项目的详细信息。

    参数说明：
    - since: 时间范围，可选值为 "daily"（日）、"weekly"（周）、"monthly"（月），默认为 "daily"
    - language: 编程语言过滤，例如 "python"、"javascript"、"go" 等，默认为空（所有语言）

    返回结果包含项目名称、描述、编程语言、星数、增长等信息。
    """
    # 验证时间范围参数
    valid_since = ["daily", "weekly", "monthly"]
    if since not in valid_since:
        return f"❌ 错误：since参数必须是以下值之一: {', '.join(valid_since)}"

    # 构建URL
    if language:
        url = f"https://github.com/trending/{language.lower()}?since={since}"
    else:
        url = f"https://github.com/trending?since={since}"

    try:
        # 获取当前日期信息
        current_date = datetime.now()
        date_str = current_date.strftime("%Y年%m月%d日")
        weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday_str = weekday_names[current_date.weekday()]

        # 时间范围显示
        since_display = {"daily": "今日", "weekly": "本周", "monthly": "本月"}

        # 简单的requests请求
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', class_='Box-row')

        if not articles:
            return f"❌ 未找到任何trending项目，可能页面结构已更改或网络问题\n请求URL: {url}"

        result = []
        result.append(f"🌟 GitHub Trending Repositories")
        result.append(f"📅 获取时间: {date_str} {weekday_str}")
        result.append(f"⏰ 时间范围: {since_display.get(since, since)}")
        if language:
            result.append(f"💻 编程语言: {language}")
        result.append(f"📊 共发现 {len(articles)} 个热门项目")
        result.append("")

        for i, article in enumerate(articles, 1):
            try:
                # 提取标题
                title_elem = article.find('h2', class_='h3')
                if not title_elem:
                    continue

                title_link = title_elem.find('a')
                if not title_link:
                    continue

                title = ' '.join(title_link.get_text(strip=True).split())
                project_url = "https://github.com" + title_link.get('href', '')

                # 提取简介
                description_elem = article.find('p', class_='col-9')
                description = description_elem.get_text(strip=True) if description_elem else "无描述"

                # 提取编程语言
                language_elem = article.find('span', {'itemprop': 'programmingLanguage'})
                project_language = language_elem.get_text(strip=True) if language_elem else "未知"

                # 提取总星标数量
                star_link = article.find('a', href=re.compile(r'/stargazers$'))
                total_stars = star_link.get_text(strip=True) if star_link else "0"

                # 提取fork数量
                fork_link = article.find('a', href=re.compile(r'/forks$'))
                total_forks = fork_link.get_text(strip=True) if fork_link else "0"

                # 提取时间段内的星标数量
                period_stars = "0"
                spans = article.find_all('span')
                for span in spans:
                    span_text = span.get_text(strip=True)
                    if 'stars' in span_text.lower() and (
                            'today' in span_text.lower() or 'this week' in span_text.lower() or 'this month' in span_text.lower()):
                        period_match = re.search(r'(\d+[,\d]*)\s*stars?', span_text, re.IGNORECASE)
                        if period_match:
                            period_stars = period_match.group(1)
                        break

                result.append(f"{i}. {title}")
                result.append(f"   🔗 {project_url}")
                result.append(f"   📝 {description}")
                result.append(
                    f"   💻 语言: {project_language} | ⭐ 总星数: {total_stars} | 🍴 Forks: {total_forks} | 🔥 {since_display.get(since, since)}: +{period_stars}")

            except Exception as e:
                result.append(f"❌ 解析第 {i} 个项目时出错: {str(e)}")
                continue

        result.append("")
        result.append("💡 建议下一步操作：")
        result.append("1. 分析GitHub热门项目趋势")
        result.append("2. 如有特别关注的项目，可使用 get_repository_readme 工具获取该项目详细文档")

        return "\n".join(result)

    except requests.exceptions.RequestException as e:
        return f"❌ 网络请求错误: {str(e)}\n请求URL: {url}\n建议检查网络连接或稍后重试"
    except Exception as e:
        return f"❌ 程序执行错误: {str(e)}\n请求URL: {url}"


@mcp.tool()
def get_repository_readme(repositories: List[str]) -> str:
    """
    获取指定GitHub仓库的README文档内容

    此工具用于获取GitHub仓库的详细文档。

    参数说明：
    - repositories: 仓库名称列表，格式为 ["owner/repo-name"]
    """
    if not repositories:
        return "❌ 错误：repositories参数不能为空，请提供至少一个仓库名称"

    results = []
    results.append("📚 GitHub Repository README Documents")

    for repo in repositories:
        try:
            # 清理仓库名称
            repo = repo.strip()
            if not repo:
                continue

            # 验证仓库名称格式
            if '/' not in repo:
                results.append(f"❌ 仓库名称格式错误: {repo}")
                results.append("   正确格式应为: owner/repository-name")
                results.append("---")
                results.append("")
                continue

            # 尝试不同的分支和文件名
            branches = ['main', 'master']
            readme_files = ['README.md', 'readme.md', 'Readme.md', 'README.txt', 'readme.txt']

            readme_content = None
            found_url = None

            for branch in branches:
                for readme_file in readme_files:
                    url = f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch}/{readme_file}"
                    try:
                        response = requests.get(url, timeout=20)
                        if response.status_code == 200:
                            readme_content = response.text
                            found_url = url
                            break
                    except:
                        continue
                if readme_content:
                    break

            if readme_content:
                # 限制内容长度，避免过长
                if len(readme_content) > 50000:  # 50KB限制
                    readme_content = readme_content[:50000] + "\n\n... [内容过长，已截断] ..."

                results.append(f"✅ 成功获取 (来源: {found_url})")
                results.append(f"仓库名称: {repo}")
                results.append("README:")
                results.append(readme_content)
                results.append("---\n\n")
            else:
                results.append(f"❌ 未找到README文件")
                results.append(f"   已尝试分支: {', '.join(branches)}")
                results.append(f"   已尝试文件: {', '.join(readme_files)}")
                results.append(f"仓库名称: {repo}")
                results.append("README: 未找到可读取的README文件")
                results.append("---\n\n")

        except Exception as e:
            results.append(f"❌ 处理仓库 {repo} 时出错: {str(e)}")
            results.append(f"仓库名称: {repo}")
            results.append(f"README: 获取失败 - {str(e)}")
            results.append("---")

    results.append("💡 建议下一步操作：")
    results.append("- 1. 分析每个项目的详细信息和技术特点")
    results.append("- 2. 如果有特别感兴趣的项目，可以进一步研究其实现细节")
    results.append("- 3. 总结项目的技术亮点和应用场景")

    return "\n".join(results)


if __name__ == "__main__":
    # 运行MCP server
    mcp.run()