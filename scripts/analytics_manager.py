"""
Analytics Manager for Historical Trends and Time Series Analysis
Handles growth tracking, velocity metrics, goal tracking, and trend visualization.
"""

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any

from error_handling import AnalyticsError, get_logger, log_and_raise


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

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        try:
            return asdict(self)
        except (TypeError, AttributeError) as e:
            get_logger(__name__).error(
                f"Error converting {self.__class__.__name__} to dict: {e}"
            )
            raise


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

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        try:
            return asdict(self)
        except (TypeError, AttributeError) as e:
            get_logger(__name__).error(
                f"Error converting {self.__class__.__name__} to dict: {e}"
            )
            raise


class AnalyticsManager:
    """Manages historical analytics, velocity metrics, and goal tracking."""

    def __init__(self, history_file: str = "analytics_history.json"):
        """Initialize the analytics manager."""
        self.history_file = history_file
        self.logger = get_logger(__name__)
        self.history_data: list[dict[str, Any]] = []
        self.load_history()

    def load_history(self) -> None:
        """Load historical data from file."""
        try:
            if not os.path.exists(self.history_file):
                self.logger.info(
                    f"History file {self.history_file} does not exist, starting with empty data"
                )
                self.history_data = []
                return

            with open(self.history_file, encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.history_data = data
            else:
                self.logger.warning(
                    f"History file {self.history_file} does not contain a list, starting with empty data"
                )
                self.history_data = []

            self.logger.debug(f"Loading historical data from {self.history_file}")

        except (FileNotFoundError, PermissionError) as e:
            self.logger.warning(f"Could not read history file {self.history_file}: {e}")
            self.history_data = []
        except (json.JSONDecodeError, TypeError) as e:
            self.logger.error(f"Invalid JSON in history file {self.history_file}: {e}")
            self.history_data = []
        except OSError as e:
            self.logger.error(f"IO error reading history file {self.history_file}: {e}")
            self.history_data = []

    def save_history(self) -> None:
        """Save historical data to file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history_data, f, indent=2, ensure_ascii=False)

            self.logger.debug(
                f"Saved {len(self.history_data)} data points to {self.history_file}"
            )

        except (PermissionError, OSError) as e:
            self.logger.error(
                f"Could not write to history file {self.history_file}: {e}"
            )
        except (TypeError, ValueError) as e:
            self.logger.error(f"Error serializing history data: {e}")

    def add_data_point(self, stats: dict[str, Any]) -> None:
        """Add a new data point to the history."""
        try:
            timestamp = datetime.now().isoformat()
            data_point = {
                "timestamp": timestamp,
                "total_loc": stats.get("total_loc", 0),
                "total_commits": stats.get("total_commits", 0),
                "total_files": stats.get("total_files", 0),
                "repos_processed": stats.get("repos_processed", 0),
            }

            self.history_data.append(data_point)
            self.save_history()

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error adding data point: {e}")
        except OSError as e:
            self.logger.error(f"Error saving data point: {e}")

    def calculate_growth_trends(self, days: int = 30) -> dict[str, Any]:
        """Calculate growth trends over the specified number of days."""
        try:
            if not self.history_data:
                return {"error": "No historical data available"}

            # Get recent data points
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_data = []

            for point in self.history_data:
                try:
                    point_date = datetime.fromisoformat(
                        point["timestamp"].replace("Z", "+00:00")
                    )
                    if point_date >= cutoff_date:
                        recent_data.append(point)
                except (ValueError, TypeError, KeyError) as e:
                    self.logger.warning(f"Invalid timestamp in data point: {e}")
                    continue

            if len(recent_data) < 2:
                return {"error": f"Insufficient data for {days} day trend analysis"}

            # Calculate trends
            first_point = recent_data[0]
            last_point = recent_data[-1]

            trends = {
                "period_days": days,
                "data_points": len(recent_data),
                "loc_growth": last_point.get("total_loc", 0)
                - first_point.get("total_loc", 0),
                "commits_growth": last_point.get("total_commits", 0)
                - first_point.get("total_commits", 0),
                "files_growth": last_point.get("total_files", 0)
                - first_point.get("total_files", 0),
                "repos_growth": last_point.get("repos_processed", 0)
                - first_point.get("repos_processed", 0),
            }

            self.logger.debug(
                f"Calculated growth trends for {days} days with {len(recent_data)} data points"
            )
            return trends

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error calculating growth trends: {e}")
            return {"error": f"Error calculating trends: {e}"}
        except (ValueError, OSError) as e:
            self.logger.error(f"Error processing historical data: {e}")
            return {"error": f"Error processing data: {e}"}

    def calculate_velocity_metrics(
        self, period: str = "weekly"
    ) -> list[VelocityMetrics]:
        """Calculate velocity metrics for the specified period."""
        try:
            if not self.history_data:
                return []

            # Sort data by timestamp
            sorted_data = sorted(
                self.history_data, key=lambda x: x.get("timestamp", "")
            )

            if len(sorted_data) < 2:
                return []

            velocity_metrics = []

            # Calculate velocity for each period
            # Use zip to iterate over consecutive pairs more efficiently
            for current, next_point in zip(
                sorted_data[:-1], sorted_data[1:], strict=False
            ):
                try:
                    # Calculate time difference in days
                    current_date = datetime.fromisoformat(
                        current["timestamp"].replace("Z", "+00:00")
                    )
                    next_date = datetime.fromisoformat(
                        next_point["timestamp"].replace("Z", "+00:00")
                    )
                    days_diff = (next_date - current_date).days

                    if days_diff > 0:
                        velocity = VelocityMetrics(
                            period=period,
                            start_date=current["timestamp"],
                            end_date=next_point["timestamp"],
                            loc_change=next_point.get("total_loc", 0)
                            - current.get("total_loc", 0),
                            commits_change=next_point.get("total_commits", 0)
                            - current.get("total_commits", 0),
                            files_change=next_point.get("total_files", 0)
                            - current.get("total_files", 0),
                            loc_velocity=(
                                next_point.get("total_loc", 0)
                                - current.get("total_loc", 0)
                            )
                            / days_diff,
                            commits_velocity=(
                                next_point.get("total_commits", 0)
                                - current.get("total_commits", 0)
                            )
                            / days_diff,
                            files_velocity=(
                                next_point.get("total_files", 0)
                                - current.get("total_files", 0)
                            )
                            / days_diff,
                        )
                        velocity_metrics.append(velocity)

                except (ValueError, TypeError, KeyError, ZeroDivisionError) as e:
                    self.logger.warning(f"Error calculating velocity for period: {e}")
                    continue

            self.logger.debug(
                f"Calculated {len(velocity_metrics)} velocity metrics for {period} period"
            )
            return velocity_metrics

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error calculating velocity metrics: {e}")
            return []
        except (ValueError, OSError) as e:
            self.logger.error(f"Error processing velocity data: {e}")
            return []

    def track_language_usage(
        self, current_stats: dict[str, Any], language_config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Track language usage statistics.

        Args:
            current_stats: Current statistics including language breakdown
            language_config: Language tracking configuration from config file

        Returns:
            Dictionary with language usage analysis
        """
        try:
            if not language_config.get("enabled", False):
                self.logger.debug("Language tracking disabled in config")
                return {}

            language_stats = current_stats.get("unified_language_stats", {})
            if not language_stats:
                self.logger.warning("No language stats available for tracking")
                return {}

            # Sort languages by LOC
            sorted_languages = sorted(
                language_stats.items(), key=lambda x: x[1]["loc"], reverse=True
            )

            # Get top languages
            top_count = language_config.get("track_top_languages", 10)
            top_languages = sorted_languages[:top_count]

            # Calculate total LOC for percentage calculation
            total_loc = sum(stats["loc"] for _, stats in language_stats.items())

            # Build language usage analysis
            language_analysis = {
                "total_languages": len(language_stats),
                "top_languages": [],
                "total_loc": total_loc,
                "language_distribution": {},
            }

            for language, stats in top_languages:
                try:
                    loc = stats["loc"]
                    commits = stats["commits"]
                    files = stats["files"]

                    # Calculate percentage
                    percentage = (loc / total_loc * 100) if total_loc > 0 else 0

                    language_analysis["top_languages"].append(
                        {
                            "language": language,
                            "loc": loc,
                            "commits": commits,
                            "files": files,
                            "percentage": percentage,
                        }
                    )

                    language_analysis["language_distribution"][language] = {
                        "loc": loc,
                        "commits": commits,
                        "files": files,
                        "percentage": percentage,
                    }

                except (TypeError, AttributeError, KeyError, ZeroDivisionError) as e:
                    self.logger.error(f"Error processing language {language}: {e}")
                    continue

            self.logger.info(
                f"Tracked {len(language_analysis['top_languages'])} top languages out of {language_analysis['total_languages']} total"
            )
            return language_analysis

        except (TypeError, AttributeError, KeyError) as e:
            log_and_raise(
                AnalyticsError,
                f"Error tracking language usage: {e}",
                error_code="LANGUAGE_TRACKING_ERROR",
            )
            return {}
        except (ValueError, OSError) as e:
            log_and_raise(
                AnalyticsError,
                f"Error processing language tracking data: {e}",
                error_code="LANGUAGE_TRACKING_ERROR",
            )
            return {}

    def _get_current_value(self, stats: dict[str, Any], metric: str) -> int | None:
        """Extract current value for a given metric."""
        try:
            if metric == "total_loc":
                value = stats.get("total_loc", 0)
                return value if isinstance(value, int) else 0
            elif metric == "total_commits":
                value = stats.get("total_commits", 0)
                return value if isinstance(value, int) else 0
            elif metric == "total_files":
                value = stats.get("total_files", 0)
                return value if isinstance(value, int) else 0
            elif metric == "guillermo_loc":
                guillermo_data = stats.get("guillermo_unified", {})
                if isinstance(guillermo_data, dict):
                    value = guillermo_data.get("loc", 0)
                    return value if isinstance(value, int) else 0
                return 0
            elif metric == "guillermo_commits":
                guillermo_data = stats.get("guillermo_unified", {})
                if isinstance(guillermo_data, dict):
                    value = guillermo_data.get("commits", 0)
                    return value if isinstance(value, int) else 0
                return 0
            elif metric == "guillermo_files":
                guillermo_data = stats.get("guillermo_unified", {})
                if isinstance(guillermo_data, dict):
                    value = guillermo_data.get("files", 0)
                    return value if isinstance(value, int) else 0
                return 0
            else:
                self.logger.warning(f"Unknown metric: {metric}")
                return None

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error getting current value for metric {metric}: {e}")
            return None

    def get_trend_analysis(self) -> dict[str, Any]:
        """
        Perform comprehensive trend analysis.

        Returns:
            Dictionary with trend analysis results
        """
        try:
            if len(self.history_data) < 3:
                self.logger.warning("Insufficient data for trend analysis")
                return {"error": "Insufficient data for trend analysis"}

            # Calculate trends for different periods
            trends = {
                "weekly": self.calculate_growth_trends(7),
                "monthly": self.calculate_growth_trends(30),
                "quarterly": self.calculate_growth_trends(90),
                "velocity": {
                    "weekly": self.calculate_velocity_metrics("weekly"),
                    "monthly": self.calculate_velocity_metrics("monthly"),
                },
            }

            self.logger.info("Completed comprehensive trend analysis")
            return trends

        except (TypeError, AttributeError, KeyError) as e:
            log_and_raise(
                AnalyticsError,
                f"Error performing trend analysis: {e}",
                error_code="TREND_ANALYSIS_ERROR",
            )
            return {}
        except (ValueError, OSError) as e:
            log_and_raise(
                AnalyticsError,
                f"Error processing trend analysis data: {e}",
                error_code="TREND_ANALYSIS_ERROR",
            )
            return {}

    def cleanup_old_data(self, days_to_keep: int = 365) -> None:
        """Remove data points older than the specified number of days."""
        try:
            if not self.history_data:
                return

            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            original_count = len(self.history_data)

            # Filter out old data points
            self.history_data = [
                point
                for point in self.history_data
                if datetime.fromisoformat(point["timestamp"].replace("Z", "+00:00"))
                >= cutoff_date
            ]

            removed_count = original_count - len(self.history_data)
            if removed_count > 0:
                self.save_history()
                self.logger.info(
                    f"Removed {removed_count} old data points, keeping {len(self.history_data)}"
                )
            else:
                self.logger.debug("No old data to clean up")

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error cleaning up old data: {e}")
        except (ValueError, OSError) as e:
            self.logger.error(f"Error processing cleanup data: {e}")


def get_analytics_manager(
    history_file: str = "analytics_history.json",
) -> AnalyticsManager:
    """
    Factory function to create and return an AnalyticsManager instance.

    Args:
        history_file: Path to the historical data file

    Returns:
        AnalyticsManager instance
    """
    try:
        manager = AnalyticsManager(history_file)
        get_logger(__name__).debug(
            f"Created AnalyticsManager with history file: {history_file}"
        )
        return manager
    except (FileNotFoundError, PermissionError) as e:
        get_logger(__name__).error(f"Could not create AnalyticsManager: {e}")
        raise
    except (json.JSONDecodeError, TypeError) as e:
        get_logger(__name__).error(f"Invalid JSON in analytics history file: {e}")
        raise
    except OSError as e:
        get_logger(__name__).error(f"IO error creating AnalyticsManager: {e}")
        raise
