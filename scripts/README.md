# Repository Statistics Scripts

This directory contains the modular Python scripts for processing repository statistics.

## Architecture

### Core Modules

- **`config_manager.py`** - Configuration management and validation

  - Loads YAML configuration files
  - Provides type-safe access to configuration values
  - Validates configuration structure

- **`git_fame_parser.py`** - Git fame execution and data parsing

  - Executes git fame commands with proper error handling
  - Parses JSON output from git fame
  - Validates data structure

- **`stats_processor.py`** - Core statistics processing logic

  - Author pattern matching (Guillermo vs bots vs others)
  - Repository statistics aggregation
  - Distribution percentage calculations
  - Data validation

- **`report_generator.py`** - Report generation
  - Markdown report generation with configurable formatting
  - JSON report generation for API consumption
  - Templated output with proper formatting

### Main Scripts

- **`process_repo_stats.py`** - Individual repository processing

  - Processes a single repository's git fame data
  - Saves results as JSON artifacts for the workflow
  - Used by the parallel matrix jobs

- **`aggregate_stats.py`** - Statistics aggregation and report generation
  - Loads artifacts from all repository processing jobs
  - Aggregates unified statistics
  - Generates final markdown and JSON reports

## Configuration

All configuration is externalized to `../config.yml`:

```yaml
repositories:
  - name: "repository-name"
    display_name: "Human Readable Name"
    branch: "develop"
    artifact_name: "unique-artifact-name"

author_patterns:
  guillermo:
    - "guillermo.*affiliaction"
    - "Guillermo.*Affiliaction"
  bots:
    - ".*\\[bot\\]$"
    - "gpt-engineer-app.*"
```

## Usage

### Individual Repository Processing

```bash
export REPO_NAME="housing-hub-saas"
export DISPLAY_NAME="InmoIA Frontend"
python3 process_repo_stats.py
```

### Statistics Aggregation

```bash
python3 aggregate_stats.py
```

## Dependencies

Install dependencies with:

```bash
pip install -r ../requirements.txt
```

Required packages:

- `git-fame` - Git statistics tool
- `PyYAML` - YAML configuration parsing

## Testing

The modular architecture enables unit testing of individual components:

```python
from config_manager import ConfigManager
from stats_processor import AuthorMatcher, StatsProcessor

# Test configuration loading
config = ConfigManager("test_config.yml")
assert config.get_repositories() is not None

# Test author matching
matcher = AuthorMatcher(["guillermo.*"], [".*bot.*"])
assert matcher.is_guillermo("guillermo.affiliaction@example.com")
```

## Error Handling

All modules include comprehensive error handling:

- Configuration validation with detailed error messages
- Git fame execution timeouts and error recovery
- Data validation at each processing step
- Graceful degradation for missing data

## Performance

- **Parallel processing**: Repository processing runs in parallel matrix jobs
- **Efficient data structures**: Uses dataclasses for type safety and performance
- **Minimal memory usage**: Streams data processing where possible
- **Caching**: GitHub Actions caches dependencies between runs
