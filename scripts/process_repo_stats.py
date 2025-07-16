#!/usr/bin/env python3
"""
Repository Statistics Processing Script
Processes git fame statistics for a single repository and saves results.
"""

import json
import sys
import os
from pathlib import Path
import subprocess
from error_handling import (
    setup_logging, DataProcessingError, log_and_raise, get_logger, ErrorCodes, with_error_context
)

# Constants for resource limits
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2MB
MAX_LINE_LENGTH_BYTES = 50 * 1024  # 50KB
MAX_OUTPUT_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
CLOC_TIMEOUT_SECONDS = 120
CLOC_PROCESS_TIMEOUT_SECONDS = 60

# Set up logging for this module
logger = get_logger(__name__)

# Add scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config_manager import get_config_manager
from git_fame_parser import GitFameParser
from stats_processor import StatsProcessor, AuthorMatcher
from language_mapper import get_language_mapper


def run_cloc_on_repo(repo_path: Path) -> dict:
    """Run cloc on the given repo path and return the parsed JSON output."""
    try:
        # Add resource limits to prevent memory issues with large repositories
        result = subprocess.run([
            'cloc', '--json', '--quiet', f'--timeout={CLOC_PROCESS_TIMEOUT_SECONDS}',
            f'--max-file-size={MAX_FILE_SIZE_BYTES}',  # 2MB file size limit
            f'--max-line-length={MAX_LINE_LENGTH_BYTES}',  # 50KB line length limit (increased for large TS/Python files)
            '--include-lang=Python,TypeScript,JavaScript,HTML,CSS,Shell',
            '--exclude-dir=.git,node_modules,venv,build,dist,data,output,logs,generated,target,coverage,.nyc_output',
            '--exclude-ext=json,toml,lock,yml,yaml,ini,cfg,conf,env,log,md,txt,svg,png,jpg,jpeg,gif,ico,bmp,tiff,webp',
            str(repo_path)
        ], capture_output=True, text=True, timeout=CLOC_TIMEOUT_SECONDS)
        
        if result.returncode != 0:
            logger.error(f"cloc failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return {}
        
        if not result.stdout.strip():
            logger.warning(f"No output from cloc for {repo_path}")
            return {}
        
        # Parse JSON output
        try:
            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse cloc JSON output: {e}")
            return {}
            
    except subprocess.TimeoutExpired as e:
        logger.error(f"cloc execution timed out after {CLOC_TIMEOUT_SECONDS} seconds: {e}")
        return {}
    except subprocess.CalledProcessError as e:
        logger.error(f"cloc process error: {e}")
        return {}
    except (TypeError, ValueError, OSError) as e:
        logger.error(f"Error executing cloc: {e}")
        return {}


def generate_svg_content(top_languages, total_loc):
    """Generate a simple SVG bar chart for language statistics."""
    width = 600
    bar_height = 30
    height = bar_height * len(top_languages) + 40
    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    y = 30
    for lang, loc in top_languages:
        bar_width = int((loc / total_loc) * (width - 200)) if total_loc > 0 else 0
        svg.append(f'<rect x="150" y="{y}" width="{bar_width}" height="{bar_height-8}" fill="#4F8EF7" />')
        svg.append(f'<text x="10" y="{y+bar_height//2}" font-size="14" fill="#222">{lang}</text>')
        svg.append(f'<text x="{150+bar_width+10}" y="{y+bar_height//2}" font-size="14" fill="#222">{loc:,}</text>')
        y += bar_height
    svg.append('</svg>')
    return '\n'.join(svg)


def generate_language_svg_bar_chart(language_stats: dict, output_path: str):
    """Generate SVG bar chart for language statistics."""
    try:
        if not language_stats:
            logger.warning("No language stats provided for SVG generation")
            return
        
        # Sort languages by LOC
        sorted_languages = sorted(language_stats.items(), key=lambda x: x[1], reverse=True)
        
        # Take top 10 languages
        top_languages = sorted_languages[:10]
        
        if not top_languages:
            logger.warning("No valid language data for SVG generation")
            return
        
        # Calculate total LOC for percentage calculation
        total_loc = sum(loc for _, loc in top_languages)
        
        # Generate SVG content
        svg_content = generate_svg_content(top_languages, total_loc)
        
        # Save SVG file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            logger.info(f"Language SVG chart saved to {output_path}")
        except (PermissionError, OSError) as e:
            logger.error(f"Could not write to {output_path}: {e}")
        except (TypeError, ValueError) as e:
            logger.error(f"Error writing SVG content: {e}")
        except IOError as e:
            logger.error(f"IO error writing {output_path}: {e}")
            
    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error generating language SVG chart: {e}")
    except (ValueError, OSError) as e:
        logger.error(f"Error processing language stats: {e}")


@with_error_context({'component': 'process_repo_stats'})
def main():
    language_stats = {}  # Ensure language_stats is always defined
    try:
        config = get_config_manager()
        config_errors = config.validate_config()
        if config_errors:
            logger.error(f"Configuration validation errors: {config_errors}")
            sys.exit(1)
        repo_name = os.environ.get('REPO_NAME')
        display_name = os.environ.get('DISPLAY_NAME')
        if not repo_name:
            logger.error("REPO_NAME environment variable not set")
            sys.exit(1)
        if not display_name:
            repo_config = config.get_repository_by_name(repo_name)
            if repo_config:
                display_name = repo_config.get('display_name', repo_name)
            else:
                display_name = repo_name
        git_fame_parser = GitFameParser(timeout_seconds=config.get_timeout_seconds())
        author_matcher = AuthorMatcher(
            guillermo_patterns=config.get_guillermo_patterns(),
            bot_patterns=config.get_bot_patterns()
        )
        stats_processor = StatsProcessor(author_matcher)
        language_mapper = get_language_mapper()
        repo_path = script_dir.parent / "repo"
        if not repo_path.exists():
            logger.error(f"Repository path does not exist: {repo_path}")
            sys.exit(1)
        try:
            cloc_data = run_cloc_on_repo(repo_path)
            cloc_language_stats = {}
            if cloc_data:
                for lang, stats in cloc_data.items():
                    if lang in ('header', 'SUM', 'JSON', 'Text', 'YAML', 'TOML', 'INI', 'Markdown', 'Properties', 'Image', 'SVG'):
                        continue
                    cloc_language_stats[lang] = {
                        'loc': stats.get('code', 0),
                        'files': stats.get('nFiles', 0),
                        'commits': 0
                    }
        except Exception as e:
            logger.warning(f"cloc analysis failed: {e}", extra={'repo_path': str(repo_path)})
            cloc_language_stats = {}
        git_fame_data = git_fame_parser.execute_git_fame(
            str(repo_path), 
            config.get_git_fame_format()
        )
        if not git_fame_data:
            logger.error("git fame data is empty")
            sys.exit(1)
        if not git_fame_parser.validate_git_fame_data(git_fame_data):
            logger.error("git fame data validation failed")
            sys.exit(1)
        authors = git_fame_parser.extract_authors(git_fame_data)
        if not authors:
            logger.error("No authors found in git fame data")
            sys.exit(1)
        git_fame_bytype_data = git_fame_parser.execute_git_fame(
            str(repo_path),
            config.get_git_fame_format(),
            by_type=True
        )
        language_stats = {}
        if git_fame_bytype_data:
            extension_stats = git_fame_parser.extract_extension_stats(git_fame_bytype_data)
            language_stats = language_mapper.get_language_stats(extension_stats)
        repo_stats = stats_processor.process_repository_data(authors, display_name)
        repo_stats.language_stats = language_stats
        stats_dict = repo_stats.to_dict()
        output_filename = config.get_stats_filename()
        output_path = script_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, indent=2, ensure_ascii=False)
        from dependency_analyzer import DependencyAnalyzer
        repo_dir = script_dir.parent / "repo"
        analyzer = DependencyAnalyzer()
        tech_stack = analyzer.analyze_repository_dependencies(repo_dir)
        tech_stack_serializable = {}
        for category, techs in tech_stack.items():
            tech_list = sorted(list(techs))
            tech_stack_serializable[category] = {
                'technologies': tech_list,
                'count': len(tech_list)
            }
        with open('tech_stack_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(tech_stack_serializable, f, indent=2, ensure_ascii=False)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_and_raise(
            DataProcessingError(
                f"Failed to process repository statistics: {e}",
                error_code=ErrorCodes.DATA_PROCESSING_FAILED,
                context={'script': 'process_repo_stats', 'repo_name': os.environ.get('REPO_NAME')}
            ),
            logger=logger
        )

if __name__ == "__main__":
    setup_logging()
    main() 