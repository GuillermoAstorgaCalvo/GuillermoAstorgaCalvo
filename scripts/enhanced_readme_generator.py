#!/usr/bin/env python3
"""
Professional Dynamic README Generator
Creates an authentic, human-written GitHub profile README
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from error_handling import (
    DataProcessingError,
    ErrorCodes,
    get_logger,
    log_and_raise,
    setup_logging,
    with_error_context,
)

# Set up logging for this module
logger = get_logger(__name__)


def load_unified_stats() -> dict[str, Any]:
    """Load unified statistics from JSON file."""
    try:
        # Try current directory first, then parent directory
        config_paths = ["unified_stats.json", "../unified_stats.json"]
        for path in config_paths:
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    logger.error("Unified stats data is not a dictionary")
                    return {}
        logger.warning("unified_stats.json not found in current or parent directory")
        return {}
    except (FileNotFoundError, PermissionError) as e:
        logger.warning(f"Could not read unified_stats.json: {e}")
        return {}
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in unified_stats.json: {e}")
        return {}
    except OSError as e:
        logger.error(f"IO error reading unified_stats.json: {e}")
        return {}


def load_analytics_history() -> list[dict[str, Any]]:
    """Load analytics history from JSON file."""
    try:
        # Try current directory first, then parent directory
        config_paths = ["analytics_history.json", "../analytics_history.json"]
        for path in config_paths:
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    logger.warning("analytics_history.json does not contain a list")
                    return []
        logger.warning(
            "analytics_history.json not found in current or parent directory"
        )
        return []

    except (FileNotFoundError, PermissionError) as e:
        logger.warning(f"Could not read analytics_history.json: {e}")
        return []
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in analytics_history.json: {e}")
        return []
    except OSError as e:
        logger.error(f"IO error reading analytics_history.json: {e}")
        return []


def load_analytics_data() -> dict[str, Any]:
    """Load analytics data from unified stats and analytics history."""
    try:
        # Load unified stats
        unified_stats = load_unified_stats()

        # Load analytics history
        analytics_history = load_analytics_history()

        # Combine the data
        data = {"unified_stats": unified_stats, "analytics_history": analytics_history}

        logger.info(
            f"Loaded analytics data: {len(unified_stats)} unified stats, {len(analytics_history)} history entries"
        )
        return data

    except Exception as e:
        logger.error(f"Error loading analytics data: {e}")
        # Return empty data structure to prevent crashes
        return {"unified_stats": {}, "analytics_history": []}


def save_readme(content: str, output_path: str = "../README.md") -> bool:
    """Save README content to file."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"README saved to {output_path}")
        return True

    except (PermissionError, OSError) as e:
        logger.error(f"Could not write to {output_path}: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Error writing README content: {e}")
        return False


def format_number(num: int) -> str:
    """Format large numbers with commas"""
    return f"{num:,}"


def get_project_descriptions() -> dict[str, dict[str, Any]]:
    """Get comprehensive project descriptions with authentic narratives"""
    # Load configuration to get project URLs
    try:
        from config_manager import create_config_manager

        config = create_config_manager(str(Path(__file__).parent.parent / "config.yml"))
        project_urls = config.get_project_urls()
    except Exception as e:
        logger.warning(f"Could not load project URLs from config: {e}")
        project_urls = {}

    return {
        "InmoIA Frontend": {
            "description": "A real estate platform that actually helps people find their perfect home. Started as a simple listing site and grew into something much bigger.",
            "tech_stack": ["React", "TypeScript", "TailwindCSS", "Next.js"],
            "features": [
                "AI Property Matching",
                "Virtual Tours",
                "Analytics Dashboard",
            ],
            "status": "🟢 Active Development",
            "url": project_urls.get(
                "inmoia_frontend",
                "https://github.com/guillermo-affiliaction/housing-hub-saas",
            ),
            "story": "This one started small - just a basic property listing. But as I worked on it, I kept thinking 'what if we could make this smarter?' Now it's a full SaaS platform. The journey from simple to complex taught me so much about scaling React apps.",
        },
        "TypeScript Backend": {
            "description": "The engine that powers everything. Built this microservices architecture to handle the heavy lifting - authentication, data processing, you name it.",
            "tech_stack": ["Node.js", "TypeScript", "PostgreSQL", "Docker"],
            "features": ["REST APIs", "Authentication", "Database Management"],
            "status": "🟢 Active Development",
            "url": project_urls.get(
                "typescript_backend",
                "https://github.com/guillermo-affiliaction/backend-housing-hub-saas",
            ),
            "story": "TypeScript changed everything for me. The first time I refactored this backend with proper types, I realized what I'd been missing. Now I can't imagine building anything complex without it.",
        },
        "Python AI MCP Backend": {
            "description": "This is where things get interesting. Built an AI backend that can understand what you're asking and actually do something about it.",
            "tech_stack": ["Python", "FastAPI", "OpenAI", "PostgreSQL"],
            "features": [
                "AI Task Completion",
                "Natural Language Processing",
                "MCP Integration",
            ],
            "status": "🟢 Active Development",
            "url": project_urls.get(
                "python_ai_backend",
                "https://github.com/guillermo-affiliaction/IAbackend-inmoIA",
            ),
            "story": "I was skeptical about AI at first, but seeing this system understand natural language requests blew my mind. It's like having a really smart assistant that actually gets things done.",
        },
        "FacturaIA": {
            "description": "Got tired of manually processing invoices, so I built something to do it for me. Sometimes the best projects come from solving your own problems.",
            "tech_stack": ["Python", "React", "TypeScript", "PostgreSQL"],
            "features": ["OCR Processing", "Data Extraction", "Invoice Management"],
            "status": "🟡 In Development",
            "url": project_urls.get(
                "facturaia", "https://github.com/GuillermoAstorgaCalvo/FacturaIA"
            ),
            "story": "This was born from pure frustration. I was manually processing invoices one day and thought 'there has to be a better way.' Turns out there was - I just had to build it.",
        },
        "Restaurant App": {
            "description": "My first full-stack project that actually went live. Built it for a friend's restaurant and it's still running today.",
            "tech_stack": ["React", "Node.js", "MongoDB", "Express.js"],
            "features": ["Order Management", "Menu System", "Admin Dashboard"],
            "status": "🟢 Live",
            "url": project_urls.get(
                "restaurant_app", "https://restauranteguillermoastorga.up.railway.app/"
            ),
            "story": "This was the project that made me realize I could actually build things people would use. Seeing real customers place orders through something I built was incredibly satisfying.",
        },
    }


