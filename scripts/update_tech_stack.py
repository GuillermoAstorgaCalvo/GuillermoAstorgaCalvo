#!/usr/bin/env python3
"""
Update Tech Stack
Updates the tech stack analysis and regenerates the README with the latest data.
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from enhanced_dependency_analyzer import EnhancedDependencyAnalyzer  # noqa: E402
from enhanced_readme_generator import main as generate_readme  # noqa: E402
from error_handling import get_logger  # noqa: E402

logger = get_logger(__name__)


def main() -> None:
    """Update tech stack and regenerate README."""
    try:
        print("🚀 Updating tech stack analysis...")

        # Generate enhanced tech stack
        analyzer = EnhancedDependencyAnalyzer()
        result = analyzer.generate_enhanced_tech_stack()

        if result:
            print("✅ Enhanced tech stack generated successfully!")
            print(
                f"📊 Found {result.get('total_technologies', 0)} technologies from {result.get('project_count', 0)} projects"
            )

            tech_stack = result.get("tech_stack_analysis", {})
            for category, data in tech_stack.items():
                techs = data.get("technologies", [])
                if techs:
                    print(
                        f"🔧 {category.title()}: {', '.join(techs[:5])}{'...' if len(techs) > 5 else ''}"
                    )

            print("\n🔄 Regenerating README with updated tech stack...")

            # Regenerate README
            generate_readme()

            print("✅ README updated with dynamic tech stack!")
            print("\n🎉 Tech stack is now fully dynamic and based on:")
            print("   • Current repository dependency analysis")
            print("   • Known project technology mapping")
            print("   • Common technology inclusion")

        else:
            print("❌ Failed to generate enhanced tech stack")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error updating tech stack: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
