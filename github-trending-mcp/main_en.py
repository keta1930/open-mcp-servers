#!/usr/bin/env python3
"""
GitHub Trending MCP Server

A specialized MCP server for analyzing trending projects on GitHub.
This server helps AI assistants to discover, analyze and understand trending
GitHub projects and their implementations.

Usage flow:
1. First call get_github_trending to discover trending repositories (with optional time range and language)
2. Then call get_repository_readme to get detailed documentation of selected repos
3. Analyze and summarize the project implementations and approaches
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List
from datetime import datetime
from fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("GitHub Trending Analyzer")


@mcp.tool()
def get_github_trending(since: str = "daily", language: str = "") -> str:
    """
    Get GitHub trending repositories

    This tool scrapes the GitHub trending page and extracts detailed information
    about trending projects.

    Parameters:
    - since: Time range, options are "daily", "weekly", "monthly", default is "daily"
    - language: Programming language filter, e.g. "python", "javascript", "go", default is empty (all languages)

    Returns information including project names, descriptions, programming languages,
    star counts, and growth.
    """
    # Validate time range parameter
    valid_since = ["daily", "weekly", "monthly"]
    if since not in valid_since:
        return f"❌ Error: since parameter must be one of: {', '.join(valid_since)}"

    # Build URL
    if language:
        url = f"https://github.com/trending/{language.lower()}?since={since}"
    else:
        url = f"https://github.com/trending?since={since}"

    try:
        # Get current date information
        current_date = datetime.now()
        date_str = current_date.strftime("%Y-%m-%d")
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_str = weekday_names[current_date.weekday()]

        # Time range display
        since_display = {"daily": "Today", "weekly": "This Week", "monthly": "This Month"}

        # Simple requests call
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', class_='Box-row')

        if not articles:
            return f"❌ No trending projects found, possible page structure change or network issue\nRequested URL: {url}"

        result = []
        result.append(f"🌟 GitHub Trending Repositories")
        result.append(f"📅 Retrieved on: {date_str} {weekday_str}")
        result.append(f"⏰ Time Range: {since_display.get(since, since)}")
        if language:
            result.append(f"💻 Language: {language}")
        result.append(f"📊 Found {len(articles)} trending projects")
        result.append("")

        for i, article in enumerate(articles, 1):
            try:
                # Extract title
                title_elem = article.find('h2', class_='h3')
                if not title_elem:
                    continue

                title_link = title_elem.find('a')
                if not title_link:
                    continue

                title = ' '.join(title_link.get_text(strip=True).split())
                project_url = "https://github.com" + title_link.get('href', '')

                # Extract description
                description_elem = article.find('p', class_='col-9')
                description = description_elem.get_text(strip=True) if description_elem else "No description"

                # Extract programming language
                language_elem = article.find('span', {'itemprop': 'programmingLanguage'})
                project_language = language_elem.get_text(strip=True) if language_elem else "Unknown"

                # Extract total stars
                star_link = article.find('a', href=re.compile(r'/stargazers$'))
                total_stars = star_link.get_text(strip=True) if star_link else "0"

                # Extract fork count
                fork_link = article.find('a', href=re.compile(r'/forks$'))
                total_forks = fork_link.get_text(strip=True) if fork_link else "0"

                # Extract period stars
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
                    f"   💻 Language: {project_language} | ⭐ Total Stars: {total_stars} | 🍴 Forks: {total_forks} | 🔥 {since_display.get(since, since)}: +{period_stars}")

            except Exception as e:
                result.append(f"❌ Error parsing project {i}: {str(e)}")
                continue

        result.append("")
        result.append("💡 Suggested next steps:")
        result.append("1. Analyze GitHub trending project trends")
        result.append(
            "2. If interested in specific projects, use get_repository_readme tool to get detailed documentation")

        return "\n".join(result)

    except requests.exceptions.RequestException as e:
        return f"❌ Network request error: {str(e)}\nRequested URL: {url}\nSuggest checking network connection or retry later"
    except Exception as e:
        return f"❌ Program execution error: {str(e)}\nRequested URL: {url}"


@mcp.tool()
def get_repository_readme(repositories: List[str]) -> str:
    """
    Get README documentation content for specified GitHub repositories

    This tool is used to fetch detailed documentation for GitHub repositories.

    Parameters:
    - repositories: List of repository names in format ["owner/repo-name"]
    """
    if not repositories:
        return "❌ Error: repositories parameter cannot be empty, please provide at least one repository name"

    results = []
    results.append("📚 GitHub Repository README Documents")

    for repo in repositories:
        try:
            # Clean repository name
            repo = repo.strip()
            if not repo:
                continue

            # Validate repository name format
            if '/' not in repo:
                results.append(f"❌ Invalid repository name format: {repo}")
                results.append("   Correct format should be: owner/repository-name")
                results.append("---")
                results.append("")
                continue

            # Try different branches and file names
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
                # Limit content length to avoid excessive length
                if len(readme_content) > 50000:  # 50KB limit
                    readme_content = readme_content[:50000] + "\n\n... [Content too long, truncated] ..."

                results.append(f"✅ Successfully retrieved (Source: {found_url})")
                results.append(f"Repository: {repo}")
                results.append("README:")
                results.append(readme_content)
                results.append("---\n\n")
            else:
                results.append(f"❌ README file not found")
                results.append(f"   Tried branches: {', '.join(branches)}")
                results.append(f"   Tried files: {', '.join(readme_files)}")
                results.append(f"Repository: {repo}")
                results.append("README: No readable README file found")
                results.append("---\n\n")

        except Exception as e:
            results.append(f"❌ Error processing repository {repo}: {str(e)}")
            results.append(f"Repository: {repo}")
            results.append(f"README: Failed to retrieve - {str(e)}")
            results.append("---")

    results.append("💡 Suggested next steps:")
    results.append("- 1. Analyze detailed information and technical features of each project")
    results.append("- 2. If particularly interested in a project, further study its implementation details")
    results.append("- 3. Summarize technical highlights and application scenarios of the projects")

    return "\n".join(results)


if __name__ == "__main__":
    # Run MCP server
    mcp.run()