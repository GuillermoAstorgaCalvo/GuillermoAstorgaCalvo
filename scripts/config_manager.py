"""
Configuration Manager for Repository Statistics Workflow
Handles loading and accessing configuration data from YAML files.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class ConfigManager:
    """Manages configuration loading and access for the statistics workflow."""
    
    def __init__(self, config_path: str = "config.yml"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            
            if not self._config:
                raise ValueError("Configuration file is empty or invalid")
                
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the full configuration dictionary."""
        if self._config is None:
            raise RuntimeError("Configuration not loaded")
        return self._config
    
    def get_repositories(self) -> List[Dict[str, str]]:
        """Get the list of repositories to process."""
        return self.config.get('repositories', [])
    
    def get_repository_by_name(self, name: str) -> Optional[Dict[str, str]]:
        """Get repository configuration by name."""
        for repo in self.get_repositories():
            if repo.get('name') == name:
                return repo
        return None
    
    def get_github_config(self) -> Dict[str, str]:
        """Get GitHub-related configuration."""
        return self.config.get('github', {})
    
    def get_author_patterns(self) -> Dict[str, List[str]]:
        """Get author pattern matching configuration."""
        return self.config.get('author_patterns', {})
    
    def get_guillermo_patterns(self) -> List[str]:
        """Get Guillermo-specific author patterns."""
        return self.get_author_patterns().get('guillermo', [])
    
    def get_bot_patterns(self) -> List[str]:
        """Get bot author patterns."""
        return self.get_author_patterns().get('bots', [])
    
    def get_processing_config(self) -> Dict[str, Any]:
        """Get processing-related configuration."""
        return self.config.get('processing', {})
    
    def get_timeout_seconds(self) -> int:
        """Get git fame processing timeout in seconds."""
        return self.get_processing_config().get('timeout_seconds', 120)
    
    def get_git_fame_format(self) -> str:
        """Get git fame output format."""
        return self.get_processing_config().get('git_fame_format', 'json')
    
    def get_report_config(self) -> Dict[str, Any]:
        """Get report generation configuration."""
        return self.config.get('report', {})
    
    def get_report_title(self) -> str:
        """Get report title."""
        return self.get_report_config().get('title', '📊 Unified Code Statistics')
    
    def get_date_format(self) -> str:
        """Get date format for reports."""
        return self.get_report_config().get('date_format', '%B %d, %Y at %H:%M UTC')
    
    def get_artifacts_config(self) -> Dict[str, Any]:
        """Get artifact-related configuration."""
        return self.config.get('artifacts', {})
    
    def get_retention_days(self) -> int:
        """Get artifact retention days."""
        return self.get_artifacts_config().get('retention_days', 1)
    
    def get_stats_filename(self) -> str:
        """Get statistics output filename."""
        return self.get_artifacts_config().get('stats_filename', 'repo_stats.json')
    
    def get_report_filename(self) -> str:
        """Get report output filename."""
        return self.get_artifacts_config().get('report_filename', 'STATS.md')
    
    def get_clone_url(self, repository_name: str) -> str:
        """
        Generate git clone URL for a repository.
        
        Args:
            repository_name: Name of the repository
            
        Returns:
            Complete git clone URL
        """
        github_config = self.get_github_config()
        org = github_config.get('organization', '')
        base_url = github_config.get('base_url', 'https://github.com')
        
        return f"{base_url}/{org}/{repository_name}.git"
    
    def validate_config(self) -> List[str]:
        """
        Validate the configuration and return any validation errors.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Check required sections
        required_sections = ['repositories', 'github', 'author_patterns']
        for section in required_sections:
            if section not in self.config:
                errors.append(f"Missing required section: {section}")
        
        # Validate repositories
        repositories = self.get_repositories()
        if not repositories:
            errors.append("No repositories configured")
        else:
            for i, repo in enumerate(repositories):
                if not repo.get('name'):
                    errors.append(f"Repository {i}: Missing 'name' field")
                if not repo.get('display_name'):
                    errors.append(f"Repository {i}: Missing 'display_name' field")
        
        # Validate GitHub config
        github_config = self.get_github_config()
        if not github_config.get('organization'):
            errors.append("Missing GitHub organization")
        
        # Validate author patterns
        author_patterns = self.get_author_patterns()
        if not author_patterns.get('guillermo'):
            errors.append("Missing Guillermo author patterns")
        
        return errors


def get_config_manager(config_path: str = "config.yml") -> ConfigManager:
    """
    Factory function to create and return a ConfigManager instance.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        ConfigManager instance
    """
    return ConfigManager(config_path) 