#!/usr/bin/env python3
"""
Dynamic README Generator
Generates GitHub profile README from analytics data
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def load_analytics_data() -> Dict[str, Any]:
    """Load analytics data from JSON file"""
    try:
        with open('analytics_history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: analytics_history.json not found")
        return {}

def format_number(num: int) -> str:
    """Format large numbers with commas"""
    return f"{num:,}"

def generate_stats_badges(data: Dict[str, Any]) -> str:
    """Generate dynamic stats badges"""
    if not data or 'global_summary' not in data:
        return ""
    
    summary = data['global_summary']
    
    badges = []
    if 'total_lines' in summary:
        badges.append(f'<img src="https://img.shields.io/badge/📈_Total_Lines_of_Code-{format_number(summary["total_lines"])}-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Total Lines of Code" />')
    
    if 'total_commits' in summary:
        badges.append(f'<img src="https://img.shields.io/badge/📝_Total_Commits-{format_number(summary["total_commits"])}-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />')
    
    if 'total_files' in summary:
        badges.append(f'<img src="https://img.shields.io/badge/📁_Total_Files-{format_number(summary["total_files"])}-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />')
    
    return '\n  '.join(badges)

def generate_repository_table(data: Dict[str, Any]) -> str:
    """Generate repository breakdown table"""
    if not data or 'repository_breakdown' not in data:
        return ""
    
    table_rows = []
    table_rows.append("| Repository | Lines | Commits | Files | Distribution % |")
    table_rows.append("|:-----------|------:|--------:|------:|:---------------|")
    
    # Add unified total
    if 'unified_total' in data:
        unified = data['unified_total']
        table_rows.append(f"| **🌟 TOTAL UNIFIED** | **{format_number(unified.get('lines', 0))}** | **{format_number(unified.get('commits', 0))}** | **{format_number(unified.get('files', 0))}** | **{unified.get('distribution', '0/0/0')}** |")
    
    # Add individual repositories
    for repo in data.get('repository_breakdown', []):
        name = repo.get('name', 'Unknown')
        lines = format_number(repo.get('lines', 0))
        commits = format_number(repo.get('commits', 0))
        files = format_number(repo.get('files', 0))
        distribution = repo.get('distribution', '0/0/0')
        
        table_rows.append(f"| 📁 **{name}** | {lines} | {commits} | {files} | {distribution} |")
    
    return '\n'.join(table_rows)

def generate_language_table(data: Dict[str, Any]) -> str:
    """Generate language usage table"""
    if not data or 'language_breakdown' not in data:
        return ""
    
    languages = data['language_breakdown']
    if not languages:
        return ""
    
    table_rows = []
    table_rows.append("| Rank | Language | Lines | % of Total |")
    table_rows.append("|:-----|:---------|------:|:-----------|")
    
    # Language emojis
    lang_emojis = {
        'TypeScript': '🔷',
        'JavaScript': '🟨',
        'Python': '🐍',
        'CSS': '🎨',
        'HTML': '🌐',
        'JSON': '📄',
        'YAML': '⚙️',
        'Markdown': '📚',
        'Shell': '🐚',
        'Dockerfile': '🐳'
    }
    
    for i, lang in enumerate(languages[:10], 1):  # Top 10 languages
        name = lang.get('name', 'Unknown')
        lines = format_number(lang.get('lines', 0))
        percentage = lang.get('percentage', 0)
        emoji = lang_emojis.get(name, '📄')
        
        table_rows.append(f"| {i} | {emoji} **{name}** | {lines} | {percentage:.1f}% |")
    
    return '\n'.join(table_rows)

def generate_readme_content(data: Dict[str, Any]) -> str:
    """Generate complete README content"""
    
    # Header
    content = """# 👋 Hi, I'm Guillermo

## 📊 **My Coding Journey**

> 📊 **Unified stats from my private enterprise repositories**  
> _Updated automatically every Monday via GitHub Actions_

<!-- Unified Stats Overview -->
<div align="center">
"""
    
    # Add dynamic stats badges
    stats_badges = generate_stats_badges(data)
    if stats_badges:
        content += f"  {stats_badges}\n"
    
    content += """</div>

<!-- Repository Breakdown -->
<details>
<summary>📊 <strong>Repository Breakdown</strong></summary>
<br>

"""
    
    # Add repository table
    repo_table = generate_repository_table(data)
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
    if data and 'language_summary' in data:
        summary = data['language_summary']
        total_languages = summary.get('total_languages', 0)
        total_lines = format_number(summary.get('total_lines', 0))
        content += f"**📊 Summary:** {total_languages} languages detected across {total_lines} lines of code\n\n"
    
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
    
    return content

def main():
    """Main function to generate README"""
    print("🔄 Generating dynamic README from analytics data...")
    
    # Load analytics data
    data = load_analytics_data()
    
    # Generate README content
    content = generate_readme_content(data)
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md generated successfully!")
    print(f"📊 Data source: analytics_history.json")
    print(f"📅 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

if __name__ == "__main__":
    main() 