def generate_hero_section() -> str:
    """Generate authentic hero section with personal touch"""
    # Load configuration for profile and animation settings
    try:
        from config_manager import create_config_manager

        config = create_config_manager(str(Path(__file__).parent.parent / "config.yml"))
        profile = config.get_profile_config()
        typing_animation = config.get_typing_animation_config()
        badge_colors = config.get_badge_colors()
    except Exception as e:
        logger.warning(f"Could not load configuration for hero section: {e}")
        # Fallback to default values
        profile = {
            "name": "Guillermo",
            "title": "Full-Stack Developer",
            "subtitle": "AI Enthusiast | Problem Solver | Code Craftsman",
            "description": "I build things. Sometimes they work, sometimes they don't, but I always learn something along the way.",
        }
        typing_animation = {
            "font": "Fira+Code",
            "weight": "500",
            "size": "28",
            "pause": "1000",
            "color": "58A6FF",
            "center": "true",
            "vCenter": "true",
            "width": "600",
            "height": "100",
            "lines": "Full-Stack+Developer;AI+Enthusiast;Problem+Solver;Code+Craftsman",
        }
        badge_colors = {"primary": "58A6FF", "secondary": "4ECDC4", "accent": "FF6B6B"}

    # Build typing animation URL
    typing_url = f"https://readme-typing-svg.herokuapp.com?font={typing_animation.get('font', 'Fira+Code')}&weight={typing_animation.get('weight', '500')}&size={typing_animation.get('size', '28')}&pause={typing_animation.get('pause', '1000')}&color={typing_animation.get('color', '58A6FF')}&center={typing_animation.get('center', 'true')}&vCenter={typing_animation.get('vCenter', 'true')}&width={typing_animation.get('width', '600')}&height={typing_animation.get('height', '100')}&lines={typing_animation.get('lines', 'Full-Stack+Developer;AI+Enthusiast;Problem+Solver;Code+Craftsman')}"

    return f"""# 👋 Hey! I'm {profile.get('name', 'Guillermo')}

<div align="center">
  <img src="{typing_url}" alt="Typing SVG" />
</div>

{profile.get("description", "I build things. Sometimes they work, sometimes they don't, but I always learn something along the way. Whether it's a simple script or a complex AI system, I love the challenge of turning ideas into reality.")}

<div align="center">
  <img src="https://img.shields.io/badge/{profile.get('title', 'Full-Stack Developer').replace(' ', '--')}-React%20%7C%20Node.js%20%7C%20Python-{badge_colors.get('primary', '58A6FF')}?style=for-the-badge&logo=github&logoColor=white" alt="Full-Stack Developer" />
  <img src="https://img.shields.io/badge/AI%20Enthusiast-Machine%20Learning%20%7C%20NLP-{badge_colors.get('secondary', '4ECDC4')}?style=for-the-badge&logo=github&logoColor=white" alt="AI Enthusiast" />
  <img src="https://img.shields.io/badge/Problem%20Solver-Clean%20Code%20%7C%20Best%20Practices-{badge_colors.get('accent', 'FF6B6B')}?style=for-the-badge&logo=github&logoColor=white" alt="Problem Solver" />
</div>

---

"""


