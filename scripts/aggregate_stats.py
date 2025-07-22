#!/usr/bin/env python3
"""
Statistics Aggregation Script
Aggregates statistics from multiple repositories and generates unified reports.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from config_manager import create_config_manager
from error_handling import (
    DataProcessingError,
    ErrorCodes,
    get_logger,
    log_and_raise,
    setup_logging,
    with_error_context,
)
from report_generator import JSONReportGenerator
from stats_processor import AuthorMatcher, AuthorStats, StatsProcessor

# Set up logging for this module
logger = get_logger(__name__)

# Add scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def load_repository_stats(repo_name: str) -> dict[str, Any]:
    """Load statistics for a specific repository."""
    try:
        stats_file = f"{repo_name}_stats.json"

        if not os.path.exists(stats_file):
            logger.warning(f"Stats file not found: {stats_file}")
            return {}

        with open(stats_file, encoding="utf-8") as f:
            data = json.load(f)

        logger.info(f"Loaded stats for {repo_name}: {len(data)} data points")
        if isinstance(data, dict):
            return data
        else:
            logger.error(f"Stats data for {repo_name} is not a dictionary")
            return {}

    except (FileNotFoundError, PermissionError) as e:
        logger.warning(f"Could not read {repo_name}_stats.json: {e}")
        return {}
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in {repo_name}_stats.json: {e}")
        return {}
    except OSError as e:
        logger.error(f"IO error reading {repo_name}_stats.json: {e}")
        return {}


def load_all_repository_stats() -> list[dict[str, Any]]:
    """Load statistics from all available repository files."""
    try:
        stats_files = []

        # Use REPOS_DIR environment variable if available, otherwise use current directory
        repos_dir = Path(os.environ.get("REPOS_DIR", "."))
        if not repos_dir.exists():
            logger.warning(f"Repository directory does not exist: {repos_dir}")
            repos_dir = Path.cwd()

        logger.info(f"Looking for stats files in: {repos_dir}")

        # Look for *_stats.json files in the repository directory
        for file_path in repos_dir.glob("*_stats.json"):
            if file_path.name != "unified_stats.json":
                stats_files.append(file_path)

        if not stats_files:
            logger.warning(f"No repository stats files found in {repos_dir}")
            return []

        repository_stats = []
        for stats_file in stats_files:
            try:
                with open(stats_file, encoding="utf-8") as f:
                    data = json.load(f)
                    repository_stats.append(data)
                    logger.info(f"Loaded stats from {stats_file.name}")
            except Exception as e:
                logger.warning(f"Failed to load {stats_file.name}: {e}")
                continue

        logger.info(f"Loaded stats from {len(repository_stats)} repositories")
        return repository_stats

    except Exception as e:
        logger.error(f"Error loading repository stats: {e}")
        return []


def save_unified_stats(
    stats: dict[str, Any], output_file: str = "unified_stats.json"
) -> bool:
    """Save unified statistics to JSON file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        logger.info(f"Unified stats saved to {output_file}")
        return True

    except (PermissionError, OSError) as e:
        logger.error(f"Could not write to {output_file}: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Error serializing unified stats: {e}")
        return False


