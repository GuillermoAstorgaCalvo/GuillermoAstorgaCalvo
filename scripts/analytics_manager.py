"""
Analytics Manager for Historical Trends and Time Series Analysis
Handles growth tracking, velocity metrics, goal tracking, and trend visualization.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics


@dataclass
class HistoricalDataPoint:
    """Represents a single data point in historical tracking."""
    timestamp: str
    total_loc: int
    total_commits: int
    total_files: int
    guillermo_loc: int
    guillermo_commits: int
    guillermo_files: int
    repos_processed: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class VelocityMetrics:
    """Represents velocity metrics for a time period."""
    period: str
    start_date: str
    end_date: str
    loc_change: int
    commits_change: int
    files_change: int
    loc_velocity: float  # LOC per day
    commits_velocity: float  # Commits per day
    files_velocity: float  # Files per day
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class GoalProgress:
    """Represents progress towards a specific goal."""
    goal_name: str
    current_value: int
    target_value: int
    percentage_complete: float
    remaining: int
    estimated_completion: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class AnalyticsManager:
    """Manages historical analytics, velocity metrics, and goal tracking."""
    
    def __init__(self, history_file: str = "analytics_history.json"):
        """
        Initialize the analytics manager.
        
        Args:
            history_file: Path to the historical data file
        """
        self.history_file = Path(history_file)
        self.history_data: List[HistoricalDataPoint] = []
        self.load_history()
    
    def load_history(self) -> None:
        """Load historical data from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history_data = [
                        HistoricalDataPoint(**point) for point in data
                    ]
        except Exception as e:
            print(f"⚠️ Could not load historical data: {e}")
            self.history_data = []
    
    def save_history(self) -> None:
        """Save historical data to file."""
        try:
            data = [point.to_dict() for point in self.history_data]
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Could not save historical data: {e}")
    
    def add_data_point(self, stats: Dict[str, Any]) -> None:
        """
        Add a new data point to the historical tracking.
        
        Args:
            stats: Current statistics dictionary
        """
        data_point = HistoricalDataPoint(
            timestamp=datetime.utcnow().isoformat() + 'Z',
            total_loc=stats.get('total_loc', 0),
            total_commits=stats.get('total_commits', 0),
            total_files=stats.get('total_files', 0),
            guillermo_loc=stats.get('guillermo_unified', {}).get('loc', 0),
            guillermo_commits=stats.get('guillermo_unified', {}).get('commits', 0),
            guillermo_files=stats.get('guillermo_unified', {}).get('files', 0),
            repos_processed=stats.get('repos_processed', 0)
        )
        
        self.history_data.append(data_point)
        self.save_history()
    
    def get_growth_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Calculate growth trends over the specified period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with growth metrics
        """
        if len(self.history_data) < 2:
            return {"error": "Insufficient historical data"}
        
        # Get data points within the specified period
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_data = [
            point for point in self.history_data
            if datetime.fromisoformat(point.timestamp.replace('Z', '+00:00')).replace(tzinfo=None) > cutoff_date
        ]
        
        if len(recent_data) < 2:
            return {"error": "Insufficient data in specified period"}
        
        # Calculate growth metrics
        first_point = recent_data[0]
        last_point = recent_data[-1]
        
        growth_metrics = {
            'period_days': days,
            'data_points': len(recent_data),
            'total_loc': {
                'start': first_point.total_loc,
                'end': last_point.total_loc,
                'growth': last_point.total_loc - first_point.total_loc,
                'growth_percentage': ((last_point.total_loc - first_point.total_loc) / first_point.total_loc * 100) if first_point.total_loc > 0 else 0
            },
            'total_commits': {
                'start': first_point.total_commits,
                'end': last_point.total_commits,
                'growth': last_point.total_commits - first_point.total_commits,
                'growth_percentage': ((last_point.total_commits - first_point.total_commits) / first_point.total_commits * 100) if first_point.total_commits > 0 else 0
            },
            'guillermo_loc': {
                'start': first_point.guillermo_loc,
                'end': last_point.guillermo_loc,
                'growth': last_point.guillermo_loc - first_point.guillermo_loc,
                'growth_percentage': ((last_point.guillermo_loc - first_point.guillermo_loc) / first_point.guillermo_loc * 100) if first_point.guillermo_loc > 0 else 0
            },
            'guillermo_commits': {
                'start': first_point.guillermo_commits,
                'end': last_point.guillermo_commits,
                'growth': last_point.guillermo_commits - first_point.guillermo_commits,
                'growth_percentage': ((last_point.guillermo_commits - first_point.guillermo_commits) / first_point.guillermo_commits * 100) if first_point.guillermo_commits > 0 else 0
            }
        }
        
        return growth_metrics
    
    def calculate_velocity_metrics(self, period: str = "weekly") -> List[VelocityMetrics]:
        """
        Calculate velocity metrics for the specified period.
        
        Args:
            period: Time period ("weekly", "monthly", "quarterly")
            
        Returns:
            List of velocity metrics
        """
        if len(self.history_data) < 2:
            return []
        
        # Sort data points by timestamp
        sorted_data = sorted(self.history_data, key=lambda x: x.timestamp)
        
        velocity_metrics = []
        
        # Group data by period
        if period == "weekly":
            group_days = 7
        elif period == "monthly":
            group_days = 30
        elif period == "quarterly":
            group_days = 90
        else:
            return []
        
        # Calculate velocity for each period
        for i in range(len(sorted_data) - 1):
            current = sorted_data[i]
            next_point = sorted_data[i + 1]
            
            # Calculate time difference in days
            current_date = datetime.fromisoformat(current.timestamp.replace('Z', '+00:00')).replace(tzinfo=None)
            next_date = datetime.fromisoformat(next_point.timestamp.replace('Z', '+00:00')).replace(tzinfo=None)
            days_diff = (next_date - current_date).days
            
            if days_diff > 0:
                velocity = VelocityMetrics(
                    period=period,
                    start_date=current.timestamp,
                    end_date=next_point.timestamp,
                    loc_change=next_point.total_loc - current.total_loc,
                    commits_change=next_point.total_commits - current.total_commits,
                    files_change=next_point.total_files - current.total_files,
                    loc_velocity=(next_point.total_loc - current.total_loc) / days_diff,
                    commits_velocity=(next_point.total_commits - current.total_commits) / days_diff,
                    files_velocity=(next_point.total_files - current.total_files) / days_diff
                )
                velocity_metrics.append(velocity)
        
        return velocity_metrics
    
    def track_goals(self, current_stats: Dict[str, Any], goals_config: Dict[str, Any]) -> List[GoalProgress]:
        """
        Track progress towards configured goals.
        
        Args:
            current_stats: Current statistics
            goals_config: Goals configuration from config file
            
        Returns:
            List of goal progress objects
        """
        if not goals_config.get('enabled', False):
            return []
        
        goals = []
        targets = goals_config.get('targets', {})
        milestones = goals_config.get('milestones', [])
        
        # Track basic targets
        for metric, target in targets.items():
            current_value = self._get_current_value(current_stats, metric)
            if current_value is not None:
                progress = GoalProgress(
                    goal_name=f"{metric.replace('_', ' ').title()}",
                    current_value=current_value,
                    target_value=target,
                    percentage_complete=(current_value / target * 100) if target > 0 else 0,
                    remaining=max(0, target - current_value)
                )
                goals.append(progress)
        
        # Track milestones
        for milestone in milestones:
            metric = milestone.get('metric')
            target = milestone.get('target')
            name = milestone.get('name')
            
            if metric and target:
                current_value = self._get_current_value(current_stats, metric)
                if current_value is not None:
                    progress = GoalProgress(
                        goal_name=name,
                        current_value=current_value,
                        target_value=target,
                        percentage_complete=(current_value / target * 100) if target > 0 else 0,
                        remaining=max(0, target - current_value)
                    )
                    goals.append(progress)
        
        return goals
    
    def _get_current_value(self, stats: Dict[str, Any], metric: str) -> Optional[int]:
        """Extract current value for a given metric."""
        if metric == 'total_loc':
            return stats.get('total_loc', 0)
        elif metric == 'total_commits':
            return stats.get('total_commits', 0)
        elif metric == 'total_files':
            return stats.get('total_files', 0)
        elif metric == 'guillermo_loc':
            return stats.get('guillermo_unified', {}).get('loc', 0)
        elif metric == 'guillermo_commits':
            return stats.get('guillermo_unified', {}).get('commits', 0)
        elif metric == 'guillermo_files':
            return stats.get('guillermo_unified', {}).get('files', 0)
        else:
            return None
    
    def get_trend_analysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive trend analysis.
        
        Returns:
            Dictionary with trend analysis results
        """
        if len(self.history_data) < 3:
            return {"error": "Insufficient data for trend analysis"}
        
        # Calculate trends for different periods
        trends = {
            'weekly': self.get_growth_trends(7),
            'monthly': self.get_growth_trends(30),
            'quarterly': self.get_growth_trends(90),
            'velocity': {
                'weekly': self.calculate_velocity_metrics("weekly"),
                'monthly': self.calculate_velocity_metrics("monthly")
            }
        }
        
        return trends
    
    def cleanup_old_data(self, retention_days: int = 90) -> None:
        """
        Remove historical data older than the specified retention period.
        
        Args:
            retention_days: Number of days to retain
        """
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        self.history_data = [
            point for point in self.history_data
            if datetime.fromisoformat(point.timestamp.replace('Z', '+00:00')).replace(tzinfo=None) > cutoff_date
        ]
        
        self.save_history()


def get_analytics_manager(history_file: str = "analytics_history.json") -> AnalyticsManager:
    """
    Factory function to create and return an AnalyticsManager instance.
    
    Args:
        history_file: Path to the historical data file
        
    Returns:
        AnalyticsManager instance
    """
    return AnalyticsManager(history_file) 