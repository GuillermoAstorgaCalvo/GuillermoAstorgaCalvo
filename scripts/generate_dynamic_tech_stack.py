#!/usr/bin/env python3
"""
Generate Dynamic Tech Stack
Runs the dynamic tech stack analyzer to generate tech stack from all repositories.
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from dynamic_tech_stack_analyzer import DynamicTechStackAnalyzer  # noqa: E402
from error_handling import get_logger  # noqa: E402

logger = get_logger(__name__)


def main() -> None:
    """Generate dynamic tech stack."""
    try:
        print("🚀 Starting dynamic tech stack analysis...")

        analyzer = DynamicTechStackAnalyzer()
        result = analyzer.generate_dynamic_tech_stack()

        if result:
            print("✅ Dynamic tech stack generated successfully!")
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

            print("\n🔄 Now regenerating README with dynamic tech stack...")

            # Regenerate README
            from enhanced_readme_generator import main as generate_readme

            generate_readme()

            print("✅ README updated with dynamic tech stack!")

        else:
            print("❌ Failed to generate dynamic tech stack")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error generating dynamic tech stack: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