def aggregate_repository_data(repo_stats_list: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate data from multiple repositories."""
    try:
        unified_stats: dict[str, Any] = {
            "total_loc": 0,
            "total_commits": 0,
            "total_files": 0,
            "repos_processed": len(repo_stats_list),
            "repository_breakdown": {},
            "language_stats": {},
            "last_updated": datetime.now().isoformat(),
        }

        for repo_data in repo_stats_list:
            try:
                repo_name = repo_data.get("repository_name", "Unknown")

                # Aggregate totals
                unified_stats["total_loc"] += repo_data.get("total_loc", 0)
                unified_stats["total_commits"] += repo_data.get("total_commits", 0)
                unified_stats["total_files"] += repo_data.get("total_files", 0)

                # Store individual repository data
                unified_stats["repository_breakdown"][repo_name] = {
                    "total_loc": repo_data.get("total_loc", 0),
                    "total_commits": repo_data.get("total_commits", 0),
                    "total_files": repo_data.get("total_files", 0),
                    "language_breakdown": repo_data.get("language_breakdown", {}),
                }

                # Aggregate language statistics
                for lang, lang_stats in repo_data.get("language_breakdown", {}).items():
                    if lang not in unified_stats["language_stats"]:
                        unified_stats["language_stats"][lang] = {
                            "loc": 0,
                            "files": 0,
                            "commits": 0,
                        }

                    unified_stats["language_stats"][lang]["loc"] += lang_stats.get(
                        "loc", 0
                    )
                    unified_stats["language_stats"][lang]["files"] += lang_stats.get(
                        "files", 0
                    )
                    unified_stats["language_stats"][lang]["commits"] += lang_stats.get(
                        "commits", 0
                    )

            except (TypeError, AttributeError, KeyError) as e:
                logger.warning(f"Error processing repository data: {e}")
                continue

        logger.info(f"Aggregated data from {len(repo_stats_list)} repositories")
        return unified_stats

    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error aggregating repository data: {e}")
        return {}
    except (ValueError, OSError) as e:
        logger.error(f"Error processing aggregated data: {e}")
        return {}


@with_error_context({"component": "aggregate_stats"})
def main() -> None:
    try:
        config = create_config_manager(str(script_dir.parent / "config.yml"))
        config_errors = config.validate_config()
        if config_errors:
            logger.error(f"Configuration validation errors: {config_errors}")
            sys.exit(1)
        author_matcher = AuthorMatcher(
            guillermo_patterns=config.get_guillermo_patterns(),
            bot_patterns=config.get_bot_patterns(),
        )
        stats_processor = StatsProcessor(author_matcher)
        # language_mapper = get_language_mapper()  # Not used in this function
        repository_stats_data = load_all_repository_stats()
        if not repository_stats_data:
            logger.error("No repository statistics found.")
            sys.exit(1)

        logger.info(f"Processing {len(repository_stats_data)} repository data entries")

        # Convert dictionary data to RepositoryStats objects
        from stats_processor import RepositoryStats

        repository_stats_list = []
        for repo_data in repository_stats_data:
            logger.info(f"Processing repository data: {repo_data.get('display_name', 'Unknown')}")
            try:
                display_name = repo_data.get("display_name", "Unknown")
                guillermo_stats = AuthorStats(
                    loc=repo_data.get("guillermo_stats", {}).get("loc", 0),
                    commits=repo_data.get("guillermo_stats", {}).get("commits", 0),
                    files=repo_data.get("guillermo_stats", {}).get("files", 0),
                )
                repo_totals = AuthorStats(
                    loc=repo_data.get("repo_totals", {}).get("loc", 0),
                    commits=repo_data.get("repo_totals", {}).get("commits", 0),
                    files=repo_data.get("repo_totals", {}).get("files", 0),
                )
                language_stats = repo_data.get("language_stats", {})

                repo_stats = RepositoryStats(
                    display_name=display_name,
                    guillermo_stats=guillermo_stats,
                    repo_totals=repo_totals,
                    language_stats=language_stats,
                )
                repository_stats_list.append(repo_stats)
            except Exception as e:
                logger.warning(f"Error converting repository data: {e}")
                continue

        unified_stats = stats_processor.aggregate_repository_stats(
            repository_stats_list
        )
        validation_errors = stats_processor.validate_unified_stats(unified_stats)
        if validation_errors:
            logger.error(f"Unified stats validation errors: {validation_errors}")
            sys.exit(1)
        all_tech_stacks = []
        repos_dir = Path(os.environ.get("REPOS_DIR", "repo-stats"))
        if not repos_dir.exists():
            repos_dir = Path.cwd()

        # Look for tech_stack_analysis.json files in the repository directory
        tech_stack_files = list(repos_dir.glob("tech_stack_analysis.json"))

        for tech_stack_file in tech_stack_files:
            try:
                with open(tech_stack_file, encoding="utf-8") as f:
                    stack = json.load(f)
                    all_tech_stacks.append(stack)
                    logger.info(f"Loaded tech stack from {tech_stack_file.name}")
            except Exception as e:
                logger.warning(
                    f"Failed to load tech stack file {tech_stack_file}: {e}",
                    extra={"file": str(tech_stack_file)},
                )
        merged_stack: dict[str, set[str]] = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }
        for stack in all_tech_stacks:
            for category in merged_stack:
                if isinstance(stack, dict) and category in stack:
                    category_data = stack[category]
                    if (
                        isinstance(category_data, dict)
                        and "technologies" in category_data
                    ):
                        technologies = category_data["technologies"]
                        if isinstance(technologies, list):
                            merged_stack[category].update(technologies)
        merged_stack_final = {
            cat: {"technologies": sorted(techs), "count": len(techs)}
            for cat, techs in merged_stack.items()
        }
        # Convert UnifiedStats to dictionary for JSON serialization
        unified_stats_dict = {
            "total_loc": unified_stats.total_loc,
            "total_commits": unified_stats.total_commits,
            "total_files": unified_stats.total_files,
            "repos_processed": unified_stats.repos_processed,
            "guillermo_unified": (
                unified_stats.guillermo_unified.to_dict()
                if unified_stats.guillermo_unified
                else {}
            ),
            "repo_breakdown": (
                {
                    name: stats.to_dict()
                    for name, stats in unified_stats.repo_breakdown.items()
                }
                if unified_stats.repo_breakdown
                else {}
            ),
            "unified_language_stats": unified_stats.unified_language_stats or {},
            "other_unknown_breakdown": unified_stats.other_unknown_breakdown or {},
            "validation_results": unified_stats.validation_results or {},
            "tech_stack_analysis": merged_stack_final,
            "last_updated": datetime.now().isoformat(),
        }

        # report_config = config.get_report_config()  # Not used
        json_generator = JSONReportGenerator()
        json_filename = "unified_stats.json"
        json_path = script_dir / json_filename
        json_generator.save_report(unified_stats_dict, str(json_path))
        guillermo = unified_stats.guillermo_unified
        global_totals = AuthorStats(
            loc=unified_stats.total_loc,
            commits=unified_stats.total_commits,
            files=unified_stats.total_files,
        )
        (
            loc_pct,
            commits_pct,
            files_pct,
        ) = stats_processor.calculate_distribution_percentages(guillermo, global_totals)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_and_raise(
            DataProcessingError(
                f"Failed to aggregate statistics: {e}",
                error_code=ErrorCodes.DATA_PROCESSING_FAILED,
                context={"script": "aggregate_stats"},
            ),
            logger=logger,
        )


if __name__ == "__main__":
    setup_logging()
    main()
