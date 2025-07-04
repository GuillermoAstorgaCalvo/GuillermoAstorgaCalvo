"""
Analytics Reporter for generating enhanced reports with historical trends and insights.
Generates markdown sections for growth tracking, velocity metrics, goal tracking, and trend visualization.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import math


class AnalyticsReporter:
    """Generates enhanced analytics reports with historical trends and insights."""
    
    def __init__(self):
        """Initialize the analytics reporter."""
        pass
    
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
    
    def generate_goal_tracking_section(self, goals: List[Any]) -> str:
        """
        Generate markdown section for goal tracking.
        
        Args:
            goals: List of goal progress objects (dict or GoalProgress)
            
        Returns:
            Markdown string for goal tracking section
        """
        if not goals:
            return ""
        
        markdown = "### 🎯 Goal Tracking\n\n"
        
        for goal in goals:
            # Convert to dict if needed
            if not isinstance(goal, dict):
                goal = goal.to_dict()
            # Create progress bar
            progress_bar = self._create_progress_bar(goal['percentage_complete'])
            
            # Determine status emoji
            if goal['percentage_complete'] >= 100:
                status_emoji = "✅"
            elif goal['percentage_complete'] >= 75:
                status_emoji = "🟡"
            elif goal['percentage_complete'] >= 50:
                status_emoji = "🟠"
            else:
                status_emoji = "🔴"
            
            markdown += f"#### {status_emoji} {goal['goal_name']}\n\n"
            markdown += f"**Progress:** {goal['current_value']:,} / {goal['target_value']:,} ({goal['percentage_complete']:.1f}%)\n\n"
            markdown += f"{progress_bar}\n\n"
            
            if goal['remaining'] > 0:
                markdown += f"**Remaining:** {goal['remaining']:,}\n\n"
            else:
                markdown += "**🎉 Goal Achieved!**\n\n"
            
            markdown += "---\n\n"
        
        return markdown
    
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
    
    def generate_insights_section(self, trends: Dict[str, Any], goals: List[Any]) -> str:
        """
        Generate insights and recommendations based on analytics data.
        
        Args:
            trends: Trend analysis data
            goals: Goal progress data (dict or GoalProgress)
            
        Returns:
            Markdown string for insights section
        """
        markdown = "### 💡 Insights & Recommendations\n\n"
        
        # Convert goals to dicts if needed
        goals_dicts = [g if isinstance(g, dict) else g.to_dict() for g in goals]
        
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
        
        # Analyze goal progress
        completed_goals = [g for g in goals_dicts if g['percentage_complete'] >= 100]
        near_completion = [g for g in goals_dicts if 75 <= g['percentage_complete'] < 100]
        
        if completed_goals:
            insights.append(f"🎉 **{len(completed_goals)} goal(s) achieved!** - Great progress!")
        
        if near_completion:
            insights.append(f"🎯 **{len(near_completion)} goal(s) near completion** - Keep up the momentum!")
        
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
        
        # Add recommendations
        markdown += "#### 📋 Recommendations\n\n"
        markdown += "- 📈 **Continue tracking** - More data points will provide better insights\n"
        markdown += "- 🎯 **Set new goals** - Consider setting stretch targets based on current velocity\n"
        markdown += "- 📊 **Monitor trends** - Watch for patterns in development activity\n"
        markdown += "- 🔄 **Regular reviews** - Weekly analytics reviews can help maintain momentum\n\n"
        
        return markdown
    
    def generate_analytics_summary(self, trends: Dict[str, Any], goals: List[Any]) -> str:
        """
        Generate a comprehensive analytics summary.
        
        Args:
            trends: Trend analysis data
            goals: Goal progress data (dict or GoalProgress)
            
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
        
        # Add goal tracking
        markdown += self.generate_goal_tracking_section(goals)
        
        # Add trend visualization
        markdown += self.generate_trend_visualization_section(trends)
        
        # Add insights
        markdown += self.generate_insights_section(trends, goals)
        
        return markdown


def get_analytics_reporter() -> AnalyticsReporter:
    """
    Factory function to create and return an AnalyticsReporter instance.
    
    Returns:
        AnalyticsReporter instance
    """
    return AnalyticsReporter() 