def generate_about_section() -> str:
    """Generate personal about section"""
    # Load configuration for contact information
    try:
        from config_manager import create_config_manager

        config = create_config_manager(str(Path(__file__).parent.parent / "config.yml"))
        contact = config.get_contact_config()
        external_services = config.get_external_services()
    except Exception as e:
        logger.warning(f"Could not load configuration for about section: {e}")
        # Fallback to default values
        contact = {
            "linkedin": "guillermoastorgacalvo",
            "email": "guillermo.astorga.calvo@gmail.com",
            "portfolio": "guillermoastorgacalvo.dev",
        }
        external_services = {
            "linkedin": "https://linkedin.com/in/guillermoastorgacalvo",
            "email": "mailto:guillermo.astorga.calvo@gmail.com",
        }

    linkedin_url = external_services.get(
        "linkedin",
        f"https://linkedin.com/in/{contact.get('linkedin', 'guillermoastorgacalvo')}",
    )
    email_url = external_services.get(
        "email", f"mailto:{contact.get('email', 'guillermo.astorga.calvo@gmail.com')}"
    )

    return f"""## 🚀 What I'm Up To

### 💼 **My Story**
I started coding because I wanted to build things that could actually help people. What began as simple scripts has turned into a passion for creating meaningful applications. I love the challenge of taking a complex problem and turning it into something elegant and useful.

**🔭 Right now:** Working on AI-powered real estate platforms and trying to make invoice processing less painful
**🌱 Learning:** New AI/ML techniques, microservices, and whatever catches my interest
**👯 Looking for:** Cool projects to collaborate on, especially open source stuff
**💬 Ask me about:** React, TypeScript, Python, AI/ML, or anything tech-related - I love talking shop!
**📫 Get in touch:** [LinkedIn]({linkedin_url}) | [Email]({email_url})

### 🎯 **What I Do**
- **Frontend Development**: Building interfaces that people actually want to use
- **Backend Development**: Creating APIs and services that don't break when you need them most
- **AI & ML**: Adding intelligence to applications in ways that actually make sense
- **Database & Cloud**: Making sure data is where it needs to be when it needs to be there
- **DevOps**: Automating the boring stuff so I can focus on building

---

"""


def generate_dynamic_stats_section(data: dict[str, Any]) -> str:
    """Generate comprehensive stats section using enhanced private repo data"""
    if not data or not isinstance(data, dict):
        return ""

    analytics_history = data.get("analytics_history", [])
    unified_stats = data.get("unified_stats", {})

    if not analytics_history and not unified_stats:
        return ""

    # Use unified stats if available, otherwise fall back to analytics history
    if unified_stats:
        return generate_enhanced_stats_from_unified(unified_stats)
    elif analytics_history:
        return generate_stats_from_analytics(analytics_history)

    return ""


