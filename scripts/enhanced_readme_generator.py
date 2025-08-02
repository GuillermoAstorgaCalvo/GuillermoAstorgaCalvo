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
        # Always look in the project root directory (parent of scripts)
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent
        stats_path = root_dir / "unified_stats.json"

        if stats_path.exists():
            with open(stats_path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                logger.error("Unified stats data is not a dictionary")
                return {}

        logger.debug(
            f"unified_stats.json not found at {stats_path} (this is normal for first run)"
        )
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
        # Always look in the project root directory (parent of scripts)
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent
        history_path = root_dir / "analytics_history.json"

        if history_path.exists():
            with open(history_path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                logger.warning("analytics_history.json does not contain a list")
                return []

        logger.debug(
            f"analytics_history.json not found at {history_path} (this is normal for first run)"
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

        # Load enhanced tech stack data if available
        enhanced_tech_stack = {}
        try:
            script_dir = Path(__file__).parent
            root_dir = script_dir.parent
            enhanced_tech_stack_path = root_dir / "enhanced_tech_stack.json"

            if enhanced_tech_stack_path.exists():
                with open(enhanced_tech_stack_path, encoding="utf-8") as f:
                    enhanced_tech_stack = json.load(f)
                logger.info("Enhanced tech stack data loaded successfully")
            else:
                logger.debug(
                    "Enhanced tech stack file not found, using unified stats only"
                )
        except Exception as e:
            logger.warning(f"Could not load enhanced tech stack data: {e}")

        return {
            "unified_stats": unified_stats,
            "analytics_history": analytics_history,
            "enhanced_tech_stack": enhanced_tech_stack,
        }

    except Exception as e:
        logger.error(f"Error loading analytics data: {e}")
        return {
            "unified_stats": {},
            "analytics_history": [],
            "enhanced_tech_stack": {},
        }


def save_readme(content: str, output_path: str | None = None) -> bool:
    """Save README content to file."""
    try:
        # Always save to the project root directory
        if output_path is None:
            script_dir = Path(__file__).parent
            root_dir = script_dir.parent
            output_path = str(root_dir / "README.md")

        # Ensure directory exists
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

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


def get_dynamic_project_descriptions() -> dict[str, dict[str, Any]]:
    """Get project descriptions with dynamic tech stack detection from repositories."""
    try:
        from api_based_repository_analyzer import APIBasedRepositoryAnalyzer
        from enhanced_dependency_analyzer import EnhancedDependencyAnalyzer

        logger.info("Attempting to get dynamic project tech stacks...")

        # Try API-based analysis first (more comprehensive)
        try:
            api_analyzer = APIBasedRepositoryAnalyzer()
            api_result = api_analyzer.analyze_all_repositories()

            if api_result and isinstance(api_result, dict) and len(api_result) > 0:
                logger.info(
                    "Using API-based repository analysis for project tech stacks"
                )
                return _merge_api_analysis_with_projects(api_result)
        except Exception as e:
            logger.warning(f"API-based analysis failed: {e}")

        # Fallback to enhanced dependency analyzer
        try:
            enhanced_analyzer = EnhancedDependencyAnalyzer()
            enhanced_result = enhanced_analyzer.get_comprehensive_tech_stack()

            if enhanced_result:
                logger.info(
                    "Using enhanced dependency analysis for project tech stacks"
                )
                return _merge_enhanced_analysis_with_projects(enhanced_result)
        except Exception as e:
            logger.warning(f"Enhanced dependency analysis failed: {e}")

        logger.info(
            "Dynamic analysis failed, falling back to static project descriptions"
        )
        return {}

    except Exception as e:
        logger.error(f"Error in dynamic project analysis: {e}")
        return {}


def _merge_api_analysis_with_projects(
    api_result: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Merge API analysis results with project descriptions."""
    # Load base project descriptions
    base_projects = _get_base_project_descriptions()

    # The API analyzer returns tech stack data directly, not nested under "tech_stack_analysis"
    tech_stack_analysis = api_result if isinstance(api_result, dict) else {}

    logger.info(f"API Analysis result keys: {list(tech_stack_analysis.keys())}")
    logger.info(f"API Analysis result: {tech_stack_analysis}")

    # Map project names to their expected tech stack categories
    project_tech_mapping = {
        "InmoIA Frontend": ["frontend"],  # Frontend-only project
        "TypeScript Backend": [
            "backend",
            "database",
            "devops",
        ],  # Backend with database and DevOps
        "Python AI MCP Backend": ["backend", "ai_ml"],  # AI/ML backend
        "FacturaIA": ["frontend", "backend", "ai_ml"],  # Full-stack with AI
        "Restaurant App": ["frontend", "backend", "database"],  # Full-stack app
    }

    # Update projects with dynamic tech stacks
    for project_name, project_info in base_projects.items():
        if project_name in project_tech_mapping:
            dynamic_tech_stack = []

            # Collect technologies from relevant categories
            for category in project_tech_mapping[project_name]:
                if category in tech_stack_analysis:
                    category_techs = tech_stack_analysis[category].get(
                        "technologies", []
                    )
                    logger.info(
                        f"Found {len(category_techs)} technologies for {project_name} in {category}: {category_techs}"
                    )
                    # Convert skillicon IDs back to readable names
                    readable_techs = _convert_skillicon_to_readable(category_techs)
                    dynamic_tech_stack.extend(readable_techs)

            # Update project with dynamic tech stack if found
            if dynamic_tech_stack:
                # Remove duplicates and limit to top technologies
                unique_techs = list(dict.fromkeys(dynamic_tech_stack))[
                    :6
                ]  # Limit to 6 most important
                project_info["tech_stack"] = unique_techs
                logger.info(
                    f"Updated {project_name} with dynamic tech stack: {unique_techs}"
                )
            else:
                logger.info(
                    f"No dynamic tech stack found for {project_name}, keeping static values"
                )

    return base_projects


def _merge_enhanced_analysis_with_projects(
    enhanced_result: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Merge enhanced analysis results with project descriptions."""
    # Load base project descriptions
    base_projects = _get_base_project_descriptions()

    # Get tech stack analysis from enhanced results
    tech_stack_analysis = enhanced_result.get("tech_stack_analysis", {})

    # Map project names to their expected tech stack categories
    project_tech_mapping = {
        "InmoIA Frontend": ["frontend"],
        "TypeScript Backend": ["backend", "database", "devops"],
        "Python AI MCP Backend": ["backend", "database", "ai_ml"],
        "FacturaIA": ["frontend", "backend", "database", "ai_ml"],
        "Restaurant App": ["frontend", "backend", "database"],
    }

    # Update projects with dynamic tech stacks
    for project_name, project_info in base_projects.items():
        if project_name in project_tech_mapping:
            dynamic_tech_stack = []

            # Collect technologies from relevant categories
            for category in project_tech_mapping[project_name]:
                if category in tech_stack_analysis:
                    category_techs = tech_stack_analysis[category].get(
                        "technologies", []
                    )
                    # Convert skillicon IDs back to readable names
                    readable_techs = _convert_skillicon_to_readable(category_techs)
                    dynamic_tech_stack.extend(readable_techs)

            # Update project with dynamic tech stack if found
            if dynamic_tech_stack:
                # Remove duplicates and limit to top technologies
                unique_techs = list(dict.fromkeys(dynamic_tech_stack))[
                    :6
                ]  # Limit to 6 most important
                project_info["tech_stack"] = unique_techs
                logger.info(
                    f"Updated {project_name} with dynamic tech stack: {unique_techs}"
                )

    return base_projects


def _get_base_project_descriptions() -> dict[str, dict[str, Any]]:
    """Get base project descriptions without tech stacks (to be filled dynamically)."""
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
            "tech_stack": [
                "React",
                "TypeScript",
                "TailwindCSS",
                "Next.js",
            ],  # Default fallback
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
            "tech_stack": [
                "Node.js",
                "TypeScript",
                "PostgreSQL",
                "Docker",
            ],  # Default fallback
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
            "tech_stack": [
                "Python",
                "FastAPI",
                "OpenAI",
                "PostgreSQL",
            ],  # Default fallback
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
            "tech_stack": [
                "Python",
                "React",
                "TypeScript",
                "PostgreSQL",
            ],  # Default fallback
            "features": ["OCR Processing", "Data Extraction", "Invoice Management"],
            "status": "🟡 In Development",
            "url": project_urls.get(
                "facturaia", "https://github.com/GuillermoAstorgaCalvo/FacturaIA"
            ),
            "story": "This was born from pure frustration. I was manually processing invoices one day and thought 'there has to be a better way.' Turns out there was - I just had to build it.",
        },
        "Restaurant App": {
            "description": "My first full-stack project that actually went live. Built it for a friend's restaurant and it's still running today.",
            "tech_stack": [
                "React",
                "Node.js",
                "MongoDB",
                "Express.js",
            ],  # Default fallback
            "features": ["Order Management", "Menu System", "Admin Dashboard"],
            "status": "🟢 Live",
            "url": project_urls.get(
                "restaurant_app", "https://restauranteguillermoastorga.up.railway.app/"
            ),
            "story": "This was the project that made me realize I could actually build things people would use. Seeing real customers place orders through something I built was incredibly satisfying.",
        },
    }


def _convert_skillicon_to_readable(skillicon_ids: list[str]) -> list[str]:
    """Convert skillicon IDs back to readable technology names."""
    # Mapping from skillicon IDs to readable names
    skillicon_to_readable = {
        # Frontend
        "react": "React",
        "ts": "TypeScript",
        "js": "JavaScript",
        "nextjs": "Next.js",
        "tailwind": "TailwindCSS",
        "html": "HTML5",
        "css": "CSS3",
        "vue": "Vue.js",
        "angular": "Angular",
        "svelte": "Svelte",
        "supabase": "Supabase",
        # Backend
        "nodejs": "Node.js",
        "py": "Python",
        "express": "Express.js",
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "java": "Java",
        "spring": "Spring Boot",
        "csharp": "C#",
        "go": "Go",
        "rust": "Rust",
        "php": "PHP",
        "ruby": "Ruby",
        # Database
        "postgres": "PostgreSQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "sqlite": "SQLite",
        "elasticsearch": "Elasticsearch",
        "dynamodb": "DynamoDB",
        # DevOps
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "Google Cloud",
        "terraform": "Terraform",
        "ansible": "Ansible",
        "jenkins": "Jenkins",
        "github": "GitHub",
        "gitlab": "GitLab",
        "git": "Git",
        "linux": "Linux",
        "vscode": "VS Code",
        # AI/ML
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "sklearn": "Scikit-learn",
        "opencv": "OpenCV",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "langchain": "LangChain",
        "transformers": "Transformers",
        "tesseract": "Tesseract",
        # Additional
        "stripe": "Stripe",
        "vite": "Vite",
        "webpack": "Webpack",
        "jest": "Jest",
        "prometheus": "Prometheus",
    }

    readable_names = []
    for skillicon_id in skillicon_ids:
        readable_name = skillicon_to_readable.get(skillicon_id, skillicon_id.title())
        readable_names.append(readable_name)

    return readable_names


def get_project_descriptions() -> dict[str, dict[str, Any]]:
    """Get comprehensive project descriptions with dynamic tech stack detection"""
    # Try to get dynamic project descriptions first
    dynamic_projects = get_dynamic_project_descriptions()

    if dynamic_projects:
        logger.info("Using dynamic project descriptions with real tech stacks")
        return dynamic_projects

    # Fallback to static descriptions
    logger.info("Using static project descriptions (fallback)")
    return _get_base_project_descriptions()


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

    # Note: Technology stack is now handled by the dedicated generate_dynamic_tech_stack_section function
    # This ensures better structure, additional dependencies display, and comprehensive analysis

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
        "backend": ["nodejs", "py", "express", "fastapi"],
        "database": ["postgres", "mongodb", "aws", "docker"],
        "ai_ml": ["tensorflow", "sklearn", "opencv"],
        "devops": ["git", "github", "vscode", "linux"],
        "additional": ["supabase", "stripe", "vite"],
    }

    # Try to get actual tech stack from unified stats
    unified_stats = data.get("unified_stats", {})
    tech_stack_analysis = unified_stats.get("tech_stack_analysis", {})

    # Also try to get enhanced tech stack data
    enhanced_tech_stack = data.get("enhanced_tech_stack", {})
    enhanced_analysis = enhanced_tech_stack.get("tech_stack_analysis", {})

    # Use enhanced data if available, otherwise fall back to unified stats
    if enhanced_analysis:
        tech_stack_analysis = enhanced_analysis
        logger.info("Using enhanced tech stack analysis")
    elif tech_stack_analysis:
        logger.info("Using unified stats tech stack analysis")
    else:
        logger.info("No tech stack data available, using defaults")

    if tech_stack_analysis:
        # Use the mapped skillicon IDs directly from the tech stack analysis
        # These are already mapped to valid skillicon IDs by the SkilliconMapper
        dynamic_tech_stack: dict[str, list[str]] = {
            "frontend": [],
            "backend": [],
            "database": [],
            "ai_ml": [],
            "devops": [],
            "additional": [],
        }

        # Process each category - technologies are already mapped to valid skillicon IDs
        for category, category_data in tech_stack_analysis.items():
            technologies = category_data.get("technologies", [])
            if category == "frontend":
                dynamic_tech_stack["frontend"].extend(technologies)
            elif category == "backend":
                dynamic_tech_stack["backend"].extend(technologies)
            elif category == "database":
                dynamic_tech_stack["database"].extend(technologies)
            elif category == "ai_ml":
                dynamic_tech_stack["ai_ml"].extend(technologies)
            elif category == "devops":
                dynamic_tech_stack["devops"].extend(technologies)
            else:
                # Any other categories go to additional
                dynamic_tech_stack["additional"].extend(technologies)

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

    # Helper function to format technology lists
    def format_tech_list(techs: list[str], max_display: int = 8) -> str:
        """Format a list of technologies with proper formatting."""
        if not techs:
            return ""

        # Limit the number of displayed technologies
        display_techs = techs[:max_display]
        formatted_techs = [f"`{tech}`" for tech in display_techs]

        if len(techs) > max_display:
            remaining = len(techs) - max_display
            formatted_techs.append(f"*+{remaining} more*")

        return ", ".join(formatted_techs)

    # Helper function to get additional dependencies for a category
    def get_additional_dependencies(category: str) -> list[str]:
        """Get additional dependencies without skillicons for a specific category."""
        if not tech_stack_analysis or category not in tech_stack_analysis:
            return []

        category_data = tech_stack_analysis[category]
        original_deps = category_data.get("original_dependencies", {})
        return original_deps.get("without_skillicon", [])

    # Helper function to generate category section
    def generate_category_section(
        category_name: str,
        display_name: str,
        emoji: str,
        tech_list: list[str],
        max_icons: int = 8,
    ) -> str:
        """Generate a technology category section."""
        if not tech_list:
            return ""

        # Get skillicon badges
        icons = ",".join(tech_list[:max_icons])

        # Get additional dependencies
        additional_deps = get_additional_dependencies(category_name)

        section = f"""### **{emoji} {display_name}**
<div align="left">
  <img src="https://skillicons.dev/icons?i={icons}" alt="{display_name} Technologies" />
</div>

**Technologies:** {format_tech_list(tech_list)}

"""

        # Add additional dependencies if any
        if additional_deps:
            section += f"**Additional:** {format_tech_list(additional_deps)}\n\n"

        return section

    # Generate each category section
    sections = [
        ("frontend", "Frontend Development", "🌐", tech_stack["frontend"]),
        ("backend", "Backend Development", "⚙️", tech_stack["backend"]),
        ("database", "Database & Cloud", "🗄️", tech_stack["database"]),
        ("ai_ml", "AI & Machine Learning", "🤖", tech_stack["ai_ml"]),
        ("devops", "Development Tools", "🛠️", tech_stack["devops"]),
    ]

    # Add category sections
    for category, display_name, emoji, tech_list in sections:
        section_content = generate_category_section(
            category, display_name, emoji, tech_list
        )
        if section_content:
            content += section_content

    # Handle additional technologies (if any)
    if tech_stack["additional"]:
        icons = ",".join(tech_stack["additional"][:8])
        content += f"""### **📊 Additional Technologies**
<div align="left">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Additional Technologies" />
</div>

**Technologies:** {format_tech_list(tech_stack["additional"])}

"""

        # Collect all additional dependencies from all categories
        if tech_stack_analysis:
            all_additional_deps = []
            for category in ["frontend", "backend", "database", "ai_ml", "devops"]:
                additional_deps = get_additional_dependencies(category)
                all_additional_deps.extend(additional_deps)

            if all_additional_deps:
                # Remove duplicates and sort
                unique_additional = sorted(set(all_additional_deps))
                content += f"**Additional Dependencies:** {format_tech_list(unique_additional, max_display=12)}\n\n"

    # Add summary section if we have comprehensive data
    if tech_stack_analysis:
        total_technologies = sum(
            len(data.get("technologies", [])) for data in tech_stack_analysis.values()
        )
        total_original = sum(
            data.get("original_dependencies", {}).get("total_original", 0)
            for data in tech_stack_analysis.values()
        )

        if total_technologies > 0:
            content += f"""### **📈 Technology Summary**
- **Total Technologies with Icons:** {total_technologies}
- **Total Original Dependencies:** {total_original}
- **Categories Analyzed:** {len([cat for cat, data in tech_stack_analysis.items() if data.get("technologies")])}

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

    # Technology Stack Section
    content += generate_dynamic_tech_stack_section(data)

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
