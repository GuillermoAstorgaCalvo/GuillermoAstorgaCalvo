#!/usr/bin/env python3
"""
Statistics Aggregation Script
Aggregates statistics from multiple repositories and generates unified reports.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import os
from error_handling import (
    setup_logging, DataProcessingError, log_and_raise, get_logger, ErrorCodes, with_error_context
)
from datetime import datetime

# Set up logging for this module
logger = get_logger(__name__)

# Add scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config_manager import create_config_manager
from stats_processor import StatsProcessor, AuthorMatcher, RepositoryStats, AuthorStats
from report_generator import MarkdownReportGenerator, JSONReportGenerator
from language_mapper import get_language_mapper


def load_repository_stats(repo_name: str) -> Dict[str, Any]:
    """Load statistics for a specific repository."""
    try:
        stats_file = f"{repo_name}_stats.json"
        
        if not os.path.exists(stats_file):
            logger.warning(f"Stats file not found: {stats_file}")
            return {}
        
        with open(stats_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded stats for {repo_name}: {len(data)} data points")
        return data
        
    except (FileNotFoundError, PermissionError) as e:
        logger.warning(f"Could not read {repo_name}_stats.json: {e}")
        return {}
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in {repo_name}_stats.json: {e}")
        return {}
    except (OSError, IOError) as e:
        logger.error(f"IO error reading {repo_name}_stats.json: {e}")
        return {}

def save_unified_stats(stats: Dict[str, Any], output_file: str = "unified_stats.json") -> bool:
    """Save unified statistics to JSON file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Unified stats saved to {output_file}")
        return True
        
    except (PermissionError, OSError) as e:
        logger.error(f"Could not write to {output_file}: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Error serializing unified stats: {e}")
        return False
    except IOError as e:
        logger.error(f"IO error writing {output_file}: {e}")
        return False

def aggregate_repository_data(repo_stats_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate data from multiple repositories."""
    try:
        unified_stats: Dict[str, Any] = {
            'total_loc': 0,
            'total_commits': 0,
            'total_files': 0,
            'repos_processed': len(repo_stats_list),
            'repository_breakdown': {},
            'language_stats': {},
            'last_updated': datetime.now().isoformat()
        }
        
        for repo_data in repo_stats_list:
            try:
                repo_name = repo_data.get('repository_name', 'Unknown')
                
                # Aggregate totals
                unified_stats['total_loc'] += repo_data.get('total_loc', 0)
                unified_stats['total_commits'] += repo_data.get('total_commits', 0)
                unified_stats['total_files'] += repo_data.get('total_files', 0)
                
                # Store individual repository data
                unified_stats['repository_breakdown'][repo_name] = {
                    'total_loc': repo_data.get('total_loc', 0),
                    'total_commits': repo_data.get('total_commits', 0),
                    'total_files': repo_data.get('total_files', 0),
                    'language_breakdown': repo_data.get('language_breakdown', {})
                }
                
                # Aggregate language statistics
                for lang, lang_stats in repo_data.get('language_breakdown', {}).items():
                    if lang not in unified_stats['language_stats']:
                        unified_stats['language_stats'][lang] = {
                            'loc': 0,
                            'files': 0,
                            'commits': 0
                        }
                    
                    unified_stats['language_stats'][lang]['loc'] += lang_stats.get('loc', 0)
                    unified_stats['language_stats'][lang]['files'] += lang_stats.get('files', 0)
                    unified_stats['language_stats'][lang]['commits'] += lang_stats.get('commits', 0)
                    
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


@with_error_context({'component': 'aggregate_stats'})
def main():
    try:
        config = create_config_manager()
        config_errors = config.validate_config()
        if config_errors:
            logger.error(f"Configuration validation errors: {config_errors}")
            sys.exit(1)
        author_matcher = AuthorMatcher(
            guillermo_patterns=config.get_guillermo_patterns(),
            bot_patterns=config.get_bot_patterns()
        )
        stats_processor = StatsProcessor(author_matcher)
        language_mapper = get_language_mapper()
        repository_stats_list = load_repository_stats()
        if not repository_stats_list:
            logger.error("No repository statistics found.")
            sys.exit(1)
        unified_stats = stats_processor.aggregate_repository_stats(repository_stats_list)
        validation_errors = stats_processor.validate_unified_stats(unified_stats)
        if validation_errors:
            logger.error(f"Unified stats validation errors: {validation_errors}")
            sys.exit(1)
        from dependency_analyzer import DependencyAnalyzer
        all_tech_stacks = []
        repos_dir = Path(os.environ.get('REPOS_DIR', 'repo-stats'))
        if not repos_dir.exists():
            repos_dir = Path.cwd()
        for subdir in repos_dir.iterdir():
            if subdir.is_dir():
                tech_stack_file = subdir / 'tech_stack_analysis.json'
                if tech_stack_file.exists():
                    try:
                        with open(tech_stack_file, 'r', encoding='utf-8') as f:
                            stack = json.load(f)
                            all_tech_stacks.append(stack)
                    except Exception as e:
                        logger.warning(f"Failed to load tech stack file {tech_stack_file}: {e}", extra={'file': str(tech_stack_file)})
        merged_stack = {
            'frontend': set(),
            'backend': set(),
            'database': set(),
            'devops': set(),
            'ai_ml': set()
        }
        for stack in all_tech_stacks:
            for category in merged_stack:
                if isinstance(stack, dict) and category in stack:
                    category_data = stack[category]
                    if isinstance(category_data, dict) and 'technologies' in category_data:
                        technologies = category_data['technologies']
                        if isinstance(technologies, list):
                            merged_stack[category].update(technologies)
        merged_stack_final = {cat: {'technologies': sorted(list(techs)), 'count': len(techs)} for cat, techs in merged_stack.items()}
        try:
            setattr(unified_stats, 'tech_stack_analysis', merged_stack_final)
        except Exception:
            if isinstance(unified_stats, dict):
                unified_stats['tech_stack_analysis'] = merged_stack_final
        report_config = config.get_report_config()
        json_generator = JSONReportGenerator()
        json_filename = "unified_stats.json"
        json_path = script_dir / json_filename
        json_generator.save_report(unified_stats, str(json_path))
        guillermo = unified_stats.guillermo_unified
        global_totals = AuthorStats(
            loc=unified_stats.total_loc,
            commits=unified_stats.total_commits,
            files=unified_stats.total_files
        )
        loc_pct, commits_pct, files_pct = stats_processor.calculate_distribution_percentages(
            guillermo, global_totals
        )
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_and_raise(
            DataProcessingError(
                f"Failed to aggregate statistics: {e}",
                error_code=ErrorCodes.DATA_PROCESSING_FAILED,
                context={'script': 'aggregate_stats'}
            ),
            logger=logger
        )

if __name__ == "__main__":
    setup_logging()
    main() 