def generate_enhanced_stats_from_unified(unified_stats: dict[str, Any]) -> str:
    """Generate enhanced stats section from comprehensive unified stats"""
    # Load configuration for badge colors
    try:
        from config_manager import create_config_manager

        config = create_config_manager(str(Path(__file__).parent.parent / "config.yml"))
        badge_colors = config.get_badge_colors()
    except Exception as e:
        logger.warning(f"Could not load badge colors from config: {e}")
        badge_colors = {
            "primary": "58A6FF",
            "secondary": "4ECDC4",
            "accent": "FF6B6B",
            "purple": "9C27B0",
        }

    # Basic stats badges
    global_summary = unified_stats.get("global_summary", {})
    guillermo_contribution = global_summary.get("guillermo_contribution", {})
    productivity_metrics = unified_stats.get("productivity_metrics", {})

    stats_badges = []
    if "total_loc" in global_summary:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/📈_Lines_of_Code-{format_number(global_summary["total_loc"])}-{badge_colors.get("primary", "58A6FF")}?style=for-the-badge&logo=github&logoColor=white" alt="Lines of Code" />'
        )

    if "total_commits" in global_summary:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/📝_Commits-{format_number(global_summary["total_commits"])}-{badge_colors.get("secondary", "4ECDC4")}?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />'
        )

    if "total_files" in global_summary:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/📁_Files-{format_number(global_summary["total_files"])}-{badge_colors.get("accent", "FF6B6B")}?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />'
        )

    if "repositories_processed" in global_summary:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/🏢_Repositories-{global_summary["repositories_processed"]}-{badge_colors.get("purple", "9C27B0")}?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" />'
        )

    # Personal contribution insights
    contribution_insights = ""
    if guillermo_contribution:
        percentages = guillermo_contribution.get("percentages", {})
        contribution_insights = "\n### **👨‍💻 My Contributions**\n"
        contribution_insights += f"🎯 **{percentages.get('loc', 0):.1f}% of all code** ({format_number(guillermo_contribution.get('loc', 0))} lines)\n"
        contribution_insights += f"📝 **{format_number(guillermo_contribution.get('commits', 0))} commits** across all projects\n"
        contribution_insights += f"📁 **{format_number(guillermo_contribution.get('files', 0))} files** created or modified\n"

    # Productivity metrics
    productivity_insights = ""
    if productivity_metrics:
        productivity_insights = "\n### **⚡ Productivity Metrics**\n"
        productivity_insights += f"🚀 **{productivity_metrics.get('avg_loc_per_commit', 0):.0f} lines per commit**\n"
        productivity_insights += f"📊 **{productivity_metrics.get('avg_files_per_commit', 0):.1f} files per commit**\n"

        code_efficiency = productivity_metrics.get("code_efficiency", {})
        if code_efficiency:
            productivity_insights += (
                f"💡 **{code_efficiency.get('loc_per_file', 0):.0f} lines per file**\n"
            )

    # Language breakdown with SVG chart
    language_stats = ""
    language_analysis = unified_stats.get("language_analysis", {})
    if language_analysis:
        # Sort languages by lines of code (not used but kept for potential future use)
        # sorted_languages = sorted(
        #     language_analysis.items(), key=lambda x: x[1]["lines"], reverse=True
        # )[:5]
        language_stats = "\n### **💻 Top Languages**\n\n"
        language_stats += '<p align="center">\n'
        language_stats += '  <img src="assets/language_stats.svg" alt="Languages by Lines of Code" width="500" />\n'
        language_stats += "</p>\n"

    # Tech stack analysis with skillicons.dev
    tech_stack_insights = ""
    tech_stack_analysis = unified_stats.get("tech_stack_analysis", {})
    if tech_stack_analysis:
        # Map actual technologies to skillicons.dev icons
        tech_to_icon = {
            # Frontend
            "React": "react",
            "TypeScript": "ts",
            "JavaScript": "js",
            "Next.js": "nextjs",
            "TailwindCSS": "tailwind",
            "HTML": "html",
            "CSS": "css",
            "Vue.js": "vuejs",
            "Angular": "angular",
            "React Router": "reactrouter",
            # Backend
            "Node.js": "nodejs",
            "Python": "python",
            "Express.js": "express",
            "FastAPI": "fastapi",
            "Django": "django",
            "Flask": "flask",
            "Java": "java",
            "Spring Boot": "spring",
            # Database & Cloud
            "PostgreSQL": "postgresql",
            "MongoDB": "mongodb",
            "Redis": "redis",
            "AWS": "aws",
            "Docker": "docker",
            "Supabase": "supabase",
            "MySQL": "mysql",
            "SQLite": "sqlite",
            "Prisma": "prisma",
            # AI & ML
            "TensorFlow": "tensorflow",
            "PyTorch": "pytorch",
            "Scikit-learn": "scikit",
            "OpenAI": "openai",
            "Pandas": "pandas",
            "NumPy": "numpy",
            "Tesseract OCR": "tesseract",
            "Pillow": "pillow",
            # DevOps & Tools
            "Git": "git",
            "GitHub": "github",
            "VS Code": "vscode",
            "Linux": "linux",
            "Docker Compose": "docker",
            "Nginx": "nginx",
            "ESLint": "eslint",
            "Webpack": "webpack",
            # Additional
            "Stripe": "stripe",
            "Zod": "zod",
            "Lodash": "lodash",
            "Axios": "axios",
            "Moment.js": "moment",
            "Chart.js": "chartjs",
        }

        # Build dynamic tech stack
        dynamic_tech_stack: dict[str, list[str]] = {
            "frontend": [],
            "backend": [],
            "database": [],
            "ai_ml": [],
            "devops": [],
            "additional": [],
        }

        # Process each category
        for category, data in tech_stack_analysis.items():
            technologies = data.get("technologies", [])
            for tech in technologies:
                icon = tech_to_icon.get(
                    tech, tech.lower().replace(" ", "").replace(".", "")
                )
                if category == "frontend":
                    dynamic_tech_stack["frontend"].append(icon)
                elif category == "backend":
                    dynamic_tech_stack["backend"].append(icon)
                elif category == "database":
                    dynamic_tech_stack["database"].append(icon)
                elif category == "ai_ml":
                    dynamic_tech_stack["ai_ml"].append(icon)
                elif category == "devops":
                    dynamic_tech_stack["devops"].append(icon)
                else:
                    dynamic_tech_stack["additional"].append(icon)

        # Generate tech stack section
        tech_stack_insights = "\n### **🛠️ Technology Stack**\n\n"
        tech_stack_insights += "I believe in using the right tool for the job. Here's my current technology stack based on my projects:\n\n"

        # Frontend
        if dynamic_tech_stack["frontend"]:
            icons = ",".join(dynamic_tech_stack["frontend"][:8])
            tech_stack_insights += f"""#### **🌐 Frontend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Frontend Technologies" />
</div>

"""

        # Backend
        if dynamic_tech_stack["backend"]:
            icons = ",".join(dynamic_tech_stack["backend"][:8])
            tech_stack_insights += f"""#### **⚙️ Backend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Backend Technologies" />
</div>

"""

        # Database & Cloud
        if dynamic_tech_stack["database"]:
            icons = ",".join(dynamic_tech_stack["database"][:8])
            tech_stack_insights += f"""#### **🗄️ Database & Cloud**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Database & Cloud Technologies" />
</div>

"""

        # AI & ML
        if dynamic_tech_stack["ai_ml"]:
            icons = ",".join(dynamic_tech_stack["ai_ml"][:8])
            tech_stack_insights += f"""#### **🤖 AI & Machine Learning**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="AI & ML Technologies" />
</div>

"""

        # DevOps & Tools
        if dynamic_tech_stack["devops"]:
            icons = ",".join(dynamic_tech_stack["devops"][:8])
            tech_stack_insights += f"""#### **🛠️ Development Tools**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Development Tools" />
</div>

"""

        # Additional Technologies
        if dynamic_tech_stack["additional"]:
            icons = ",".join(dynamic_tech_stack["additional"][:8])
            tech_stack_insights += f"""#### **📊 Additional Technologies**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Additional Technologies" />
</div>

"""

    # Repository insights
    repo_insights = ""
    repo_analysis = unified_stats.get("repository_analysis", {})
    if repo_analysis:
        # Sort repositories by Guillermo's contribution
        sorted_repos = sorted(
            repo_analysis.items(),
            key=lambda x: x[1]["guillermo_stats"].get("loc", 0),
            reverse=True,
        )[:3]

        repo_insights = "\n### **🏢 Top Projects**\n"
        for repo_name, repo_data in sorted_repos:
            guillermo_stats = repo_data.get("guillermo_stats", {})
            percentages = repo_data.get("percentages", {})
            repo_insights += f"• **{repo_name}** - {format_number(guillermo_stats.get('loc', 0))} lines ({percentages.get('loc', 0):.1f}% contribution)\n"

    # Insights
    insights_section = ""
    insights = unified_stats.get("insights", {})
    if insights:
        insights_section = "\n### **💡 Key Insights**\n"

        achievements = insights.get("achievements", [])
        if achievements:
            insights_section += "🏆 **Achievements:**\n"
            for achievement in achievements[:2]:  # Show top 2 achievements
                insights_section += f"• {achievement}\n"

        strengths = insights.get("strengths", [])
        if strengths:
            insights_section += "\n💪 **Strengths:**\n"
            for strength in strengths[:2]:  # Show top 2 strengths
                insights_section += f"• {strength}\n"

    # Other/Unknown breakdown
    other_unknown_section = ""
    other_unknown = unified_stats.get("other_unknown_breakdown", {})
    if other_unknown and (
        other_unknown.get("other", 0) > 0 or other_unknown.get("unknown", 0) > 0
    ):
        other_unknown_section = "\n### **🗂️ Other/Unknown Files**\n"
        if other_unknown.get("other", 0) > 0:
            other_unknown_section += (
                f"• **Other:** {format_number(other_unknown['other'])} lines\n"
            )
        if other_unknown.get("unknown", 0) > 0:
            other_unknown_section += (
                f"• **Unknown:** {format_number(other_unknown['unknown'])} lines\n"
            )

    # Validation warning
    validation_section = ""
    validation = unified_stats.get("validation_results", {})
    if validation:
        if (
            validation.get("loc_mismatch")
            or validation.get("files_mismatch")
            or validation.get("commits_mismatch")
        ):
            validation_section = (
                "\n> ⚠️ **Note:** There is a mismatch between the sum of language/project stats and the global totals. "
                "This may be due to unclassified files, multi-language files, or aggregation logic.\n"
            )

    return f"""## 📊 **My Private Repository Stats**

> 📊 **Real data from my private enterprise repositories**
> _Updated every Monday - this is where the real work happens!_

<!-- Dynamic Stats Overview -->
<div align="center">
  {"  ".join(stats_badges)}
</div>

{contribution_insights}

{productivity_insights}

{language_stats}

{tech_stack_insights}

{repo_insights}

{insights_section}

{other_unknown_section}

{validation_section}

These numbers tell the real story - late nights debugging, moments of breakthrough, and a lot of trial and error. Every line of code represents a problem solved or something new learned. The private repos are where the magic happens!

---

"""


