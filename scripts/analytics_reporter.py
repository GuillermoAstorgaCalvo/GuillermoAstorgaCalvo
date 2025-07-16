"""
Analytics Reporter for generating enhanced reports with historical trends and insights.
Generates markdown sections for growth tracking, velocity metrics, goal tracking, and trend visualization.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import math
import json
import logging

logger = logging.getLogger(__name__)


class AnalyticsReporter:
    """Generates enhanced analytics reports with historical trends and insights."""
    
    def generate_growth_trends_section(self, trends: Dict[str, Any]) -> str:
        """
        Generate markdown section for growth trends.
        
        Args:
            trends: Growth trends data from AnalyticsManager
            
        Returns:
            Markdown string for growth trends section
        """
        if "error" in trends:
            return f"### 📈 Growth Trends\n\n⚠️ {trends['error']}\n\n"
        
        markdown = "### 📈 Growth Trends\n\n"
        
        # Weekly trends
        if 'weekly' in trends and 'error' not in trends['weekly']:
            weekly = trends['weekly']
            markdown += "#### 🗓️ Weekly Growth (7 days)\n\n"
            markdown += self._format_growth_metrics(weekly)
        
        # Monthly trends
        if 'monthly' in trends and 'error' not in trends['monthly']:
            monthly = trends['monthly']
            markdown += "#### 📅 Monthly Growth (30 days)\n\n"
            markdown += self._format_growth_metrics(monthly)
        
        # Quarterly trends
        if 'quarterly' in trends and 'error' not in trends['quarterly']:
            quarterly = trends['quarterly']
            markdown += "#### 📊 Quarterly Growth (90 days)\n\n"
            markdown += self._format_growth_metrics(quarterly)
        
        return markdown
    
    def _format_growth_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format growth metrics into a markdown table."""
        markdown = "| Metric | Start | End | Growth | Growth % |\n"
        markdown += "|--------|-------|-----|--------|----------|\n"
        
        for metric_name, data in metrics.items():
            if isinstance(data, dict) and 'start' in data:
                start = data['start']
                end = data['end']
                growth = data['growth']
                growth_pct = data['growth_percentage']
                
                # Format the metric name
                display_name = metric_name.replace('_', ' ').title()
                
                # Add emoji based on growth
                emoji = "📈" if growth >= 0 else "📉"
                
                markdown += f"| {emoji} {display_name} | {start:,} | {end:,} | {growth:+,} | {growth_pct:+.1f}% |\n"
        
        markdown += "\n"
        return markdown
    
    def generate_velocity_metrics_section(self, velocity_data: Dict[str, Any]) -> str:
        """
        Generate markdown section for velocity metrics.
        
        Args:
            velocity_data: Velocity metrics data from AnalyticsManager
            
        Returns:
            Markdown string for velocity metrics section
        """
        markdown = "### ⚡ Velocity Metrics\n\n"
        
        for period, metrics in velocity_data.items():
            if not metrics:
                continue
            
            markdown += f"#### 📊 {period.title()} Velocity\n\n"
            markdown += "| Period | LOC/Day | Commits/Day | Files/Day |\n"
            markdown += "|--------|---------|-------------|-----------|\n"
            
            for metric in metrics[-5:]:  # Show last 5 periods
                start_date = datetime.fromisoformat(metric.start_date.replace('Z', '+00:00')).replace(tzinfo=None)
                end_date = datetime.fromisoformat(metric.end_date.replace('Z', '+00:00')).replace(tzinfo=None)
                period_str = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
                
                markdown += f"| {period_str} | {metric.loc_velocity:.1f} | {metric.commits_velocity:.1f} | {metric.files_velocity:.1f} |\n"
            
            markdown += "\n"
        
        return markdown
    
    def generate_language_usage_section(self, language_analysis: Dict[str, Any]) -> str:
        """
        Generate markdown section for language usage analysis.
        
        Args:
            language_analysis: Language usage analysis data
            
        Returns:
            Markdown string for language usage section
        """
        if not language_analysis:
            return ""
        
        markdown = "### 🔤 Language Usage Analysis\n\n"
        
        # Summary stats
        total_languages = language_analysis.get('total_languages', 0)
        total_loc = language_analysis.get('total_loc', 0)
        
        markdown += f"**📊 Summary:** {total_languages} languages detected across {total_loc:,} lines of code\n\n"
        
        # Top languages table
        top_languages = language_analysis.get('top_languages', [])
        if top_languages:
            markdown += "#### 🏆 Top Languages by Lines of Code\n\n"
            markdown += "| Rank | Language | Lines | Commits | Files | % of Total |\n"
            markdown += "|:-----|:---------|------:|--------:|------:|:-----------|\n"
            
            for i, lang_data in enumerate(top_languages, 1):
                language = lang_data['language']
                
                # Skip unwanted languages
                if language in ['Unknown', 'Assets', 'HTML']:
                    continue
                
                loc = lang_data['loc']
                commits = lang_data['commits']
                files = lang_data['files']
                percentage = lang_data['percentage']
                
                # Get language emoji
                emoji = self._get_language_emoji(language)
                
                markdown += f"| {i} | {emoji} **{language}** | {loc:,} | {commits:,} | {files:,} | {percentage:.1f}% |\n"
            
            markdown += "\n"
        
        # Language distribution insights
        markdown += "#### 💡 Language Insights\n\n"
        
        if top_languages:
            primary_lang = top_languages[0]
            primary_percentage = primary_lang['percentage']
            
            if primary_percentage > 50:
                markdown += f"🎯 **{primary_lang['language']} dominates** with {primary_percentage:.1f}% of all code\n\n"
            elif primary_percentage > 30:
                markdown += f"📈 **{primary_lang['language']} is primary** with {primary_percentage:.1f}% of codebase\n\n"
            else:
                markdown += f"🔄 **Diverse codebase** - {primary_lang['language']} leads with {primary_percentage:.1f}%\n\n"
            
            # Show top 3 languages
            if len(top_languages) >= 3:
                top3 = top_languages[:3]
                markdown += "**Top 3 Languages:**\n"
                for i, lang in enumerate(top3, 1):
                    markdown += f"- {i}. {lang['language']} ({lang['percentage']:.1f}%)\n"
                markdown += "\n"
        
        return markdown
    
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
    
    def _create_progress_bar(self, percentage: float) -> str:
        """Create a visual progress bar for goal tracking."""
        bar_length = 20
        filled_length = int(bar_length * percentage / 100)
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"`{bar}` {percentage:.1f}%"
    
    def generate_trend_visualization_section(self, trends: Dict[str, Any]) -> str:
        """
        Generate markdown section with trend visualizations.
        
        Args:
            trends: Comprehensive trend analysis data
            
        Returns:
            Markdown string for trend visualization section
        """
        markdown = "### 📊 Trend Visualization\n\n"
        
        # Generate simple ASCII charts for key metrics
        if 'monthly' in trends and 'error' not in trends['monthly']:
            monthly = trends['monthly']
            
            # LOC trend chart
            if 'total_loc' in monthly:
                loc_data = monthly['total_loc']
                markdown += "#### 📈 Lines of Code Trend\n\n"
                markdown += self._create_simple_chart(
                    loc_data['start'], 
                    loc_data['end'], 
                    "LOC"
                )
                markdown += "\n"
            
            # Commits trend chart
            if 'total_commits' in monthly:
                commits_data = monthly['total_commits']
                markdown += "#### 🔄 Commits Trend\n\n"
                markdown += self._create_simple_chart(
                    commits_data['start'], 
                    commits_data['end'], 
                    "Commits"
                )
                markdown += "\n"
        
        return markdown
    
    def _create_simple_chart(self, start_value: int, end_value: int, label: str) -> str:
        """Create a simple ASCII chart showing growth trend."""
        if start_value == 0:
            return f"⚠️ No baseline data for {label}\n\n"
        
        growth_ratio = end_value / start_value if start_value > 0 else 1
        
        # Create a simple bar representation
        if growth_ratio >= 2:
            trend = "📈 Strong Growth"
            bars = "████████████████████"
        elif growth_ratio >= 1.5:
            trend = "📈 Good Growth"
            bars = "████████████████░░░░"
        elif growth_ratio >= 1.1:
            trend = "📈 Moderate Growth"
            bars = "████████████░░░░░░░░"
        elif growth_ratio >= 0.9:
            trend = "➡️ Stable"
            bars = "████████░░░░░░░░░░░░"
        else:
            trend = "📉 Decline"
            bars = "████░░░░░░░░░░░░░░░░"
        
        markdown = f"**{trend}**\n\n"
        markdown += f"`{bars}`\n\n"
        markdown += f"**Start:** {start_value:,} | **End:** {end_value:,} | **Growth:** {((growth_ratio - 1) * 100):+.1f}%\n\n"
        
        return markdown
    
    def generate_insights_section(self, trends: Dict[str, Any], language_analysis: Dict[str, Any]) -> str:
        """
        Generate insights and recommendations based on analytics data.
        
        Args:
            trends: Trend analysis data
            language_analysis: Language usage analysis data
            
        Returns:
            Markdown string for insights section
        """
        markdown = "### 💡 Insights & Recommendations\n\n"
        
        insights = []
        
        # Analyze growth trends
        if 'monthly' in trends and 'error' not in trends['monthly']:
            monthly = trends['monthly']
            
            # LOC growth insight
            if 'total_loc' in monthly:
                loc_growth = monthly['total_loc']['growth_percentage']
                if loc_growth > 20:
                    insights.append("🚀 **Strong code growth detected** - Excellent development velocity!")
                elif loc_growth > 10:
                    insights.append("📈 **Good code growth** - Maintaining steady development pace.")
                elif loc_growth < 0:
                    insights.append("⚠️ **Code reduction detected** - Consider if this is intentional refactoring.")
            
            # Commits growth insight
            if 'total_commits' in monthly:
                commits_growth = monthly['total_commits']['growth_percentage']
                if commits_growth > 30:
                    insights.append("⚡ **High commit frequency** - Great development activity!")
                elif commits_growth < 5:
                    insights.append("📝 **Low commit activity** - Consider more frequent commits.")
        
        # Analyze language usage
        if language_analysis:
            total_languages = language_analysis.get('total_languages', 0)
            top_languages = language_analysis.get('top_languages', [])
            
            if total_languages > 10:
                insights.append(f"🌍 **Diverse tech stack** - {total_languages} languages detected!")
            elif total_languages > 5:
                insights.append(f"🔄 **Multi-language project** - {total_languages} languages in use")
            
            if top_languages:
                primary_lang = top_languages[0]
                primary_percentage = primary_lang['percentage']
                
                if primary_percentage > 70:
                    insights.append(f"🎯 **{primary_lang['language']} focused** - {primary_percentage:.1f}% of codebase")
                elif primary_percentage < 30:
                    insights.append("🔄 **Balanced codebase** - Good language distribution")
        
        # Velocity insights
        if 'velocity' in trends:
            velocity = trends['velocity']
            if 'weekly' in velocity and velocity['weekly']:
                recent_velocity = velocity['weekly'][-1] if velocity['weekly'] else None
                if recent_velocity:
                    if recent_velocity.loc_velocity > 100:
                        insights.append("⚡ **High development velocity** - Excellent productivity!")
                    elif recent_velocity.loc_velocity < 10:
                        insights.append("🐌 **Low development velocity** - Consider increasing activity.")
        
        # Generate insights
        if insights:
            for insight in insights:
                markdown += f"{insight}\n\n"
        else:
            markdown += "📊 **Baseline established** - Continue tracking for meaningful insights.\n\n"
        
        # Recommendations section removed as requested
        
        return markdown
    
    def generate_analytics_summary(self, trends: Dict[str, Any], language_analysis: Dict[str, Any]) -> str:
        """
        Generate a comprehensive analytics summary.
        
        Args:
            trends: Trend analysis data
            language_analysis: Language usage analysis data
            
        Returns:
            Complete analytics report as markdown
        """
        markdown = "## 📊 Enhanced Analytics & Insights\n\n"
        markdown += f"*Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}*\n\n"
        
        # Add growth trends
        markdown += self.generate_growth_trends_section(trends)
        
        # Add velocity metrics
        if 'velocity' in trends:
            markdown += self.generate_velocity_metrics_section(trends['velocity'])
        
        # Add language usage analysis
        markdown += self.generate_language_usage_section(language_analysis)
        
        # Add trend visualization
        markdown += self.generate_trend_visualization_section(trends)
        
        # Add insights
        markdown += self.generate_insights_section(trends, language_analysis)
        
        return markdown


