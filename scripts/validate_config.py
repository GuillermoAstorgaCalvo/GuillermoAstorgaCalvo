#!/usr/bin/env python3
"""
Configuration Validation Script
Validates the config.yml file to ensure it meets all requirements.
"""

import os
import sys
from typing import Any

import yaml


def validate_repository_config(repo: dict[str, Any], index: int) -> list[str]:
    """Validate a single repository configuration."""
    errors = []
    repo_name = repo.get("name", f"repository[{index}]")

    # Required fields
    required_fields = [
        "name",
        "display_name",
        "branch",
        "artifact_name",
        "organization",
        "token_type",
    ]
    for field in required_fields:
        if field not in repo:
            errors.append(f"Repository '{repo_name}' missing required field: {field}")
        elif not repo[field] or not str(repo[field]).strip():
            errors.append(f"Repository '{repo_name}' has empty {field}")

    # Validate token type
    token_type = repo.get("token_type")
    valid_token_types = ["personal", "private"]
    if token_type and token_type not in valid_token_types:
        errors.append(
            f"Repository '{repo_name}' has invalid token_type: {token_type}. Must be one of: {valid_token_types}"
        )

    # Validate organization format
    org = repo.get("organization")
    if org and not isinstance(org, str):
        errors.append(f"Repository '{repo_name}' organization must be a string")

    # Validate artifact name format
    artifact_name = repo.get("artifact_name")
    if artifact_name and not isinstance(artifact_name, str):
        errors.append(f"Repository '{repo_name}' artifact_name must be a string")

    return errors


def validate_config_file(config_path: str) -> list[str]:
    """Validate the entire configuration file."""
    errors = []

    try:
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not config:
            errors.append("config.yml is empty")
            return errors

        if not isinstance(config, dict):
            errors.append("config.yml must contain a dictionary")
            return errors

        # Check for repositories section
        repositories = config.get("repositories", [])
        if not repositories:
            errors.append("No repositories found in config.yml")
            return errors

        if not isinstance(repositories, list):
            errors.append("'repositories' must be a list")
            return errors

        # Validate each repository
        for i, repo in enumerate(repositories):
            if not isinstance(repo, dict):
                errors.append(f"Repository at index {i} must be a dictionary")
                continue

            repo_errors = validate_repository_config(repo, i)
            errors.extend(repo_errors)

        # Check for duplicate repository names
        repo_names = [repo.get("name") for repo in repositories if repo.get("name")]
        duplicate_names = [
            name for name in set(repo_names) if repo_names.count(name) > 1
        ]
        if duplicate_names:
            errors.append(f"Duplicate repository names found: {duplicate_names}")

        # Check for duplicate artifact names
        artifact_names = [
            repo.get("artifact_name")
            for repo in repositories
            if repo.get("artifact_name")
        ]
        duplicate_artifacts = [
            name for name in set(artifact_names) if artifact_names.count(name) > 1
        ]
        if duplicate_artifacts:
            errors.append(f"Duplicate artifact names found: {duplicate_artifacts}")

        # Validate other sections if present
        if "github" in config:
            github_config = config["github"]
            if not isinstance(github_config, dict):
                errors.append("'github' section must be a dictionary")

        if "external_services" in config:
            external_services = config["external_services"]
            if not isinstance(external_services, dict):
                errors.append("'external_services' section must be a dictionary")

        if "author_patterns" in config:
            author_patterns = config["author_patterns"]
            if not isinstance(author_patterns, dict):
                errors.append("'author_patterns' section must be a dictionary")

        if "processing" in config:
            processing = config["processing"]
            if not isinstance(processing, dict):
                errors.append("'processing' section must be a dictionary")

        if "report" in config:
            report = config["report"]
            if not isinstance(report, dict):
                errors.append("'report' section must be a dictionary")

        if "artifacts" in config:
            artifacts = config["artifacts"]
            if not isinstance(artifacts, dict):
                errors.append("'artifacts' section must be a dictionary")

        if "analytics" in config:
            analytics = config["analytics"]
            if not isinstance(analytics, dict):
                errors.append("'analytics' section must be a dictionary")

    except FileNotFoundError:
        errors.append(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        errors.append(f"Error parsing YAML: {e}")
    except Exception as e:
        errors.append(f"Unexpected error: {e}")

    return errors


def print_validation_summary(
    repositories: list[dict[str, Any]], errors: list[str]
) -> bool:
    """Print a summary of the validation results."""
    print("🔍 Configuration Validation Summary")
    print("=" * 50)

    if errors:
        print(f"❌ Found {len(errors)} validation errors:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()
        return False
    else:
        print("✅ Configuration validation passed!")
        print(f"📊 Found {len(repositories)} repositories:")
        for repo in repositories:
            name = repo.get("name", "unnamed")
            display_name = repo.get("display_name", "No display name")
            org = repo.get("organization", "No organization")
            token_type = repo.get("token_type", "No token type")
            print(f"  - {name} ({display_name}) - {org} ({token_type})")
        print()
        return True


def main() -> None:
    """Main function to validate configuration."""
    config_path = "config.yml"

    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)

    # Validate configuration
    errors = validate_config_file(config_path)

    # Load repositories for summary
    repositories = []
    try:
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
            repositories = config.get("repositories", [])
    except Exception:  # nosec B110: Generic exception handling for config loading
        pass

    # Print summary
    is_valid = print_validation_summary(repositories, errors)

    if not is_valid:
        print("💡 Configuration Tips:")
        print(
            "  - Ensure all repositories have required fields: name, display_name, branch, artifact_name, organization, token_type"
        )
        print("  - token_type must be either 'personal' or 'private'")
        print("  - organization must be a non-empty string")
        print("  - artifact_name must be unique across all repositories")
        print("  - repository names must be unique")
        print()
        print("📝 Example repository configuration:")
        print(
            """
  - name: "my-repo"
    display_name: "My Repository"
    branch: "main"
    artifact_name: "my-repo-stats"
    organization: "my-username"
    token_type: "personal"
        """
        )
        sys.exit(1)

    print("🎉 Configuration is valid and ready to use!")
    return None


if __name__ == "__main__":
    main()
