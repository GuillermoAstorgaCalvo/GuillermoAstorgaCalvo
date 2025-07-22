#!/usr/bin/env python3
"""
Generate API Tech Stack
Runs the API-based repository analyzer to generate tech stack from all repositories.
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from api_based_repository_analyzer import APIBasedRepositoryAnalyzer  # noqa: E402
from error_handling import get_logger  # noqa: E402

logger = get_logger(__name__)


def main() -> None:
    """Generate API-based tech stack."""
    try:
        print("🚀 Starting API-based tech stack analysis...")

        analyzer = APIBasedRepositoryAnalyzer()
        result = analyzer.generate_api_based_tech_stack()

        if result:
            print("✅ API-based tech stack generated successfully!")
            print(
                f"📊 Found {result.get('total_technologies', 0)} technologies across {result.get('repository_count', 0)} repositories"
            )

            tech_stack = result.get("tech_stack_analysis", {})
            for category, data in tech_stack.items():
                techs = data.get("technologies", [])
                if techs:
                    print(
                        f"🔧 {category.title()}: {', '.join(techs[:5])}{'...' if len(techs) > 5 else ''}"
                    )

            print("\n🔄 Now regenerating README with API-based tech stack...")

            # Regenerate README
            from enhanced_readme_generator import main as generate_readme

            generate_readme()

            print("✅ README updated with API-based tech stack!")
            print("\n🎉 Tech stack is now fully dynamic and based on:")
            print("   • GitHub API repository analysis")
            print("   • Dependency file content analysis")
            print("   • Repository structure detection")
            print("   • Description and topics analysis")

        else:
            print("❌ Failed to generate API-based tech stack")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error generating API-based tech stack: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
