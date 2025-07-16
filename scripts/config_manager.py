"""
Configuration Manager for Repository Statistics Workflow
Handles loading and accessing configuration data from YAML files.
"""

from typing import Any

import yaml
from error_handling import (
    ConfigError,
    ErrorCodes,
    get_logger,
    log_and_raise,
)

# Set up logging for this module
logger = get_logger(__name__)


class ConfigManager:
    """Manages configuration loading and access for the statistics workflow."""

    def __init__(self, config_path: str | None = None) -> None:
        """
        Initialize the ConfigManager.

        Args:
            config_path: Path to the configuration file (defaults to config.yml)
        """
        self.config_path = config_path or "config.yml"
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            logger.debug(f"Loading configuration from: {self.config_path}")

            with open(self.config_path, encoding="utf-8") as f:
                self._config = yaml.safe_load(f)

            if not isinstance(self._config, dict):
                log_and_raise(
                    ConfigError(
                        f"Configuration file {self.config_path} must contain a dictionary",
                        error_code=ErrorCodes.CONFIG_INVALID,
                        context={
                            "config_path": self.config_path,
                            "config_type": type(self._config).__name__,
                        },
                    ),
                    logger=logger,
                )

            logger.debug(
                f"Configuration contains {len(self._config)} top-level sections"
            )

        except (FileNotFoundError, PermissionError) as e:
            log_and_raise(
                ConfigError(
                    f"Could not access configuration file {self.config_path}: {e}",
                    error_code=ErrorCodes.CONFIG_ACCESS_FAILED,
                    context={"config_path": self.config_path, "error": str(e)},
                ),
                logger=logger,
            )
        except (yaml.YAMLError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid YAML in configuration file {self.config_path}: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"config_path": self.config_path, "error": str(e)},
                ),
                logger=logger,
            )
        except OSError as e:
            log_and_raise(
                ConfigError(
                    f"IO error reading configuration file {self.config_path}: {e}",
                    error_code=ErrorCodes.CONFIG_ACCESS_FAILED,
                    context={"config_path": self.config_path, "error": str(e)},
                ),
                logger=logger,
            )

    @property
    def config(self) -> dict[str, Any]:
        """Get the full configuration dictionary."""
        if self._config is None:
            raise ConfigError(
                "Configuration not loaded",
                error_code=ErrorCodes.CONFIG_INVALID,
                context={"config_path": str(self.config_path)},
            )
        return self._config

    def get_repositories(self) -> list[dict[str, str]]:
        """Get the list of repositories to process."""
        try:
            repositories = self.config.get("repositories", [])
            logger.debug(
                f"Retrieved {len(repositories)} repositories from configuration"
            )
            return list[dict[str, str]](repositories)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Missing 'repositories' section in configuration: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "repositories", "missing_key": str(e)},
                ),
                logger=logger,
            )
            return []  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid 'repositories' configuration format: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "repositories", "type_error": str(e)},
                ),
                logger=logger,
            )
            return []  # This line will never be reached due to log_and_raise

    def get_repository_by_name(self, name: str) -> dict[str, str] | None:
        """Get repository configuration by name."""
        try:
            for repo in self.get_repositories():
                if repo.get("name") == name:
                    logger.debug(f"Found repository configuration for: {name}")
                    return repo
            logger.warning(f"Repository not found in configuration: {name}")
            return None
        except (KeyError, TypeError, AttributeError) as e:
            # These errors are already handled by get_repositories()
            # Just re-raise with more context
            log_and_raise(
                ConfigError(
                    f"Failed to retrieve repository by name '{name}': {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"repository_name": name, "error_type": type(e).__name__},
                ),
                logger=logger,
            )
            return None  # This line will never be reached due to log_and_raise

    def get_github_config(self) -> dict[str, str]:
        """Get GitHub-related configuration."""
        try:
            github_config = self.config.get("github", {})
            logger.debug(
                f"Retrieved GitHub configuration with {len(github_config)} settings"
            )
            return dict[str, str](github_config)
        except KeyError as e:
            log_and_raise(
                ConfigError(
                    f"Missing 'github' section in configuration: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "github", "missing_key": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise
        except TypeError as e:
            log_and_raise(
                ConfigError(
                    f"Invalid 'github' configuration format: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "github", "type_error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise
        except AttributeError as e:
            log_and_raise(
                ConfigError(
                    f"Configuration object is not properly initialized: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "github", "attribute_error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def get_author_patterns(self) -> dict[str, list[str]]:
        """Get author pattern matching configuration."""
        try:
            patterns = self.config.get("author_patterns", {})
            logger.debug(f"Retrieved author patterns with {len(patterns)} categories")
            return dict[str, list[str]](patterns)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving author patterns: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "author_patterns", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid author patterns configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "author_patterns", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def get_guillermo_patterns(self) -> list[str]:
        """Get Guillermo author patterns."""
        try:
            patterns = self.get_author_patterns().get("guillermo", [])
            logger.debug(f"Retrieved {len(patterns)} Guillermo author patterns")
            return list[str](patterns)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving Guillermo patterns: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "author_patterns.guillermo", "error": str(e)},
                ),
                logger=logger,
            )
            return []  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid Guillermo patterns configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "author_patterns.guillermo", "error": str(e)},
                ),
                logger=logger,
            )
            return []  # This line will never be reached due to log_and_raise

    def get_bot_patterns(self) -> list[str]:
        """Get bot author patterns."""
        try:
            patterns = self.get_author_patterns().get("bots", [])
            logger.debug(f"Retrieved {len(patterns)} bot patterns")
            return list[str](patterns)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving bot patterns: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "author_patterns.bots", "error": str(e)},
                ),
                logger=logger,
            )
            return []  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid bot patterns configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "author_patterns.bots", "error": str(e)},
                ),
                logger=logger,
            )
            return []  # This line will never be reached due to log_and_raise

    def get_processing_config(self) -> dict[str, Any]:
        """Get processing configuration."""
        try:
            processing_config = self.config.get("processing", {})
            logger.debug(
                f"Retrieved processing configuration with {len(processing_config)} settings"
            )
            return dict[str, Any](processing_config)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving processing configuration: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "processing", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid processing configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "processing", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def get_timeout(self) -> int:
        """Get processing timeout in seconds."""
        try:
            timeout = self.get_processing_config().get("timeout_seconds", 60)
            logger.debug(f"Retrieved timeout setting: {timeout} seconds")
            return int(timeout)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving timeout setting: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "processing.timeout_seconds", "error": str(e)},
                ),
                logger=logger,
            )
            return 60  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid timeout configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "processing.timeout_seconds", "error": str(e)},
                ),
                logger=logger,
            )
            return 60  # This line will never be reached due to log_and_raise

    def get_git_fame_format(self) -> str:
        """Get git fame output format."""
        try:
            format_type = self.get_processing_config().get("git_fame_format", "json")
            logger.debug(f"Retrieved git fame format: {format_type}")
            return str(format_type)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving git fame format: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "processing.git_fame_format", "error": str(e)},
                ),
                logger=logger,
            )
            return "json"  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid git fame format configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "processing.git_fame_format", "error": str(e)},
                ),
                logger=logger,
            )
            return "json"  # This line will never be reached due to log_and_raise

    def get_report_config(self) -> dict[str, Any]:
        """Get report configuration."""
        try:
            report_config = self.config.get("report", {})
            logger.debug(
                f"Retrieved report configuration with {len(report_config)} settings"
            )
            return dict[str, Any](report_config)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving report configuration: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "report", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid report configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "report", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def get_report_title(self) -> str:
        """Get report title."""
        try:
            title = self.get_report_config().get(
                "title", "Repository Statistics Report"
            )
            logger.debug(f"Retrieved report title: {title}")
            return str(title)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving report title: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "report.title", "error": str(e)},
                ),
                logger=logger,
            )
            return "Repository Statistics Report"  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid report title configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "report.title", "error": str(e)},
                ),
                logger=logger,
            )
            return "Repository Statistics Report"  # This line will never be reached due to log_and_raise

    def get_date_format(self) -> str:
        """Get date format for reports."""
        try:
            date_format = self.get_report_config().get(
                "date_format", "%Y-%m-%d %H:%M:%S"
            )
            logger.debug(f"Retrieved date format: {date_format}")
            return str(date_format)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving date format: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "report.date_format", "error": str(e)},
                ),
                logger=logger,
            )
            return "%Y-%m-%d %H:%M:%S"  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid date format configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "report.date_format", "error": str(e)},
                ),
                logger=logger,
            )
            return "%Y-%m-%d %H:%M:%S"  # This line will never be reached due to log_and_raise

    def get_artifacts_config(self) -> dict[str, Any]:
        """Get artifacts configuration."""
        try:
            artifacts_config = self.config.get("artifacts", {})
            logger.debug(
                f"Retrieved artifacts configuration with {len(artifacts_config)} settings"
            )
            return dict[str, Any](artifacts_config)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving artifacts configuration: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "artifacts", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid artifacts configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "artifacts", "error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def get_retention_days(self) -> int:
        """Get artifact retention days."""
        try:
            retention = self.get_artifacts_config().get("retention_days", 7)
            logger.debug(f"Retrieved retention days: {retention}")
            return int(retention)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving retention days: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "artifacts.retention_days", "error": str(e)},
                ),
                logger=logger,
            )
            return 7  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid retention days configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "artifacts.retention_days", "error": str(e)},
                ),
                logger=logger,
            )
            return 7  # This line will never be reached due to log_and_raise

    def get_stats_filename(self) -> str:
        """Get stats filename."""
        try:
            filename = self.get_artifacts_config().get(
                "stats_filename", "repo_stats.json"
            )
            logger.debug(f"Retrieved stats filename: {filename}")
            return str(filename)
        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving stats filename: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"section": "artifacts.stats_filename", "error": str(e)},
                ),
                logger=logger,
            )
            return "repo_stats.json"  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid stats filename configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"section": "artifacts.stats_filename", "error": str(e)},
                ),
                logger=logger,
            )
            return "repo_stats.json"  # This line will never be reached due to log_and_raise

    def get_full_config(self) -> dict[str, Any]:
        """Get the complete configuration."""
        try:
            logger.debug("Retrieved full configuration")
            return self.config.copy()
        except (AttributeError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error retrieving full configuration: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"error": str(e)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def generate_clone_url(self, repository_name: str) -> str:
        """Generate clone URL for a repository."""
        try:
            github_config = self.get_github_config()
            organization = github_config.get("organization", "")
            base_url = github_config.get("base_url", "https://github.com")

            if not organization:
                log_and_raise(
                    ConfigError(
                        "GitHub organization not configured",
                        error_code=ErrorCodes.CONFIG_MISSING,
                        context={"section": "github.organization"},
                    ),
                    logger=logger,
                )

            clone_url = f"{base_url}/{organization}/{repository_name}.git"
            logger.debug(f"Generated clone URL for {repository_name}: {clone_url}")
            return clone_url

        except (KeyError, TypeError) as e:
            log_and_raise(
                ConfigError(
                    f"Error generating clone URL for {repository_name}: {e}",
                    error_code=ErrorCodes.CONFIG_MISSING,
                    context={"repository_name": repository_name, "error": str(e)},
                ),
                logger=logger,
            )
            return ""  # This line will never be reached due to log_and_raise
        except (AttributeError, ValueError) as e:
            log_and_raise(
                ConfigError(
                    f"Invalid configuration for clone URL generation: {e}",
                    error_code=ErrorCodes.CONFIG_INVALID,
                    context={"repository_name": repository_name, "error": str(e)},
                ),
                logger=logger,
            )
            return ""  # This line will never be reached due to log_and_raise

    def validate_config(self) -> list[str]:
        """Validate configuration and return list of validation errors."""
        try:
            errors = []
            logger.debug("Starting configuration validation")

            # Check required sections
            required_sections = ["repositories", "github", "author_patterns"]
            for section in required_sections:
                if section not in self.config:
                    errors.append(f"Missing required section: {section}")

            # Validate repositories
            if "repositories" in self.config:
                repositories = self.config["repositories"]
                if not isinstance(repositories, list):
                    errors.append("Repositories must be a list")
                else:
                    for i, repo in enumerate(repositories):
                        if not isinstance(repo, dict):
                            errors.append(f"Repository {i} must be a dictionary")
                        else:
                            required_fields = ["name", "display_name", "branch"]
                            for field in required_fields:
                                if field not in repo:
                                    errors.append(
                                        f"Repository {i} missing required field: {field}"
                                    )

            # Validate GitHub configuration
            if "github" in self.config:
                github_config = self.config["github"]
                if not isinstance(github_config, dict):
                    errors.append("GitHub configuration must be a dictionary")
                elif "organization" not in github_config:
                    errors.append("GitHub configuration missing organization")

            # Validate author patterns
            if "author_patterns" in self.config:
                patterns = self.config["author_patterns"]
                if not isinstance(patterns, dict):
                    errors.append("Author patterns must be a dictionary")
                else:
                    required_patterns = ["guillermo", "bots"]
                    for pattern_type in required_patterns:
                        if pattern_type not in patterns:
                            errors.append(
                                f"Missing author pattern type: {pattern_type}"
                            )
                        elif not isinstance(patterns[pattern_type], list):
                            errors.append(
                                f"Author pattern {pattern_type} must be a list"
                            )

            return errors

        except (TypeError, AttributeError, KeyError) as e:
            logger.error(f"Error during configuration validation: {e}")
            return [f"Configuration validation error: {e}"]
        except (ValueError, OSError) as e:
            logger.error(f"Error processing configuration: {e}")
            return [f"Configuration processing error: {e}"]


def create_config_manager(config_path: str | None = None) -> ConfigManager:
    """Factory function to create a ConfigManager instance."""
    try:
        logger.debug(f"Creating ConfigManager instance with path: {config_path}")
        return ConfigManager(config_path)
    except (FileNotFoundError, PermissionError) as e:
        log_and_raise(
            ConfigError(
                f"Could not create ConfigManager: {e}",
                error_code=ErrorCodes.CONFIG_ACCESS_FAILED,
                context={"config_path": config_path, "error": str(e)},
            ),
            logger=logger,
        )
        return ConfigManager()  # This line will never be reached due to log_and_raise
    except (yaml.YAMLError, TypeError) as e:
        log_and_raise(
            ConfigError(
                f"Invalid configuration: {e}",
                error_code=ErrorCodes.CONFIG_INVALID,
                context={"config_path": config_path, "error": str(e)},
            ),
            logger=logger,
        )
        return ConfigManager()  # This line will never be reached due to log_and_raise
    except OSError as e:
        log_and_raise(
            ConfigError(
                f"IO error creating ConfigManager: {e}",
                error_code=ErrorCodes.CONFIG_ACCESS_FAILED,
                context={"config_path": config_path, "error": str(e)},
            ),
            logger=logger,
        )
        return ConfigManager()  # This line will never be reached due to log_and_raise