def generate_stats_from_analytics(analytics_history: list[dict[str, Any]]) -> str:
    """Generate stats section from analytics history (fallback)"""
    if not analytics_history or len(analytics_history) == 0:
        return ""

    # Load configuration for badge colors
    try:
        from config_manager import create_config_manager

        config = create_config_manager(str(Path(__file__).parent.parent / "config.yml"))
        badge_colors = config.get_badge_colors()
    except Exception as e:
        logger.warning(f"Could not load badge colors from config: {e}")
        badge_colors = {
            "primary": "58A6FF",
            "secondary": "4ECDC4",
            "accent": "FF6B6B",
            "purple": "9C27B0",
        }

    latest_data = analytics_history[-1]  # Get the most recent data

    # Basic stats badges
    stats_badges = []
    if "total_loc" in latest_data:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/📈_Lines_of_Code-{format_number(latest_data["total_loc"])}-{badge_colors.get("primary", "58A6FF")}?style=for-the-badge&logo=github&logoColor=white" alt="Lines of Code" />'
        )

    if "total_commits" in latest_data:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/📝_Commits-{format_number(latest_data["total_commits"])}-{badge_colors.get("secondary", "4ECDC4")}?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />'
        )

    if "total_files" in latest_data:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/📁_Files-{format_number(latest_data["total_files"])}-{badge_colors.get("accent", "FF6B6B")}?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />'
        )

    if "repos_processed" in latest_data:
        stats_badges.append(
            f'<img src="https://img.shields.io/badge/🏢_Repositories-{latest_data["repos_processed"]}-{badge_colors.get("purple", "9C27B0")}?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" />'
        )

    # Personal contribution percentage
    contribution_insights = ""
    if "guillermo_loc" in latest_data and "total_loc" in latest_data:
        contribution_pct = (
            (latest_data["guillermo_loc"] / latest_data["total_loc"]) * 100
            if latest_data["total_loc"] > 0
            else 0
        )
        contribution_insights = "\n### **👨‍💻 My Contributions**\n"
        contribution_insights += f"🎯 **{contribution_pct:.1f}% of all code** ({format_number(latest_data['guillermo_loc'])} lines)\n"
        if "guillermo_commits" in latest_data:
            contribution_insights += f"📝 **{format_number(latest_data['guillermo_commits'])} commits** across all projects\n"
        if "guillermo_files" in latest_data:
            contribution_insights += f"📁 **{format_number(latest_data['guillermo_files'])} files** created or modified\n"

    return f"""## 📊 **My Private Repository Stats**

> 📊 **Real data from my private enterprise repositories**
> _Updated every Monday - this is where the real work happens!_

<!-- Dynamic Stats Overview -->
<div align="center">
  {"  ".join(stats_badges)}
</div>

{contribution_insights}

These numbers tell the real story - late nights debugging, moments of breakthrough, and a lot of trial and error. Every line of code represents a problem solved or something new learned. The private repos are where the magic happens!

---

"""