def load_analytics_data() -> Dict[str, Any]:
    """Load analytics data from JSON files."""
    try:
        analytics_data = {}
        
        # Load unified stats
        try:
            with open('unified_stats.json', 'r', encoding='utf-8') as f:
                analytics_data['unified_stats'] = json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            logger.warning(f"Could not read unified_stats.json: {e}")
            analytics_data['unified_stats'] = {}
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Invalid JSON in unified_stats.json: {e}")
            analytics_data['unified_stats'] = {}
        except (OSError, IOError) as e:
            logger.error(f"IO error reading unified_stats.json: {e}")
            analytics_data['unified_stats'] = {}
        
        # Load analytics history
        try:
            with open('analytics_history.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    analytics_data['analytics_history'] = data
                else:
                    logger.warning("analytics_history.json does not contain a list")
                    analytics_data['analytics_history'] = []
        except (FileNotFoundError, PermissionError) as e:
            logger.warning(f"Could not read analytics_history.json: {e}")
            analytics_data['analytics_history'] = []
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Invalid JSON in analytics_history.json: {e}")
            analytics_data['analytics_history'] = []
        except (OSError, IOError) as e:
            logger.error(f"IO error reading analytics_history.json: {e}")
            analytics_data['analytics_history'] = []
        
        return analytics_data
        
    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error loading analytics data: {e}")
        return {}

def generate_analytics_report(data: Dict[str, Any]) -> str:
    """Generate analytics report from data."""
    try:
        report = "# 📊 Analytics Report\n\n"
        
        # Add timestamp
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add unified stats summary
        unified_stats = data.get('unified_stats', {})
        if unified_stats:
            report += "## 📈 Current Statistics\n\n"
            report += f"- **Total Lines of Code:** {unified_stats.get('total_loc', 0):,}\n"
            report += f"- **Total Commits:** {unified_stats.get('total_commits', 0):,}\n"
            report += f"- **Total Files:** {unified_stats.get('total_files', 0):,}\n"
            report += f"- **Repositories Processed:** {unified_stats.get('repos_processed', 0)}\n\n"
        
        # Add analytics history summary
        analytics_history = data.get('analytics_history', [])
        if analytics_history:
            report += "## 📊 Historical Trends\n\n"
            report += f"- **Data Points:** {len(analytics_history)}\n"
            
            if len(analytics_history) >= 2:
                first_point = analytics_history[0]
                last_point = analytics_history[-1]
                
                try:
                    first_date = datetime.fromisoformat(first_point.get('timestamp', '').replace('Z', '+00:00'))
                    last_date = datetime.fromisoformat(last_point.get('timestamp', '').replace('Z', '+00:00'))
                    days_span = (last_date - first_date).days
                    report += f"- **Time Span:** {days_span} days\n"
                except (ValueError, TypeError, KeyError) as e:
                    logger.warning(f"Error parsing timestamps: {e}")
        
        return report
        
    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error generating analytics report: {e}")
        return "# 📊 Analytics Report\n\n*Error generating report*\n\n"
    except (ValueError, OSError) as e:
        logger.error(f"Error processing analytics data: {e}")
        return "# 📊 Analytics Report\n\n*Error processing data*\n\n"

def save_report(report: str, output_file: str = "analytics_report.md") -> bool:
    """Save analytics report to file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Analytics report saved to {output_file}")
        return True
        
    except (PermissionError, OSError) as e:
        logger.error(f"Could not write to {output_file}: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Error writing report content: {e}")
        return False
    except IOError as e:
        logger.error(f"IO error writing {output_file}: {e}")
        return False 