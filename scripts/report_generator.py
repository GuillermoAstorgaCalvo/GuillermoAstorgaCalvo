"""
Report Generator Module
Handles generation of markdown reports from statistics data.
"""

from datetime import datetime
from typing import Dict, Any
from stats_processor import UnifiedStats, AuthorStats
from analytics_manager import get_analytics_manager
from analytics_reporter import get_analytics_reporter


class MarkdownReportGenerator:
    """Generates markdown reports from unified statistics."""
    
    def __init__(self, title: str = "📊 Unified Code Statistics", 
                 date_format: str = "%B %d, %Y at %H:%M UTC"):
        """
        Initialize the report generator.
        
        Args:
            title: Report title
            date_format: Date format string for timestamps
        """
        self.title = title
        self.date_format = date_format
        self.months_en = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August', 
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
    
    def format_timestamp(self, dt: datetime = None) -> str:
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
    
    def calculate_distribution_percentages(self, stats: AuthorStats, totals: AuthorStats) -> tuple:
        """
        Calculate distribution percentages.
        
        Args:
            stats: Author statistics
            totals: Total repository statistics
            
        Returns:
            Tuple of (loc_pct, commits_pct, files_pct)
        """
        loc_pct = (stats.loc / totals.loc * 100) if totals.loc > 0 else 0
        commits_pct = (stats.commits / totals.commits * 100) if totals.commits > 0 else 0
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
            stats: Unified statistics data
            
        Returns:
            Markdown string for global summary
        """
        summary = "## 🔍 Global Summary\n\n"
        summary += f"- **Repositories processed:** {stats.repos_processed}\n"
        summary += f"- **Total commits:** {self.format_number(stats.total_commits)}\n"
        summary += f"- **Total files:** {self.format_number(stats.total_files)}\n"
        summary += f"- **Total lines of code:** {self.format_number(stats.total_loc)}\n\n"
        
        return summary
    
    def generate_contributions_table(self, stats: UnifiedStats) -> str:
        """
        Generate the contributions table section.
        
        Args:
            stats: Unified statistics data
            
        Returns:
            Markdown string for contributions table
        """
        table = "## 👨‍💻 Contributions by Repository and Author\n\n"
        table += "| Repository | Author | Lines | Commits | Files | Distribution % |\n"
        table += "|:-----------|:-------|------:|--------:|------:|:---------------|\n"
        
        # Calculate global distribution percentages
        guillermo = stats.guillermo_unified
        global_totals = AuthorStats(
            loc=stats.total_loc,
            commits=stats.total_commits,
            files=stats.total_files
        )
        
        loc_pct, commits_pct, files_pct = self.calculate_distribution_percentages(
            guillermo, global_totals
        )
        
        # Add unified total row
        table += f"| **🌟 TOTAL UNIFIED** | **Guillermo** | "
        table += f"**{self.format_number(guillermo.loc)}** | "
        table += f"**{self.format_number(guillermo.commits)}** | "
        table += f"**{self.format_number(guillermo.files)}** | "
        table += f"**{self.format_percentage(loc_pct)}/{self.format_percentage(commits_pct)}/{self.format_percentage(files_pct)}** |\n"
        
        # Add separator row
        table += "| | | | | | |\n"
        
        # Sort repositories in specific order: Frontend, Backend, AI Backend
        def get_repo_order_key(repo_name):
            """Get sorting key to ensure specific repository order."""
            repo_name_lower = repo_name.lower()
            if 'frontend' in repo_name_lower:
                return 1  # First
            elif 'backend' in repo_name_lower and 'ai' not in repo_name_lower:
                return 2  # Second
            elif 'ai' in repo_name_lower:
                return 3  # Third
            else:
                return 4  # Any others last
        
        # Sort repositories by the defined order
        sorted_repos = sorted(
            stats.repo_breakdown.items(),
            key=lambda x: get_repo_order_key(x[0])
        )
        
        # Add individual repository rows in sorted order
        for repo_name, repo_data in sorted_repos:
            g_stats = repo_data.guillermo_stats
            repo_totals = repo_data.repo_totals
            
            # Calculate repository-specific percentages
            repo_loc_pct, repo_commits_pct, repo_files_pct = self.calculate_distribution_percentages(
                g_stats, repo_totals
            )
            
            table += f"| 📁 **{repo_name}** | Guillermo | "
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
            key=lambda x: x[1]['loc'],
            reverse=True
        )
        
        total_loc = stats.total_loc
        
        for language, lang_stats in sorted_languages:
            loc = lang_stats['loc']
            commits = lang_stats['commits']
            files = lang_stats['files']
            
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
            'Python': '🐍',
            'JavaScript': '🟨',
            'TypeScript': '🔷',
            'Java': '☕',
            'C': '🔵',
            'C++': '🔵',
            'C#': '💜',
            'PHP': '🐘',
            'Ruby': '💎',
            'Go': '🐹',
            'Rust': '🦀',
            'Swift': '🍎',
            'Kotlin': '🟠',
            'Scala': '🔴',
            'HTML': '🌐',
            'CSS': '🎨',
            'Shell': '🐚',
            'PowerShell': '💻',
            'SQL': '🗄️',
            'R': '📊',
            'MATLAB': '📈',
            'Julia': '🔬',
            'Dart': '🎯',
            'Lua': '🌙',
            'Perl': '🐪',
            'Haskell': 'λ',
            'Clojure': '🍃',
            'Elixir': '💧',
            'Erlang': '☎️',
            'OCaml': '🐫',
            'F#': '🔷',
            'Assembly': '⚙️',
            'VHDL': '🔌',
            'Verilog': '🔌',
            'TeX': '📝',
            'Markdown': '📄',
            'YAML': '📋',
            'JSON': '📄',
            'XML': '📄',
            'CSV': '📊',
            'Dockerfile': '🐳',
            'Makefile': '🔨',
            'CMake': '🔨',
            'Gradle': '🔨',
            'Maven': '🔨',
            'Documentation': '📚',
            'Configuration': '⚙️',
            'Data': '📊',
            'Assets': '🎨',
            'Unknown': '❓'
        }
        
        return language_emojis.get(language, '📄')
    
    def generate_footer(self) -> str:
        """Generate the report footer."""
        footer = "\n---\n"
        footer += "*Generated automatically by GitHub Actions*"
        
        return footer
    
    def generate_report(self, stats: UnifiedStats, config: Dict[str, Any] = None) -> str:
        """
        Generate the complete markdown report.
        
        Args:
            stats: Unified statistics data
            config: Configuration dictionary for analytics
            
        Returns:
            Complete markdown report string
        """
        report = ""
        report += self.generate_header()
        report += self.generate_global_summary(stats)
        report += self.generate_contributions_table(stats)
        
        # Debug: Check if language stats exist
        if hasattr(stats, 'unified_language_stats') and stats.unified_language_stats:
            print(f"✅ Language stats found: {len(stats.unified_language_stats)} languages")
            for lang, stats_data in stats.unified_language_stats.items():
                print(f"  - {lang}: {stats_data['loc']} LOC")
        else:
            print("⚠️ No language stats found in unified stats")
        
        report += self.generate_language_breakdown_table(stats)
        
        # Add analytics section if enabled
        if config and config.get('analytics', {}).get('track_history', False):
            try:
                # Initialize analytics
                analytics_manager = get_analytics_manager()
                analytics_reporter = get_analytics_reporter()
                
                # Convert stats to dictionary format for analytics
                stats_dict = {
                    'total_loc': stats.total_loc,
                    'total_commits': stats.total_commits,
                    'total_files': stats.total_files,
                    'guillermo_unified': {
                        'loc': stats.guillermo_unified.loc,
                        'commits': stats.guillermo_unified.commits,
                        'files': stats.guillermo_unified.files
                    },
                    'repos_processed': stats.repos_processed,
                    'unified_language_stats': stats.unified_language_stats
                }
                
                # Add current data point to history
                analytics_manager.add_data_point(stats_dict)
                
                # Get trend analysis
                trends = analytics_manager.get_trend_analysis()
                
                # Track language usage
                language_config = config.get('analytics', {}).get('language_usage', {})
                language_analysis = analytics_manager.track_language_usage(stats_dict, language_config)
                
                # Generate analytics report
                analytics_section = analytics_reporter.generate_analytics_summary(trends, language_analysis)
                report += analytics_section
                
                # Cleanup old data
                retention_days = config.get('analytics', {}).get('retention_days', 90)
                analytics_manager.cleanup_old_data(retention_days)
                
            except Exception as e:
                print(f"⚠️ Analytics error: {e}")
                report += "\n### 📊 Analytics\n\n⚠️ Analytics temporarily unavailable.\n\n"
        
        report += self.generate_footer()
        
        return report
    
    def save_report(self, stats: UnifiedStats, filename: str = "STATS.md", config: Dict[str, Any] = None) -> None:
        """
        Generate and save a markdown report to file.
        
        Args:
            stats: Unified statistics data
            filename: Output filename
            config: Configuration dictionary for analytics
        """
        report = self.generate_report(stats, config)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)


class JSONReportGenerator:
    """Generates JSON reports from unified statistics."""
    
    def __init__(self):
        """Initialize the JSON report generator."""
        pass
    
    def generate_report(self, stats: UnifiedStats) -> Dict[str, Any]:
        """
        Generate a JSON report from unified statistics.
        
        Args:
            stats: Unified statistics data
            
        Returns:
            Dictionary representation of the statistics
        """
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'global_summary': {
                'repositories_processed': stats.repos_processed,
                'total_commits': stats.total_commits,
                'total_files': stats.total_files,
                'total_loc': stats.total_loc
            },
            'guillermo_unified': stats.guillermo_unified.to_dict(),
            'repository_breakdown': {},
            'language_breakdown': stats.unified_language_stats
        }
        
        # Add repository breakdown
        for repo_name, repo_data in stats.repo_breakdown.items():
            report['repository_breakdown'][repo_name] = repo_data.to_dict()
        
        return report
    
    def save_report(self, stats: UnifiedStats, filename: str = "stats.json") -> None:
        """
        Generate and save a JSON report to file.
        
        Args:
            stats: Unified statistics data
            filename: Output filename
        """
        import json
        
        report = self.generate_report(stats)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False) 