def generate_projects_section() -> str:
    """Generate authentic projects section with personal stories"""
    projects = get_project_descriptions()

    content = """## 🚀 **Stuff I've Built**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&pause=1000&color=58A6FF&center=true&vCenter=true&width=500&height=50&lines=Innovative+SaaS+Solutions;AI-Powered+Applications;Modern+Web+Platforms" alt="Projects Typing" />
</div>

Here are some projects I'm pretty proud of. Each one taught me something different and pushed me to grow.

"""

    for project_name, project_info in projects.items():
        tech_stack_badges = []
        for tech in project_info["tech_stack"]:
            color_map = {
                "React": "61DAFB",
                "TypeScript": "3178C6",
                "Python": "3776AB",
                "Node.js": "339933",
                "Next.js": "000000",
                "TailwindCSS": "38B2AC",
                "PostgreSQL": "336791",
                "MongoDB": "47A248",
                "Docker": "2496ED",
                "FastAPI": "009688",
                "Express.js": "000000",
            }
            color = color_map.get(tech, "58A6FF")
            tech_stack_badges.append(
                f"![{tech}](https://img.shields.io/badge/-{tech}-{color}?style=for-the-badge&logo={tech.lower()}&logoColor=white)"
            )

        features_list = "\n".join(
            [f"- {feature}" for feature in project_info["features"]]
        )

        content += f"""### 🏆 **{project_name}**
{project_info["status"]} • {project_info["description"]}

**Tech Stack:** {" ".join(tech_stack_badges)}

**What it does:**
{features_list}

**The backstory:** {project_info["story"]}

**🔗 [Check it out]({project_info["url"]})**

---
"""

    return content


