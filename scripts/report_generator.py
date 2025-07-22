"""
Report Generator Module
Handles generation of markdown reports from statistics data.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from analytics_manager import get_analytics_manager
from analytics_reporter import get_analytics_reporter
from error_handling import DataProcessingError, get_logger, log_and_raise
from stats_processor import AuthorStats, UnifiedStats


class MarkdownReportGenerator:
    """Generates markdown reports from unified statistics."""

    def __init__(
        self,
        title: str = "📊 Unified Code Statistics",
        date_format: str = "%B %d, %Y at %H:%M UTC",
    ):
        """
        Initialize the report generator.

        Args:
            title: Report title
            date_format: Date format string for timestamps
        """
        self.title = title
        self.date_format = date_format
        self.months_en = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        self.logger = get_logger(__name__)

    def format_timestamp(self, dt: datetime | None = None) -> str:
        """
        Format a timestamp according to the configured format.

        Args:
            dt: DateTime object (defaults to current UTC time)

        Returns:
            Formatted timestamp string
        """
        if dt is None:
            dt = datetime.utcnow()

        # Custom formatting for readable English dates
        month_name = self.months_en[dt.month]
        return f"{month_name} {dt.day}, {dt.year} at {dt.strftime('%H:%M')} UTC"

    def format_number(self, number: int) -> str:
        """
        Format a number with thousand separators.

        Args:
            number: Number to format

        Returns:
            Formatted number string
        """
        return f"{number:,}"

    def format_percentage(self, percentage: float) -> str:
        """
        Format a percentage to one decimal place.

        Args:
            percentage: Percentage value

        Returns:
            Formatted percentage string
        """
        return f"{percentage:.1f}"

    def calculate_distribution_percentages(
        self, stats: AuthorStats, totals: AuthorStats
    ) -> tuple:
        """
        Calculate distribution percentages.

        Args:
            stats: Author statistics
            totals: Total repository statistics

        Returns:
            Tuple of (loc_pct, commits_pct, files_pct)
        """
        loc_pct = (stats.loc / totals.loc * 100) if totals.loc > 0 else 0
        commits_pct = (
            (stats.commits / totals.commits * 100) if totals.commits > 0 else 0
        )
        files_pct = (stats.files / totals.files * 100) if totals.files > 0 else 0

        return (loc_pct, commits_pct, files_pct)

    def generate_header(self) -> str:
        """Generate the report header with title and timestamp."""
        current_date = self.format_timestamp()

        header = f"# {self.title}\n\n"
        header += f"*Last updated: {current_date}*\n\n"

        return header

    def generate_global_summary(self, stats: UnifiedStats) -> str:
        """
        Generate the global summary section.

        Args:
            stats: Unified statistics object

        Returns:
            Markdown string for global summary
        """
        try:
            summary = "## 🔍 Global Summary\n\n"

            # Add total statistics
            summary += "**📊 Total Statistics:**\n"
            summary += f"- **Lines of Code:** {stats.total_loc:,}\n"
            summary += f"- **Total Commits:** {stats.total_commits:,}\n"
            summary += f"- **Total Files:** {stats.total_files:,}\n"
            summary += f"- **Repositories Processed:** {stats.repos_processed}\n\n"

            # Add Guillermo's contribution summary
            if stats.guillermo_unified:
                guillermo_stats = stats.guillermo_unified
                summary += "**👨‍💻 My Contributions:**\n"
                summary += f"- **Lines of Code:** {guillermo_stats.loc:,}\n"
                summary += f"- **Commits:** {guillermo_stats.commits:,}\n"
                summary += f"- **Files:** {guillermo_stats.files:,}\n\n"

                # Calculate distribution percentages
                (
                    loc_pct,
                    commits_pct,
                    files_pct,
                ) = self.calculate_distribution_percentages(
                    guillermo_stats,
                    AuthorStats(
                        loc=stats.total_loc,
                        commits=stats.total_commits,
                        files=stats.total_files,
                    ),
                )

                summary += "**📈 Contribution Distribution:**\n"
                summary += f"- **LOC:** {loc_pct:.1f}%\n"
                summary += f"- **Commits:** {commits_pct:.1f}%\n"
                summary += f"- **Files:** {files_pct:.1f}%\n\n"

            return summary

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error generating global summary: {e}")
            return "## 🔍 Global Summary\n\n*Error generating summary*\n\n"
        except (ValueError, ZeroDivisionError) as e:
            self.logger.error(f"Error calculating distribution percentages: {e}")
            return "## 🔍 Global Summary\n\n*Error calculating statistics*\n\n"

    def generate_contributions_table(self, stats: UnifiedStats) -> str:
        """
        Generate the contributions table section.

        Args:
            stats: Unified statistics data

        Returns:
            Markdown string for contributions table
        """
        table = "## 👨‍💻 Contributions by Repository\n\n"
        table += "| Repository | Lines | Commits | Files | Distribution % |\n"
        table += "|:-----------|------:|--------:|------:|:---------------|\n"

        # Calculate global distribution percentages
        guillermo = stats.guillermo_unified
        global_totals = AuthorStats(
            loc=stats.total_loc, commits=stats.total_commits, files=stats.total_files
        )

        loc_pct, commits_pct, files_pct = self.calculate_distribution_percentages(
            guillermo, global_totals
        )

        # Add unified total row
        table += "| **🌟 TOTAL UNIFIED** | "
        table += f"**{self.format_number(guillermo.loc)}** | "
        table += f"**{self.format_number(guillermo.commits)}** | "
        table += f"**{self.format_number(guillermo.files)}** | "
        table += f"**{self.format_percentage(loc_pct)}/{self.format_percentage(commits_pct)}/{self.format_percentage(files_pct)}** |\n"

        # Add separator row
        table += "| | | | | |\n"

        # Sort repositories in specific order: Frontend, Backend, AI Backend
        def get_repo_order_key(repo_name: str) -> int:
            """Get sorting key to ensure specific repository order."""
            repo_name_lower = repo_name.lower()
            if "frontend" in repo_name_lower:
                return 1  # First
            elif "backend" in repo_name_lower and "ai" not in repo_name_lower:
                return 2  # Second
            elif "ai" in repo_name_lower:
                return 3  # Third
            else:
                return 4  # Any others last

        # Sort repositories by the defined order
        sorted_repos = sorted(
            stats.repo_breakdown.items(), key=lambda x: get_repo_order_key(x[0])
        )

        # Add individual repository rows in sorted order
        for repo_name, repo_data in sorted_repos:
            g_stats = repo_data.guillermo_stats
            repo_totals = repo_data.repo_totals

            # Calculate repository-specific percentages
            (
                repo_loc_pct,
                repo_commits_pct,
                repo_files_pct,
            ) = self.calculate_distribution_percentages(g_stats, repo_totals)

            table += f"| 📁 **{repo_name}** | "
            table += f"{self.format_number(g_stats.loc)} | "
            table += f"{self.format_number(g_stats.commits)} | "
            table += f"{self.format_number(g_stats.files)} | "
            table += f"{self.format_percentage(repo_loc_pct)}/{self.format_percentage(repo_commits_pct)}/{self.format_percentage(repo_files_pct)} |\n"

        return table

    def generate_language_breakdown_table(self, stats: UnifiedStats) -> str:
        """
        Generate the language breakdown table section.

        Args:
            stats: Unified statistics data

        Returns:
            Markdown string for language breakdown table
        """
        if not stats.unified_language_stats:
            return ""

        table = "## 🔤 Language Breakdown\n\n"
        table += "| Language | Lines | Commits | Files | % of Total LOC |\n"
        table += "|:---------|------:|--------:|------:|:---------------|\n"

        # Sort languages by LOC (descending)
        sorted_languages = sorted(
            stats.unified_language_stats.items(),
            key=lambda x: x[1]["loc"],
            reverse=True,
        )

        total_loc = stats.total_loc

        for language, lang_stats in sorted_languages:
            loc = lang_stats["loc"]
            commits = lang_stats["commits"]
            files = lang_stats["files"]

            # Calculate percentage of total LOC
            loc_pct = (loc / total_loc * 100) if total_loc > 0 else 0

            # Add language emoji based on language
            emoji = self._get_language_emoji(language)

            table += f"| {emoji} **{language}** | {self.format_number(loc)} | "
            table += f"{self.format_number(commits)} | {self.format_number(files)} | "
            table += f"{self.format_percentage(loc_pct)} |\n"

        return table

    def _get_language_emoji(self, language: str) -> str:
        """Get emoji for a programming language."""
        language_emojis = {
            "Python": "🐍",
            "JavaScript": "🟨",
            "TypeScript": "🔷",
            "Java": "☕",
            "C": "🔵",
            "C++": "🔵",
            "C#": "💜",
            "PHP": "🐘",
            "Ruby": "💎",
            "Go": "🐹",
            "Rust": "🦀",
            "Swift": "🍎",
            "Kotlin": "🟠",
            "Scala": "🔴",
            "HTML": "🌐",
            "CSS": "🎨",
            "Shell": "🐚",
            "PowerShell": "💻",
            "SQL": "🗄️",
            "R": "📊",
            "MATLAB": "📈",
            "Julia": "🔬",
            "Dart": "🎯",
            "Lua": "🌙",
            "Perl": "🐪",
            "Haskell": "λ",
            "Clojure": "🍃",
            "Elixir": "💧",
            "Erlang": "☎️",
            "OCaml": "🐫",
            "F#": "🔷",
            "Assembly": "⚙️",
            "VHDL": "🔌",
            "Verilog": "🔌",
            "TeX": "📝",
            "Markdown": "📄",
            "YAML": "📋",
            "JSON": "📄",
            "XML": "📄",
            "CSV": "📊",
            "Dockerfile": "🐳",
            "Makefile": "🔨",
            "CMake": "🔨",
            "Gradle": "🔨",
            "Maven": "🔨",
            "Documentation": "📚",
            "Configuration": "⚙️",
            "Data": "📊",
            "Assets": "🎨",
            "Unknown": "❓",
        }

        return language_emojis.get(language, "📄")

    def generate_footer(self) -> str:
        """Generate the report footer."""
        footer = "\n---\n"
        footer += "*Generated automatically by GitHub Actions*"

        return footer

    def generate_report(
        self, stats: UnifiedStats, config: dict[str, Any] | None = None
    ) -> str:
        report = ""
        try:
            report += self.generate_header()
            report += self.generate_global_summary(stats)
            report += self.generate_contributions_table(stats)
            if config and config.get("analytics", {}).get("track_history", False):
                try:
                    analytics_manager = get_analytics_manager()
                    analytics_reporter = get_analytics_reporter()
                    stats_dict = {
                        "total_loc": stats.total_loc,
                        "total_commits": stats.total_commits,
                        "total_files": stats.total_files,
                        "guillermo_unified": {
                            "loc": stats.guillermo_unified.loc,
                            "commits": stats.guillermo_unified.commits,
                            "files": stats.guillermo_unified.files,
                        },
                        "repos_processed": stats.repos_processed,
                        "unified_language_stats": stats.unified_language_stats,
                    }
                    analytics_manager.add_data_point(stats_dict)
                    trends = analytics_manager.get_trend_analysis()
                    language_config = config.get("analytics", {}).get(
                        "language_usage", {}
                    )
                    language_analysis = analytics_manager.track_language_usage(
                        stats_dict, language_config
                    )
                    analytics_section = analytics_reporter.generate_analytics_summary(
                        trends, language_analysis
                    )
                    report += analytics_section
                    retention_days = config.get("analytics", {}).get(
                        "retention_days", 90
                    )
                    analytics_manager.cleanup_old_data(retention_days)
                except (TypeError, AttributeError, KeyError, ValueError, OSError) as e:
                    self.logger.error(f"Analytics section failed: {e}", exc_info=True)
                    report += (
                        "\n### 📊 Analytics\n\n⚠️ Analytics temporarily unavailable.\n\n"
                    )
            report += self.generate_footer()
            return report
        except (TypeError, AttributeError, KeyError, ValueError, OSError) as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed to generate markdown report: {e}",
                    context={"stats": str(stats), "config": str(config)},
                ),
                logger=self.logger,
            )
            return ""  # This line will never be reached due to log_and_raise

    def save_report(
        self,
        stats: UnifiedStats,
        filename: str = "STATS.md",
        config: dict[str, Any] | None = None,
    ) -> None:
        """
        Generate and save a markdown report to file.

        Args:
            stats: Unified statistics data
            filename: Output filename
            config: Configuration dictionary for analytics
        """
        try:
            report = self.generate_report(stats, config)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report)
            self.logger.info(f"Markdown report saved to {filename}")
        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed to save markdown report: {e}",
                    context={"filename": filename},
                ),
                logger=self.logger,
            )


class JSONReportGenerator:
    """Generates comprehensive JSON reports from unified statistics."""

    def __init__(self) -> None:
        """Initialize the JSON report generator."""
        self.logger = get_logger(__name__)

    def generate_report(
        self, stats: UnifiedStats, tech_stack_data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Generate a comprehensive JSON report from unified statistics.

        Args:
            stats: Unified statistics data
        Returns:
            Dictionary representation of the comprehensive statistics
        """
        from datetime import datetime

        try:
            # Calculate additional metrics
            guillermo = stats.guillermo_unified
            global_totals = AuthorStats(
                loc=stats.total_loc,
                commits=stats.total_commits,
                files=stats.total_files,
            )

            # Calculate percentages
            loc_pct = (
                (guillermo.loc / global_totals.loc * 100)
                if global_totals.loc > 0
                else 0
            )
            commits_pct = (
                (guillermo.commits / global_totals.commits * 100)
                if global_totals.commits > 0
                else 0
            )
            files_pct = (
                (guillermo.files / global_totals.files * 100)
                if global_totals.files > 0
                else 0
            )

            # Calculate productivity metrics
            avg_loc_per_commit = (
                guillermo.loc / guillermo.commits if guillermo.commits > 0 else 0
            )
            avg_files_per_commit = (
                guillermo.files / guillermo.commits if guillermo.commits > 0 else 0
            )

            # Language analysis
            language_analysis = {}
            if stats.unified_language_stats:
                total_loc = stats.total_loc
                for lang, lang_stats in stats.unified_language_stats.items():
                    lang_pct = (
                        (lang_stats["loc"] / total_loc * 100) if total_loc > 0 else 0
                    )
                    language_analysis[lang] = {
                        "lines": lang_stats["loc"],
                        "commits": lang_stats["commits"],
                        "files": lang_stats["files"],
                        "percentage": round(lang_pct, 2),
                        "avg_loc_per_commit": (
                            lang_stats["loc"] / lang_stats["commits"]
                            if lang_stats["commits"] > 0
                            else 0
                        ),
                    }

            # Repository analysis
            repo_analysis = {}
            for repo_name, repo_data in stats.repo_breakdown.items():
                repo_guillermo = repo_data.guillermo_stats
                repo_totals = repo_data.repo_totals

                repo_loc_pct = (
                    (repo_guillermo.loc / repo_totals.loc * 100)
                    if repo_totals.loc > 0
                    else 0
                )
                repo_commits_pct = (
                    (repo_guillermo.commits / repo_totals.commits * 100)
                    if repo_totals.commits > 0
                    else 0
                )
                repo_files_pct = (
                    (repo_guillermo.files / repo_totals.files * 100)
                    if repo_totals.files > 0
                    else 0
                )

                repo_analysis[repo_name] = {
                    "guillermo_stats": repo_guillermo.to_dict(),
                    "repo_totals": repo_totals.to_dict(),
                    "percentages": {
                        "loc": round(repo_loc_pct, 2),
                        "commits": round(repo_commits_pct, 2),
                        "files": round(repo_files_pct, 2),
                    },
                    "productivity": {
                        "avg_loc_per_commit": (
                            repo_guillermo.loc / repo_guillermo.commits
                            if repo_guillermo.commits > 0
                            else 0
                        ),
                        "avg_files_per_commit": (
                            repo_guillermo.files / repo_guillermo.commits
                            if repo_guillermo.commits > 0
                            else 0
                        ),
                    },
                }

            # Use provided tech stack data or fallback to analysis
            if tech_stack_data:
                tech_stack = tech_stack_data
            else:
                tech_stack = self._analyze_tech_stack(stats.unified_language_stats)

            # Project complexity analysis
            complexity_analysis = self._analyze_complexity(stats)

            # Generate comprehensive report
            report = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "metadata": {
                    "version": "2.0",
                    "generated_by": "Enhanced JSON Report Generator",
                    "data_source": "Private Repository Analytics",
                },
                "global_summary": {
                    "repositories_processed": stats.repos_processed,
                    "total_commits": stats.total_commits,
                    "total_files": stats.total_files,
                    "total_loc": stats.total_loc,
                    "guillermo_contribution": {
                        "loc": guillermo.loc,
                        "commits": guillermo.commits,
                        "files": guillermo.files,
                        "percentages": {
                            "loc": round(loc_pct, 2),
                            "commits": round(commits_pct, 2),
                            "files": round(files_pct, 2),
                        },
                    },
                },
                "productivity_metrics": {
                    "avg_loc_per_commit": round(avg_loc_per_commit, 2),
                    "avg_files_per_commit": round(avg_files_per_commit, 2),
                    "code_efficiency": {
                        "loc_per_file": (
                            guillermo.loc / guillermo.files
                            if guillermo.files > 0
                            else 0
                        ),
                        "commits_per_file": (
                            guillermo.commits / guillermo.files
                            if guillermo.files > 0
                            else 0
                        ),
                    },
                },
                "language_analysis": language_analysis,
                "repository_analysis": repo_analysis,
                "tech_stack_analysis": tech_stack,
                "complexity_analysis": complexity_analysis,
                "insights": self._generate_insights(
                    stats, language_analysis, repo_analysis
                ),
                "raw_data": {
                    "guillermo_unified": stats.guillermo_unified.to_dict(),
                    "repository_breakdown": {
                        name: data.to_dict()
                        for name, data in stats.repo_breakdown.items()
                    },
                    "language_breakdown": stats.unified_language_stats,
                },
            }

            return report
        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed to generate JSON report: {e}",
                    context={"stats": str(stats)},
                ),
                logger=self.logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def _analyze_tech_stack(self, language_stats: dict[str, Any]) -> dict[str, Any]:
        """Analyze technology stack from actual dependencies in package.json and requirements.txt files."""
        try:
            from dependency_analyzer import DependencyAnalyzer

            analyzer = DependencyAnalyzer()
            current_dir = Path.cwd()
            repos_dir = current_dir / "repos"
            if not repos_dir.exists():
                repos_dir = current_dir
            tech_stack = analyzer.analyze_all_repositories(repos_dir)

            # Enhanced tech stack based on README projects
            # This includes technologies from all the user's projects mentioned in README
            enhanced_tech_stack = {
                "frontend": {
                    "technologies": [
                        "react",
                        "ts",
                        "js",
                        "nextjs",
                        "tailwind",
                        "supabase",
                    ],
                    "total_loc": 0,
                },
                "backend": {
                    "technologies": [
                        "express",
                        "jest",
                        "nodejs",
                        "prometheus",
                        "redis",
                        "ts",
                        "py",
                        "fastapi",
                        "django",
                        "flask",
                    ],
                    "total_loc": 0,
                },
                "database": {
                    "technologies": ["postgres", "mongodb", "redis", "sqlite"],
                    "total_loc": 0,
                },
                "devops": {
                    "technologies": [
                        "docker",
                        "kubernetes",
                        "aws",
                        "azure",
                        "gcp",
                        "githubactions",
                        "nginx",
                        "jenkins",
                        "terraform",
                    ],
                    "total_loc": 0,
                },
                "ai_ml": {
                    "technologies": [
                        "openai",
                        "tensorflow",
                        "pytorch",
                        "sklearn",
                        "pandas",
                        "numpy",
                        "opencv",
                        "tesseract",
                        "langchain",
                        "anthropic",
                    ],
                    "total_loc": 0,
                },
            }

            # Merge detected technologies with enhanced list
            for category in ["frontend", "backend", "database", "devops", "ai_ml"]:
                detected_techs = tech_stack.get(category, {}).get("technologies", [])
                enhanced_techs = enhanced_tech_stack[category]["technologies"]
                # Combine and remove duplicates while preserving order
                combined_techs = []
                seen = set()
                for tech in enhanced_techs + detected_techs:
                    if tech not in seen:
                        combined_techs.append(tech)
                        seen.add(tech)
                enhanced_tech_stack[category]["technologies"] = combined_techs
                enhanced_tech_stack[category]["count"] = len(combined_techs)

            # Calculate total_loc based on language stats
            for lang, stats in language_stats.items():
                loc = stats.get("loc", 0)
                if lang in ["TypeScript", "JavaScript", "HTML", "CSS"]:
                    enhanced_tech_stack["frontend"]["total_loc"] += loc
                elif lang == "Python":
                    enhanced_tech_stack["backend"]["total_loc"] += loc

            return enhanced_tech_stack
        except ImportError:
            self.logger.warning(
                "DependencyAnalyzer not available, using fallback tech stack analysis"
            )
            return self._fallback_tech_stack_analysis(language_stats)
        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed to analyze tech stack: {e}",
                    context={"language_stats": str(language_stats)},
                ),
                logger=self.logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def _fallback_tech_stack_analysis(
        self, language_stats: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            categories: dict[str, dict[str, Any]] = {
                "frontend": {"technologies": [], "total_loc": 0},
                "backend": {"technologies": [], "total_loc": 0},
                "database": {"technologies": [], "total_loc": 0},
                "devops": {"technologies": [], "total_loc": 0},
                "ai_ml": {"technologies": [], "total_loc": 0},
            }
            lang_to_tech = {
                "TypeScript": "TypeScript, React, Next.js",
                "JavaScript": "JavaScript, Node.js",
                "Python": "Python, FastAPI, Django",
                "HTML": "HTML",
                "CSS": "CSS, TailwindCSS",
            }
            for lang, stats in language_stats.items():
                if lang in lang_to_tech:
                    tech_name = lang_to_tech[lang]
                    loc = stats.get("loc", 0)
                    if lang in ["TypeScript", "JavaScript", "HTML", "CSS"]:
                        frontend_techs = categories["frontend"]["technologies"]
                        if isinstance(frontend_techs, list):
                            frontend_techs.append(tech_name)
                        categories["frontend"]["total_loc"] += loc
                    elif lang == "Python":
                        backend_techs = categories["backend"]["technologies"]
                        if isinstance(backend_techs, list):
                            backend_techs.append(tech_name)
                        categories["backend"]["total_loc"] += loc
            for category in categories.values():
                techs = category["technologies"]
                if isinstance(techs, list):
                    category["technologies"] = sorted(set(techs))
            return categories
        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed in fallback tech stack analysis: {e}",
                    context={"language_stats": str(language_stats)},
                ),
                logger=self.logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def _analyze_complexity(self, stats: UnifiedStats) -> dict[str, Any]:
        try:
            total_loc = stats.total_loc
            total_commits = stats.total_commits
            total_files = stats.total_files
            excluded_categories = {
                "Unknown",
                "Assets",
                "Documentation",
                "Image",
                "Font",
                "Archive",
                "Binary",
                "JSON",
                "YAML",
                "TOML",
                "INI",
                "Properties",
                "Log",
                "Markdown",
                "reStructuredText",
                "AsciiDoc",
                "BibTeX",
            }
            programming_languages = 0
            if stats.unified_language_stats:
                programming_languages = len(
                    [
                        lang
                        for lang in stats.unified_language_stats.keys()
                        if lang not in excluded_categories
                    ]
                )
            complexity = {
                "project_scale": {
                    "total_projects": stats.repos_processed,
                    "avg_loc_per_project": (
                        total_loc / stats.repos_processed
                        if stats.repos_processed > 0
                        else 0
                    ),
                    "avg_commits_per_project": (
                        total_commits / stats.repos_processed
                        if stats.repos_processed > 0
                        else 0
                    ),
                    "avg_files_per_project": (
                        total_files / stats.repos_processed
                        if stats.repos_processed > 0
                        else 0
                    ),
                },
                "code_distribution": {
                    "loc_per_file": total_loc / total_files if total_files > 0 else 0,
                    "commits_per_file": (
                        total_commits / total_files if total_files > 0 else 0
                    ),
                    "files_per_commit": (
                        total_files / total_commits if total_commits > 0 else 0
                    ),
                },
                "repository_diversity": {
                    "languages_used": programming_languages,
                    "project_types": len(stats.repo_breakdown),
                },
            }
            return complexity
        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed to analyze complexity: {e}", context={"stats": str(stats)}
                ),
                logger=self.logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def _generate_insights(
        self,
        stats: UnifiedStats,
        language_analysis: dict[str, Any],
        repo_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            insights: dict[str, list[str]] = {
                "strengths": [],
                "focus_areas": [],
                "achievements": [],
                "recommendations": [],
            }
            excluded_categories = {
                "Unknown",
                "Assets",
                "Documentation",
                "Image",
                "Font",
                "Archive",
                "Binary",
                "JSON",
                "YAML",
                "TOML",
                "INI",
                "Properties",
                "Log",
                "Markdown",
                "reStructuredText",
                "AsciiDoc",
                "BibTeX",
            }
            programming_languages = 0
            if stats.unified_language_stats:
                programming_languages = len(
                    [
                        lang
                        for lang in stats.unified_language_stats.keys()
                        if lang not in excluded_categories
                    ]
                )
            if stats.guillermo_unified.commits > 100:
                insights["strengths"].append(
                    "High commit frequency indicates consistent development activity"
                )
            if programming_languages > 5:
                insights["strengths"].append(
                    "Diverse technology stack across multiple programming languages"
                )
            if stats.guillermo_unified.loc > 100000:
                insights["focus_areas"].append(
                    "Large codebase suggests complex, enterprise-level projects"
                )
            if stats.guillermo_unified.loc > 50000:
                insights["achievements"].append(
                    f"Built {stats.guillermo_unified.loc:,} lines of code across {stats.repos_processed} projects"
                )
            if stats.guillermo_unified.commits > 200:
                insights["achievements"].append(
                    f"Made {stats.guillermo_unified.commits:,} commits demonstrating consistent development"
                )
            if programming_languages < 3:
                insights["recommendations"].append(
                    "Consider expanding technology stack for broader expertise"
                )
            return insights
        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Failed to generate insights: {e}",
                    context={
                        "stats": str(stats),
                        "language_analysis": str(language_analysis),
                        "repo_analysis": str(repo_analysis),
                    },
                ),
                logger=self.logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def _generate_advanced_insights(
        self,
        stats: UnifiedStats,
        language_analysis: dict[str, Any],
        repo_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate advanced insights including skill assessment and predictions."""
        insights = {
            "skill_assessment": self._assess_skill_levels(stats, language_analysis),
            "technology_maturity": self._analyze_technology_maturity(stats),
            "productivity_trends": self._analyze_productivity_trends(stats),
            "recommendations": self._generate_recommendations(stats, language_analysis),
            "predictions": self._generate_predictions(stats),
        }
        return insights

    def _assess_skill_levels(
        self, stats: UnifiedStats, language_analysis: dict[str, Any]
    ) -> dict[str, Any]:
        """Assess skill levels based on code complexity and productivity."""
        skill_levels = {}

        # Analyze by language
        for lang, lang_stats in language_analysis.items():
            loc = lang_stats.get("lines", 0)
            commits = lang_stats.get("commits", 0)

            if loc > 0:
                # Calculate complexity metrics
                avg_loc_per_commit = loc / max(commits, 1)
                complexity_score = min(
                    avg_loc_per_commit / 100, 1.0
                )  # Normalize to 0-1

                # Determine skill level
                if complexity_score > 0.8 and loc > 10000:
                    skill_level = "Expert"
                elif complexity_score > 0.6 and loc > 5000:
                    skill_level = "Advanced"
                elif complexity_score > 0.4 and loc > 1000:
                    skill_level = "Intermediate"
                else:
                    skill_level = "Beginner"

                skill_levels[lang] = {
                    "level": skill_level,
                    "confidence": min(complexity_score * 100, 100),
                    "metrics": {
                        "total_loc": loc,
                        "avg_loc_per_commit": avg_loc_per_commit,
                        "complexity_score": complexity_score,
                    },
                }

        return skill_levels

    def _analyze_technology_maturity(self, stats: UnifiedStats) -> dict[str, Any]:
        """Analyze technology stack maturity and adoption patterns."""
        maturity_analysis = {
            "frontend_maturity": self._assess_frontend_maturity(stats),
            "backend_maturity": self._assess_backend_maturity(stats),
            "devops_maturity": self._assess_devops_maturity(stats),
            "ai_ml_maturity": self._assess_ai_ml_maturity(stats),
        }
        return maturity_analysis

    def _assess_frontend_maturity(self, stats: UnifiedStats) -> dict[str, Any]:
        """Assess frontend technology maturity."""
        frontend_techs = stats.tech_stack_analysis.get("frontend", {}).get(
            "technologies", []
        )

        # Modern frontend indicators
        modern_indicators = ["react", "vue", "angular", "nextjs", "nuxt", "svelte"]
        modern_count = sum(1 for tech in frontend_techs if tech in modern_indicators)

        # Build tools
        build_tools = ["vite", "webpack", "rollup", "parcel"]
        build_tool_count = sum(1 for tech in frontend_techs if tech in build_tools)

        # Styling frameworks
        styling_frameworks = ["tailwind", "bootstrap", "material-ui", "chakra"]
        styling_count = sum(1 for tech in frontend_techs if tech in styling_frameworks)

        # Calculate maturity score
        maturity_score = (
            modern_count * 0.4 + build_tool_count * 0.3 + styling_count * 0.3
        ) / 3

        if maturity_score > 0.8:
            maturity_level = "Advanced"
        elif maturity_score > 0.6:
            maturity_level = "Intermediate"
        elif maturity_score > 0.4:
            maturity_level = "Basic"
        else:
            maturity_level = "Beginner"

        return {
            "level": maturity_level,
            "score": maturity_score,
            "modern_frameworks": modern_count,
            "build_tools": build_tool_count,
            "styling_frameworks": styling_count,
            "recommendations": self._get_frontend_recommendations(frontend_techs),
        }

    def _assess_backend_maturity(self, stats: UnifiedStats) -> dict[str, Any]:
        """Assess backend technology maturity."""
        backend_techs = stats.tech_stack_analysis.get("backend", {}).get(
            "technologies", []
        )

        # Modern backend indicators
        modern_indicators = [
            "fastapi",
            "express",
            "nestjs",
            "spring",
            "django",
            "flask",
        ]
        modern_count = sum(1 for tech in backend_techs if tech in modern_indicators)

        # Database technologies
        db_techs = stats.tech_stack_analysis.get("database", {}).get("technologies", [])
        db_count = len(db_techs)

        # API technologies
        api_indicators = ["rest", "graphql", "grpc", "openapi"]
        api_count = sum(
            1 for tech in backend_techs if any(api in tech for api in api_indicators)
        )

        # Calculate maturity score
        maturity_score = (modern_count * 0.4 + db_count * 0.3 + api_count * 0.3) / 3

        if maturity_score > 0.8:
            maturity_level = "Advanced"
        elif maturity_score > 0.6:
            maturity_level = "Intermediate"
        elif maturity_score > 0.4:
            maturity_level = "Basic"
        else:
            maturity_level = "Beginner"

        return {
            "level": maturity_level,
            "score": maturity_score,
            "modern_frameworks": modern_count,
            "database_technologies": db_count,
            "api_technologies": api_count,
            "recommendations": self._get_backend_recommendations(backend_techs),
        }

    def _assess_devops_maturity(self, stats: UnifiedStats) -> dict[str, Any]:
        """Assess DevOps technology maturity."""
        devops_techs = stats.tech_stack_analysis.get("devops", {}).get(
            "technologies", []
        )

        # Containerization
        container_indicators = ["docker", "kubernetes", "containerd"]
        container_count = sum(
            1 for tech in devops_techs if tech in container_indicators
        )

        # Cloud platforms
        cloud_indicators = ["aws", "azure", "gcp", "digitalocean", "heroku"]
        cloud_count = sum(1 for tech in devops_techs if tech in cloud_indicators)

        # CI/CD
        cicd_indicators = ["githubactions", "jenkins", "gitlab", "circleci", "travis"]
        cicd_count = sum(1 for tech in devops_techs if tech in cicd_indicators)

        # Infrastructure as Code
        iac_indicators = ["terraform", "ansible", "cloudformation", "pulumi"]
        iac_count = sum(1 for tech in devops_techs if tech in iac_indicators)

        # Calculate maturity score
        maturity_score = (
            container_count * 0.3
            + cloud_count * 0.3
            + cicd_count * 0.2
            + iac_count * 0.2
        ) / 4

        if maturity_score > 0.8:
            maturity_level = "Advanced"
        elif maturity_score > 0.6:
            maturity_level = "Intermediate"
        elif maturity_score > 0.4:
            maturity_level = "Basic"
        else:
            maturity_level = "Beginner"

        return {
            "level": maturity_level,
            "score": maturity_score,
            "containerization": container_count,
            "cloud_platforms": cloud_count,
            "cicd_tools": cicd_count,
            "infrastructure_as_code": iac_count,
            "recommendations": self._get_devops_recommendations(devops_techs),
        }

    def _assess_ai_ml_maturity(self, stats: UnifiedStats) -> dict[str, Any]:
        """Assess AI/ML technology maturity."""
        ai_ml_techs = stats.tech_stack_analysis.get("ai_ml", {}).get("technologies", [])

        # Deep Learning frameworks
        dl_indicators = ["tensorflow", "pytorch", "keras", "jax"]
        dl_count = sum(1 for tech in ai_ml_techs if tech in dl_indicators)

        # Traditional ML
        ml_indicators = ["sklearn", "pandas", "numpy", "scipy"]
        ml_count = sum(1 for tech in ai_ml_techs if tech in ml_indicators)

        # AI Services
        ai_services = ["openai", "anthropic", "huggingface", "langchain"]
        ai_count = sum(1 for tech in ai_ml_techs if tech in ai_services)

        # Computer Vision
        cv_indicators = ["opencv", "pillow", "albumentations"]
        cv_count = sum(1 for tech in ai_ml_techs if tech in cv_indicators)

        # Calculate maturity score
        maturity_score = (
            dl_count * 0.3 + ml_count * 0.3 + ai_count * 0.2 + cv_count * 0.2
        ) / 4

        if maturity_score > 0.8:
            maturity_level = "Advanced"
        elif maturity_score > 0.6:
            maturity_level = "Intermediate"
        elif maturity_score > 0.4:
            maturity_level = "Basic"
        else:
            maturity_level = "Beginner"

        return {
            "level": maturity_level,
            "score": maturity_score,
            "deep_learning": dl_count,
            "machine_learning": ml_count,
            "ai_services": ai_count,
            "computer_vision": cv_count,
            "recommendations": self._get_ai_ml_recommendations(ai_ml_techs),
        }

    def _analyze_productivity_trends(self, stats: UnifiedStats) -> dict[str, Any]:
        """Analyze productivity trends and patterns."""
        total_commits = stats.total_commits
        total_loc = stats.total_loc
        total_files = stats.total_files

        # Calculate productivity metrics
        avg_loc_per_commit = total_loc / max(total_commits, 1)
        avg_files_per_commit = total_files / max(total_commits, 1)

        # Determine productivity level
        if avg_loc_per_commit > 200 and avg_files_per_commit > 5:
            productivity_level = "High"
        elif avg_loc_per_commit > 100 and avg_files_per_commit > 3:
            productivity_level = "Medium"
        else:
            productivity_level = "Low"

        return {
            "level": productivity_level,
            "avg_loc_per_commit": avg_loc_per_commit,
            "avg_files_per_commit": avg_files_per_commit,
            "total_commits": total_commits,
            "total_loc": total_loc,
            "efficiency_score": min((avg_loc_per_commit / 200) * 100, 100),
        }

    def _generate_recommendations(
        self, stats: UnifiedStats, language_analysis: dict[str, Any]
    ) -> list[str]:
        """Generate personalized recommendations based on current state."""
        recommendations = []

        # Language diversity recommendations
        if len(language_analysis) < 3:
            recommendations.append(
                "Consider expanding language diversity for broader expertise"
            )

        # Technology stack recommendations
        frontend_techs = stats.tech_stack_analysis.get("frontend", {}).get(
            "technologies", []
        )
        backend_techs = stats.tech_stack_analysis.get("backend", {}).get(
            "technologies", []
        )

        if not frontend_techs:
            recommendations.append(
                "Consider adding frontend technologies to your stack"
            )

        if not backend_techs:
            recommendations.append("Consider adding backend technologies to your stack")

        # Modern technology recommendations
        modern_frontend = ["react", "vue", "angular", "nextjs", "nuxt"]
        if not any(tech in frontend_techs for tech in modern_frontend):
            recommendations.append("Consider learning a modern frontend framework")

        # DevOps recommendations
        devops_techs = stats.tech_stack_analysis.get("devops", {}).get(
            "technologies", []
        )
        if "docker" not in devops_techs:
            recommendations.append("Consider learning Docker for containerization")

        if not any(tech in devops_techs for tech in ["aws", "azure", "gcp"]):
            recommendations.append("Consider learning cloud platforms for deployment")

        return recommendations

    def _generate_predictions(self, stats: UnifiedStats) -> dict[str, Any]:
        """Generate predictions based on current patterns."""
        predictions = {
            "growth_forecast": self._predict_growth(stats),
            "technology_adoption": self._predict_technology_adoption(stats),
            "skill_development": self._predict_skill_development(stats),
        }
        return predictions

    def _predict_growth(self, stats: UnifiedStats) -> dict[str, Any]:
        """Predict growth based on current metrics."""
        current_velocity = stats.total_commits / max(
            stats.total_loc / 1000, 1
        )  # commits per 1k LOC

        if current_velocity > 10:
            growth_rate = "High"
            confidence = 85
        elif current_velocity > 5:
            growth_rate = "Medium"
            confidence = 70
        else:
            growth_rate = "Low"
            confidence = 60

        return {
            "rate": growth_rate,
            "confidence": confidence,
            "velocity": current_velocity,
            "estimated_next_month": int(stats.total_commits * 1.2),
        }

    def _predict_technology_adoption(self, stats: UnifiedStats) -> dict[str, Any]:
        """Predict likely technology adoptions."""
        current_techs = []
        for category in ["frontend", "backend", "database", "devops", "ai_ml"]:
            techs = stats.tech_stack_analysis.get(category, {}).get("technologies", [])
            current_techs.extend(techs)

        # Predict based on current stack
        predictions = []

        if "react" in current_techs and "nextjs" not in current_techs:
            predictions.append(
                {
                    "technology": "nextjs",
                    "probability": 80,
                    "reason": "Natural progression from React",
                }
            )

        if "python" in current_techs and "fastapi" not in current_techs:
            predictions.append(
                {
                    "technology": "fastapi",
                    "probability": 75,
                    "reason": "Modern Python web framework",
                }
            )

        if "docker" in current_techs and "kubernetes" not in current_techs:
            predictions.append(
                {
                    "technology": "kubernetes",
                    "probability": 70,
                    "reason": "Container orchestration",
                }
            )

        return {"predictions": predictions}

    def _predict_skill_development(self, stats: UnifiedStats) -> dict[str, Any]:
        """Predict skill development areas."""
        skill_areas = []

        # Analyze current strengths and weaknesses
        frontend_techs = stats.tech_stack_analysis.get("frontend", {}).get(
            "technologies", []
        )
        backend_techs = stats.tech_stack_analysis.get("backend", {}).get(
            "technologies", []
        )
        devops_techs = stats.tech_stack_analysis.get("devops", {}).get(
            "technologies", []
        )

        if len(frontend_techs) > len(backend_techs):
            skill_areas.append(
                {
                    "area": "Backend Development",
                    "priority": "High",
                    "reason": "Balance frontend/backend skills",
                }
            )

        if "docker" not in devops_techs:
            skill_areas.append(
                {
                    "area": "DevOps",
                    "priority": "Medium",
                    "reason": "Modern deployment practices",
                }
            )

        return {"skill_areas": skill_areas}

    def _get_frontend_recommendations(self, techs: list[str]) -> list[str]:
        """Get frontend-specific recommendations."""
        recommendations = []

        if not any(tech in techs for tech in ["react", "vue", "angular"]):
            recommendations.append("Learn a modern JavaScript framework")

        if "typescript" not in techs:
            recommendations.append("Consider TypeScript for better type safety")

        if not any(tech in techs for tech in ["tailwind", "bootstrap"]):
            recommendations.append("Learn a CSS framework for faster styling")

        return recommendations

    def _get_backend_recommendations(self, techs: list[str]) -> list[str]:
        """Get backend-specific recommendations."""
        recommendations = []

        if not any(tech in techs for tech in ["fastapi", "express", "django"]):
            recommendations.append("Learn a modern backend framework")

        if "postgres" not in techs and "mysql" not in techs:
            recommendations.append("Learn a relational database")

        return recommendations

    def _get_devops_recommendations(self, techs: list[str]) -> list[str]:
        """Get DevOps-specific recommendations."""
        recommendations = []

        if "docker" not in techs:
            recommendations.append("Learn Docker for containerization")

        if not any(tech in techs for tech in ["aws", "azure", "gcp"]):
            recommendations.append("Learn a cloud platform")

        if "githubactions" not in techs:
            recommendations.append("Set up CI/CD pipelines")

        return recommendations

    def _get_ai_ml_recommendations(self, techs: list[str]) -> list[str]:
        """Get AI/ML-specific recommendations."""
        recommendations = []

        if "sklearn" not in techs:
            recommendations.append("Learn scikit-learn for machine learning")

        if not any(tech in techs for tech in ["tensorflow", "pytorch"]):
            recommendations.append("Learn a deep learning framework")

        if "pandas" not in techs:
            recommendations.append("Learn pandas for data manipulation")

        return recommendations
