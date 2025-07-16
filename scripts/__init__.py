"""
GitHub Profile README Generator Scripts Package

This package contains all the scripts for generating and updating GitHub profile README
with repository statistics and analytics.

Modules:
    - aggregate_stats: Aggregates statistics from multiple repositories
    - analytics_manager: Manages analytics data and historical tracking
    - analytics_reporter: Generates analytics reports
    - config_manager: Manages configuration loading and validation
    - dependency_analyzer: Analyzes project dependencies and tech stack
    - enhanced_readme_generator: Generates enhanced README content
    - error_handling: Comprehensive error handling and logging utilities
    - generate_language_svg: Generates language statistics SVG charts
    - generate_readme: Legacy README generator
    - git_fame_parser: Parses git-fame output data
    - language_mapper: Maps file extensions to programming languages
    - process_repo_stats: Processes individual repository statistics
    - regenerate_readme: Regenerates README from existing data
    - report_generator: Generates various report formats
    - stats_processor: Core statistics processing logic
    - update_tech_stack: Updates technology stack information
"""

__version__ = "2.0.0"
__author__ = "Guillermo Astorga Calvo"
__description__ = "GitHub Profile README Generator with Analytics"

# Import key functions for easy access
from .config_manager import create_config_manager
from .error_handling import setup_logging, get_logger
from .stats_processor import StatsProcessor, AuthorMatcher
from .language_mapper import get_language_mapper

__all__ = [
    'create_config_manager',
    'setup_logging', 
    'get_logger',
    'StatsProcessor',
    'AuthorMatcher',
    'get_language_mapper'
] 