def generate_dynamic_tech_stack_section(data: dict[str, Any]) -> str:
    """Generate dynamic tech stack section using skillicons.dev based on actual repository data"""

    # Default tech stack if no data is available
    default_tech_stack = {
        "frontend": ["react", "ts", "js", "nextjs", "tailwind", "html", "css"],
        "backend": ["nodejs", "python", "express", "fastapi"],
        "database": ["postgresql", "mongodb", "aws", "docker"],
        "ai_ml": ["tensorflow", "scikit", "openai"],
        "devops": ["git", "github", "vscode", "linux"],
        "additional": ["supabase", "stripe", "framer"],
    }

    # Try to get actual tech stack from unified stats
    unified_stats = data.get("unified_stats", {})
    tech_stack_analysis = unified_stats.get("tech_stack_analysis", {})

    if tech_stack_analysis:
        # Map actual technologies to skillicons.dev icons
        tech_to_icon = {
            # Frontend
            "React": "react",
            "TypeScript": "ts",
            "JavaScript": "js",
            "Next.js": "nextjs",
            "TailwindCSS": "tailwind",
            "HTML": "html",
            "CSS": "css",
            "Vue.js": "vuejs",
            "Angular": "angular",
            "React Router": "reactrouter",
            # Backend
            "Node.js": "nodejs",
            "Python": "python",
            "Express.js": "express",
            "FastAPI": "fastapi",
            "Django": "django",
            "Flask": "flask",
            "Java": "java",
            "Spring Boot": "spring",
            # Database & Cloud
            "PostgreSQL": "postgresql",
            "MongoDB": "mongodb",
            "Redis": "redis",
            "AWS": "aws",
            "Docker": "docker",
            "Supabase": "supabase",
            "MySQL": "mysql",
            "SQLite": "sqlite",
            "Prisma": "prisma",
            # AI & ML
            "TensorFlow": "tensorflow",
            "PyTorch": "pytorch",
            "Scikit-learn": "scikit",
            "OpenAI": "openai",
            "Pandas": "pandas",
            "NumPy": "numpy",
            "Tesseract OCR": "tesseract",
            "Pillow": "pillow",
            # DevOps & Tools
            "Git": "git",
            "GitHub": "github",
            "VS Code": "vscode",
            "Linux": "linux",
            "Docker Compose": "docker",
            "Nginx": "nginx",
            "ESLint": "eslint",
            "Webpack": "webpack",
            # Additional
            "Stripe": "stripe",
            "Zod": "zod",
            "Lodash": "lodash",
            "Axios": "axios",
            "Moment.js": "moment",
            "Chart.js": "chartjs",
        }

        # Build dynamic tech stack
        dynamic_tech_stack: dict[str, list[str]] = {
            "frontend": [],
            "backend": [],
            "database": [],
            "ai_ml": [],
            "devops": [],
            "additional": [],
        }

        # Process each category
        for category, data in tech_stack_analysis.items():
            technologies = data.get("technologies", [])
            for tech in technologies:
                icon = tech_to_icon.get(
                    tech, tech.lower().replace(" ", "").replace(".", "")
                )
                if category == "frontend":
                    dynamic_tech_stack["frontend"].append(icon)
                elif category == "backend":
                    dynamic_tech_stack["backend"].append(icon)
                elif category == "database":
                    dynamic_tech_stack["database"].append(icon)
                elif category == "ai_ml":
                    dynamic_tech_stack["ai_ml"].append(icon)
                elif category == "devops":
                    dynamic_tech_stack["devops"].append(icon)
                else:
                    dynamic_tech_stack["additional"].append(icon)

        # Use dynamic tech stack if we have data, otherwise use default
        tech_stack = (
            dynamic_tech_stack
            if any(any(techs) for techs in dynamic_tech_stack.values())
            else default_tech_stack
        )
    else:
        tech_stack = default_tech_stack

    # Generate the tech stack section
    content = """## 🛠️ **Technology Stack**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Modern+Technologies;Best+Practices;Clean+Code" alt="Tech Stack Typing" />
</div>

I believe in using the right tool for the job. Here's my current technology stack based on my projects:

"""

    # Frontend
    if tech_stack["frontend"]:
        icons = ",".join(tech_stack["frontend"][:8])  # Limit to 8 icons
        content += f"""### **🌐 Frontend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Frontend Technologies" />
</div>

"""

    # Backend
    if tech_stack["backend"]:
        icons = ",".join(tech_stack["backend"][:8])
        content += f"""### **⚙️ Backend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Backend Technologies" />
</div>

"""

    # Database & Cloud
    if tech_stack["database"]:
        icons = ",".join(tech_stack["database"][:8])
        content += f"""### **🗄️ Database & Cloud**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Database & Cloud Technologies" />
</div>

"""

    # AI & ML
    if tech_stack["ai_ml"]:
        icons = ",".join(tech_stack["ai_ml"][:8])
        content += f"""### **🤖 AI & Machine Learning**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="AI & ML Technologies" />
</div>

"""

    # DevOps & Tools
    if tech_stack["devops"]:
        icons = ",".join(tech_stack["devops"][:8])
        content += f"""### **🛠️ Development Tools**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Development Tools" />
</div>

"""

    # Additional Technologies
    if tech_stack["additional"]:
        icons = ",".join(tech_stack["additional"][:8])
        content += f"""### **📊 Additional Technologies**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Additional Technologies" />
</div>

"""

    content += "---\n"
    return content


