#!/usr/bin/env python3
"""
Dynamic README Generator
Generates GitHub profile README from analytics data
"""

import json
from typing import Any

from error_handling import (
    DataProcessingError,
    get_logger,
    log_and_raise,
    with_error_context,
)

# Set up logging for this module
logger = get_logger(__name__)


def load_analytics_data() -> dict[str, Any]:
    """Load analytics data from JSON file."""
    try:
        with open("analytics_history.json", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug("Loading analytics data from analytics_history.json")
        if isinstance(data, dict):
            return data
        else:
            logger.error("Analytics data is not a dictionary")
            return {}
    except (FileNotFoundError, PermissionError) as e:
        logger.warning(f"Could not read analytics_history.json: {e}")
        return {}
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in analytics_history.json: {e}")
        return {}
    except OSError as e:
        logger.error(f"IO error reading analytics_history.json: {e}")
        return {}


def format_number(num: int) -> str:
    """Format large numbers with commas"""
    try:
        return f"{num:,}"
    except (ValueError, TypeError) as e:
        logger.warning(f"Error formatting number {num}: {e}")
        return str(num)


def generate_badges(global_summary: dict[str, Any]) -> list[str]:
    """Generate badges for the README."""
    badges = []

    try:
        total_lines = global_summary.get("total_loc", 0)
        total_commits = global_summary.get("total_commits", 0)
        total_files = global_summary.get("total_files", 0)

        if total_lines > 0:
            badges.append(
                f'<img src="https://img.shields.io/badge/📈_Total_Lines_of_Code-{format_number(total_lines)}-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Total Lines of Code" />'
            )
            logger.debug(f"Added total lines badge: {format_number(total_lines)}")

        if total_commits > 0:
            badges.append(
                f'<img src="https://img.shields.io/badge/📝_Total_Commits-{format_number(total_commits)}-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />'
            )
            logger.debug(f"Added total commits badge: {format_number(total_commits)}")

        if total_files > 0:
            badges.append(
                f'<img src="https://img.shields.io/badge/📁_Total_Files-{format_number(total_files)}-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />'
            )
            logger.debug(f"Added total files badge: {format_number(total_files)}")

    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error generating badges: {e}")

    return badges


def generate_repository_breakdown(repo_breakdown: dict[str, Any]) -> str:
    """Generate repository breakdown section."""
    try:
        if not repo_breakdown:
            logger.debug("No repository breakdown data available")
            return ""

        breakdown_lines = []
        breakdown_lines.append("### 📊 Repository Breakdown\n")

        for repo_name, repo_data in repo_breakdown.items():
            try:
                lines = repo_data.get("repo_totals", {}).get("loc", 0)
                commits = repo_data.get("repo_totals", {}).get("commits", 0)
                files = repo_data.get("repo_totals", {}).get("files", 0)

                breakdown_lines.append(
                    f"**{repo_name}**: {format_number(lines)} lines, {format_number(commits)} commits, {format_number(files)} files"
                )
                logger.debug(
                    f"Added unified total row: {lines} lines, {commits} commits, {files} files"
                )

            except (TypeError, AttributeError, KeyError) as e:
                logger.warning(f"Error processing repository {repo_name}: {e}")
                continue

        return "\n".join(breakdown_lines)

    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error generating repository breakdown: {e}")
        return ""


def generate_language_table(data: dict[str, Any]) -> str:
    """Generate language usage table"""

    try:
        if not data or "language_breakdown" not in data:
            logger.debug("No language breakdown data available")
            return ""

        languages = data["language_breakdown"]
        if not languages:
            logger.debug("Empty language breakdown data")
            return ""

        table_rows = []
        table_rows.append("| Rank | Language | Lines | % of Total |")
        table_rows.append("|:-----|:---------|------:|:-----------|")

        # Language emojis
        lang_emojis = {
            "TypeScript": "🔷",
            "JavaScript": "🟨",
            "Python": "🐍",
            "CSS": "🎨",
            "HTML": "🌐",
            "JSON": "📄",
            "YAML": "⚙️",
            "Markdown": "📚",
            "Shell": "🐚",
            "Dockerfile": "🐳",
        }

        processed_languages = 0
        for i, lang in enumerate(languages[:10], 1):  # Top 10 languages
            try:
                name = lang.get("name", "Unknown")
                lines = format_number(lang.get("lines", 0))
                percentage = lang.get("percentage", 0)
                emoji = lang_emojis.get(name, "📄")

                table_rows.append(
                    f"| {i} | {emoji} **{name}** | {lines} | {percentage:.1f}% |"
                )
                processed_languages += 1

            except (TypeError, AttributeError, KeyError, ValueError) as e:
                logger.error(
                    f"Error processing language {lang.get('name', 'Unknown')}: {e}"
                )
                continue

        logger.info(f"Generated language table with {processed_languages} languages")
        return "\n".join(table_rows)

    except (TypeError, AttributeError, KeyError, ValueError) as e:
        logger.error(f"Error generating language table: {e}", exc_info=True)
        return ""


def generate_readme_content(data: dict[str, Any]) -> str:
    """Generate complete README content"""

    try:
        logger.info("Starting README content generation")

        # Header
        content = """# 👋 Hi, I'm Guillermo

## 📊 **My Coding Journey**

> 📊 **Unified stats from my private enterprise repositories**
> _Updated automatically every Monday via GitHub Actions_

<!-- Unified Stats Overview -->
<div align="center">
"""

        # Add dynamic stats badges
        stats_badges = generate_badges(data.get("global_summary", {}))
        if stats_badges:
            content += f"  {stats_badges}\n"

        content += """</div>

<!-- Repository Breakdown -->
<details>
<summary>📊 <strong>Repository Breakdown</strong></summary>
<br>

"""

        # Add repository table
        repo_table = generate_repository_breakdown(data.get("repository_breakdown", {}))
        if repo_table:
            content += repo_table + "\n"

        content += """
</details>

<!-- Language Breakdown -->
<details>
<summary>🔤 <strong>Language Usage Analysis</strong></summary>
<br>

"""

        # Add language summary
        if data and "language_summary" in data:
            summary = data["language_summary"]
            total_languages = summary.get("total_languages", 0)
            total_lines = format_number(summary.get("total_lines", 0))
            content += f"**📊 Summary:** {total_languages} languages detected across {total_lines} lines of code\n\n"
            logger.debug(
                f"Added language summary: {total_languages} languages, {total_lines} lines"
            )

        # Add language table
        lang_table = generate_language_table(data)
        if lang_table:
            content += lang_table + "\n"

        content += """
</details>

<!-- GitHub Stats for Public Activity -->
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=GuillermoAstorgaCalvo&show_icons=true&theme=radical&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E&icon_color=58A6FF)

<!-- Contribution Graph -->
![GitHub Streak](https://streak-stats.demolab.com/?user=GuillermoAstorgaCalvo&theme=radical&hide_border=true&background=0D1117&stroke=58A6FF&ring=58A6FF&fire=58A6FF&currStreakNum=8B949E&sideNums=8B949E&currStreakLabel=8B949E&sideLabels=8B949E&dates=8B949E)

## 🛠️ **Tech Stack**

### **Languages & Frameworks**
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/-Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)

### **Tools & Technologies**
![Git](https://img.shields.io/badge/-Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

## 📈 **GitHub Stats**

<!-- Repository Stats -->
![Repository Stats](https://github-readme-stats.vercel.app/api?username=GuillermoAstorgaCalvo&show_icons=true&theme=radical&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E&icon_color=58A6FF&include_all_commits=true&count_private=true)

<!-- Weekly Stats -->
![Weekly Stats](https://github-readme-stats.vercel.app/api/wakatime?username=GuillermoAstorgaCalvo&theme=radical&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E)

## 🚀 **Featured Projects**

### **FacturaIA** - AI-Powered Invoice Management
![FacturaIA](https://img.shields.io/badge/-FacturaIA-FF6B6B?style=for-the-badge&logo=github&logoColor=white)
> AI-driven invoice processing and management system with automated data extraction and analysis.

### **Restaurant App** - Full-Stack Restaurant Management
![Restaurant App](https://img.shields.io/badge/-Restaurant%20App-4ECDC4?style=for-the-badge&logo=github&logoColor=white)
> Complete restaurant management solution with ordering, inventory, and analytics.

### **Analytics Dashboard** - Multi-Repository Analytics
![Analytics Dashboard](https://img.shields.io/badge/-Analytics%20Dashboard-45B7D1?style=for-the-badge&logo=github&logoColor=white)
> Comprehensive analytics platform for tracking coding metrics across multiple repositories.

## 📊 **Coding Analytics**

<!-- Dynamic Analytics Section -->
<div align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=GuillermoAstorgaCalvo&theme=react-dark&hide_border=true&bg_color=0D1117&color=58A6FF&line=58A6FF&point=58A6FF" alt="Activity Graph" />
</div>

## 🌟 **Let's Connect**

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/guillermoastorgacalvo)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GuillermoAstorgaCalvo)
[![Email](https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:guillermo.astorga.calvo@gmail.com)
[![Portfolio](https://img.shields.io/badge/-Portfolio-FF6B6B?style=for-the-badge&logo=github&logoColor=white)](https://guillermoastorgacalvo.dev)

---

<div align="center">
  <img src="https://komarev.com/ghpvc/?username=GuillermoAstorgaCalvo&style=flat-square&color=58A6FF" alt="Profile Views" />
</div>
"""

        logger.info("Successfully generated README content")
        return content

    except (TypeError, AttributeError, KeyError, ValueError, OSError) as e:
        log_and_raise(
            DataProcessingError,
            f"Error generating README content: {e}",
            error_code="CONTENT_GENERATION_ERROR",
        )
        return ""


@with_error_context({"component": "generate_readme"})
def main() -> None:
    """Main function to generate README"""

    try:
        logger.info("Starting README generation process")

        # Load analytics data
        data = load_analytics_data()

        # Generate README content
        content = generate_readme_content(data)

        # Write to README.md
        logger.info("Writing README content to README.md")
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("README.md successfully generated")

    except DataProcessingError as e:
        logger.error(f"README generation failed: {e}")
        raise
    except FileNotFoundError as e:
        log_and_raise(
            DataProcessingError,
            f"Output file path not found: {e}",
            error_code="OUTPUT_PATH_ERROR",
        )
    except PermissionError as e:
        log_and_raise(
            DataProcessingError,
            f"Permission denied writing README.md: {e}",
            error_code="PERMISSION_DENIED",
        )
    except (TypeError, AttributeError, KeyError, ValueError, OSError) as e:
        log_and_raise(
            DataProcessingError,
            f"Unexpected error in README generation: {e}",
            error_code="UNEXPECTED_ERROR",
        )


if __name__ == "__main__":
    try:
        main()
    except DataProcessingError as e:
        logger.error(f"README generation failed: {e}")
        exit(1)
    except (TypeError, AttributeError, KeyError, ValueError, OSError) as e:
        logger.error(f"Unexpected error in README generation: {e}", exc_info=True)
        exit(1)
