#!/usr/bin/env python3
"""
Environment Manager
Manages environment variables for local development (.env) and production (GitHub Secrets).
"""

import os
from pathlib import Path

from dotenv import load_dotenv


class EnvManager:
    """Manages environment variables for different environments."""

    def __init__(self) -> None:
        """Initialize the environment manager."""
        self._load_env_file()

    def _load_env_file(self) -> None:
        """Load environment variables from .env file if it exists."""
        # Look for .env file in project root (parent of scripts directory)
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"

        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ Loaded environment from {env_file}")
        else:
            print(f"ℹ️ No .env file found at {env_file}")

    def get_private_token(self) -> str | None:
        """Get private repository token."""
        return os.environ.get("PRIVATE_REPOS_TOKEN")

    def get_personal_token(self) -> str | None:
        """Get personal repository token."""
        return os.environ.get("PERSONAL_REPOS_TOKEN")

    def get_token_by_type(self, token_type: str) -> str | None:
        """Get token by type (private or personal)."""
        if token_type == "private":
            return self.get_private_token()
        elif token_type == "personal":
            return self.get_personal_token()
        return None

    def get_repo_name(self) -> str | None:
        """Get repository name from environment."""
        return os.environ.get("REPO_NAME")

    def get_display_name(self) -> str | None:
        """Get display name from environment."""
        return os.environ.get("DISPLAY_NAME")

    def get_repos_dir(self) -> str:
        """Get repositories directory from environment with fallback."""
        return os.environ.get("REPOS_DIR", ".")

    def are_tokens_available(self) -> bool:
        """Check if both tokens are available."""
        return bool(self.get_private_token() and self.get_personal_token())

    def get_token_status(self) -> dict[str, bool]:
        """Get status of both tokens."""
        return {
            "PRIVATE_REPOS_TOKEN": bool(self.get_private_token()),
            "PERSONAL_REPOS_TOKEN": bool(self.get_personal_token()),
        }

    def create_env_template(self) -> None:
        """Create a .env template file."""
        project_root = Path(__file__).parent.parent
        env_template = project_root / ".env.template"

        template_content = """# GitHub Tokens for Tech Stack Analysis
# Copy this file to .env and fill in your tokens

# For private repositories (guillermo-affiliaction organization)
# Required permissions: repo:read, contents:read, metadata:read
PRIVATE_REPOS_TOKEN=your_private_token_here

# For personal repositories (GuillermoAstorgaCalvo user)
# Required permissions: repo:read, contents:read, metadata:read
PERSONAL_REPOS_TOKEN=your_personal_token_here

# Instructions:
# 1. Copy this file to .env
# 2. Replace the placeholder values with your actual tokens
# 3. Never commit .env to version control
# 4. For GitHub Actions, use repository secrets instead
"""

        with open(env_template, "w", encoding="utf-8") as f:
            f.write(template_content)

        print(f"✅ Created .env template at {env_template}")


# Global instance
env_manager = EnvManager()