def generate_experience_section() -> str:
    """Generate authentic experience section"""
    return """## 💼 **Experience & Growth**

### **🎯 What I Focus On**
I build full-stack applications that solve real problems. My approach is pretty simple - use modern tools, write clean code, and focus on what actually matters to users. I love working with AI and finding ways to make applications smarter without overcomplicating things.

### **🏆 What I've Done**
- **Built SaaS platforms** that handle real traffic and don't crash
- **Added AI features** that actually improve user experience
- **Maintained code quality** across multiple projects
- **Learned to balance** quick development with long-term maintainability

### **📈 My Journey**
- **Started with simple scripts** and gradually tackled bigger challenges
- **Discovered TypeScript** and realized what I'd been missing
- **Explored AI/ML** and found ways to make it practical
- **Embraced DevOps** to make development less painful

The numbers in my stats aren't just metrics - they're late nights, debugging sessions, and moments of "aha!" Every commit represents a problem solved or something new learned.

---

"""


def generate_contact_section() -> str:
    """Generate authentic contact section"""
    # Load configuration for contact information and external services
    try:
        from config_manager import create_config_manager

        config = create_config_manager(str(Path(__file__).parent.parent / "config.yml"))
        contact = config.get_contact_config()
        external_services = config.get_external_services()
        github_config = config.get_github_config()
        badge_colors = config.get_badge_colors()
    except Exception as e:
        logger.warning(f"Could not load configuration for contact section: {e}")
        # Fallback to default values
        contact = {
            "linkedin": "guillermoastorgacalvo",
            "email": "guillermo.astorga.calvo@gmail.com",
            "portfolio": "guillermoastorgacalvo.dev",
        }
        external_services = {
            "linkedin": "https://linkedin.com/in/guillermoastorgacalvo",
            "email": "mailto:guillermo.astorga.calvo@gmail.com",
        }
        github_config = {"username": "GuillermoAstorgaCalvo"}
        badge_colors = {"accent": "FF6B6B"}

    linkedin_url = external_services.get(
        "linkedin",
        f"https://linkedin.com/in/{contact.get('linkedin', 'guillermoastorgacalvo')}",
    )
    email_url = external_services.get(
        "email", f"mailto:{contact.get('email', 'guillermo.astorga.calvo@gmail.com')}"
    )
    github_url = (
        f"https://github.com/{github_config.get('username', 'GuillermoAstorgaCalvo')}"
    )
    portfolio_url = f"https://{contact.get('portfolio', 'guillermoastorgacalvo.dev')}"

    return f"""## 🌟 **Let's Connect**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Let%27s+Build+Something+Amazing;Together!" alt="Contact Typing" />
</div>

I'm always up for connecting with fellow developers, discussing interesting projects, or exploring new opportunities. Whether you want to collaborate on something cool, ask about my projects, or just say hello - I'd love to hear from you!

<div align="center">
  <a href="{linkedin_url}">
    <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="{github_url}">
    <img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="{email_url}">
    <img src="https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <a href="{portfolio_url}">
    <img src="https://img.shields.io/badge/-Portfolio-{badge_colors.get('accent', 'FF6B6B')}?style=for-the-badge&logo=github&logoColor=white" alt="Portfolio" />
  </a>
</div>

---

*Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*
"""


def generate_enhanced_readme(data: dict[str, Any]) -> str:
    """Generate complete enhanced README content"""

    content = ""

    # Hero Section
    content += generate_hero_section()

    # About Section
    content += generate_about_section()

    # Dynamic Stats Section
    content += generate_dynamic_stats_section(data)

    # Projects Section
    content += generate_projects_section()

    # Experience Section
    content += generate_experience_section()

    # Contact Section
    content += generate_contact_section()

    return content


@with_error_context({"component": "enhanced_readme_generator"})
def main() -> None:
    """Main function to generate enhanced README"""
    try:
        # Load analytics data
        data = load_analytics_data()

        # Generate enhanced README content
        content = generate_enhanced_readme(data)

        # Always write to project root
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(root_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Enhanced README generated successfully: {readme_path}")

    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_and_raise(
            DataProcessingError(
                f"Failed to generate enhanced README: {e}",
                error_code=ErrorCodes.DATA_PROCESSING_FAILED,
                context={"script": "enhanced_readme_generator"},
            ),
            logger=logger,
        )


if __name__ == "__main__":
    setup_logging()
    main()
