#!/usr/bin/env python3
"""
Generate language ranking SVG from unified stats
"""

import json
import sys
from pathlib import Path
from typing import Any

from error_handling import SvgGenerationError, get_logger, log_and_raise


def generate_language_svg_bar_chart(language_stats: dict, output_path: str) -> None:
    """Generate a modern SVG bar chart for language stats and save to output_path."""
    logger = get_logger(__name__)

    try:
        import svgwrite

        # Define categories to exclude (non-programming languages)
        excluded_categories = {
            # Configuration files
            "Configuration",
            "YAML",
            "JSON",
            "TOML",
            "INI",
            "Properties",
            # Non-code categories
            "Unknown",
            "Assets",
            "Documentation",
            "Image",
            "Font",
            "Archive",
            "Binary",
            # Other non-programming languages
            "Log",
            "Markdown",
            "reStructuredText",
            "AsciiDoc",
            "BibTeX",
        }

        # Filter out excluded categories and any with 0 lines
        valid_langs = [
            (lang, stats)
            for lang, stats in language_stats.items()
            if stats.get("lines", 0) > 0 and lang not in excluded_categories
        ]
        sorted_langs = sorted(valid_langs, key=lambda x: x[1]["lines"], reverse=True)

        if not sorted_langs:
            logger.warning("No valid languages found for SVG generation")
            return

        total_loc = sum(stats["lines"] for _, stats in sorted_langs)
        logger.info(
            f"Generating SVG for {len(sorted_langs)} languages with {total_loc:,} total LOC"
        )

        # Calculate chart dimensions
        width = 700  # Increased width for better spacing
        bar_height = 35
        max_bar_width = width - 250  # Space for labels and values
        height = bar_height * len(sorted_langs) + 80

        dwg = svgwrite.Drawing(output_path, size=(width, height))

        # Define gradients for better visual appeal
        # Add gradients directly to dwg.defs
        # Gradient for major languages (>50%)
        major_gradient = dwg.linearGradient(
            id="major_gradient", x1="0%", y1="0%", x2="100%", y2="0%"
        )
        major_gradient.add_stop_color(offset="0%", color="#4F8EF7", opacity=1)
        major_gradient.add_stop_color(offset="100%", color="#2E5BB8", opacity=1)
        dwg.defs.add(major_gradient)
        # Gradient for medium languages (10-50%)
        medium_gradient = dwg.linearGradient(
            id="medium_gradient", x1="0%", y1="0%", x2="100%", y2="0%"
        )
        medium_gradient.add_stop_color(offset="0%", color="#6BB6FF", opacity=1)
        medium_gradient.add_stop_color(offset="100%", color="#4F8EF7", opacity=1)
        dwg.defs.add(medium_gradient)
        # Gradient for minor languages (<10%)
        minor_gradient = dwg.linearGradient(
            id="minor_gradient", x1="0%", y1="0%", x2="100%", y2="0%"
        )
        minor_gradient.add_stop_color(offset="0%", color="#A8D8FF", opacity=1)
        minor_gradient.add_stop_color(offset="100%", color="#6BB6FF", opacity=1)
        dwg.defs.add(minor_gradient)
        # Add background with subtle gradient
        bg_gradient = dwg.linearGradient(
            id="bg_gradient", x1="0%", y1="0%", x2="0%", y2="100%"
        )
        bg_gradient.add_stop_color(offset="0%", color="#FAFBFC", opacity=1)
        bg_gradient.add_stop_color(offset="100%", color="#F5F7FA", opacity=1)
        dwg.defs.add(bg_gradient)

        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="url(#bg_gradient)"))

        # Add title with better styling
        title_group = dwg.g()
        title_group.add(
            dwg.text(
                "💻 Top Programming Languages",
                insert=(15, 30),
                font_size="22px",
                font_weight="bold",
                font_family="Segoe UI, Arial, sans-serif",
                fill="#1A1A1A",
            )
        )
        title_group.add(
            dwg.text(
                "by Lines of Code",
                insert=(15, 50),
                font_size="14px",
                font_family="Segoe UI, Arial, sans-serif",
                fill="#666",
            )
        )
        dwg.add(title_group)

        # Add total stats
        total_text = f"Total: {total_loc:,} LOC across {len(sorted_langs)} languages"
        dwg.add(
            dwg.text(
                total_text,
                insert=(width - 15, 25),
                font_size="12px",
                font_family="Segoe UI, Arial, sans-serif",
                fill="#888",
                text_anchor="end",
            )
        )

        y = 70
        processed_languages = 0
        for i, (lang, stats) in enumerate(sorted_langs):
            try:
                loc = stats.get("lines", 0)

                # Calculate bar width based on percentage of total (not max)
                if total_loc > 0:
                    bar_ratio = loc / total_loc
                    bar_width = int(bar_ratio * max_bar_width)  # Minimum 25px width
                else:
                    bar_width = 0

                # Clamp bar width to max_bar_width
                bar_width = min(bar_width, max_bar_width)

                # Calculate percentage based on total LOC (not max LOC)
                percentage = (loc / total_loc) * 100 if total_loc > 0 else 0

                # Bar color based on percentage of total
                if percentage > 50:
                    gradient_id = "major_gradient"
                    rank_emoji = "🥇"
                elif percentage > 10:
                    gradient_id = "medium_gradient"
                    rank_emoji = "🥈"
                else:
                    gradient_id = "minor_gradient"
                    rank_emoji = "🥉"

                # Always place LOC at the far right
                loc_margin = 15
                loc_x = width - loc_margin
                # Percentage logic as before
                pct_font_size = 12
                pct_margin = 10
                pct_inside_threshold = (
                    60  # px, bar must be at least this wide to fit percentage inside
                )
                pct_text = f"{percentage:.1f}%"
                pct_y = y - 2
                pct_fill_inside = "#fff"  # White text inside bar
                pct_fill_outside = "#4F8EF7"  # Brand color outside bar
                # Ensure bar never overlaps LOC value
                max_bar_width_adjusted = (
                    loc_x - 200 - 60
                )  # 60px buffer for LOC and margin
                bar_width = min(bar_width, max_bar_width_adjusted)
                # Percentage placement
                if bar_width >= pct_inside_threshold:
                    pct_x = 200 + bar_width - pct_margin
                    pct_anchor = "end"
                    pct_fill = pct_fill_inside
                else:
                    pct_x = 200 + bar_width + pct_margin
                    pct_anchor = "start"
                    pct_fill = pct_fill_outside
                # Draw bar with shadow effect
                shadow_offset = 2
                dwg.add(
                    dwg.rect(
                        insert=(200 + shadow_offset, y - 17 + shadow_offset),
                        size=(bar_width, 24),
                        fill="#000000",
                        opacity=0.1,
                        rx=6,
                        ry=6,
                    )
                )
                # Main bar
                dwg.add(
                    dwg.rect(
                        insert=(200, y - 17),
                        size=(bar_width, 24),
                        fill=f"url(#{gradient_id})",
                        rx=6,
                        ry=6,
                    )
                )
                # Add subtle border
                dwg.add(
                    dwg.rect(
                        insert=(200, y - 17),
                        size=(bar_width, 24),
                        fill="none",
                        stroke="#FFFFFF",
                        stroke_width=1,
                        opacity=0.3,
                        rx=6,
                        ry=6,
                    )
                )

                # Rank and language name
                rank_text = f"{i + 1}."
                dwg.add(
                    dwg.text(
                        rank_text,
                        insert=(15, y - 2),
                        font_size="12px",
                        font_weight="bold",
                        font_family="Segoe UI, Arial, sans-serif",
                        fill="#666",
                    )
                )

                # Language name with emoji
                lang_text = f"{rank_emoji} {lang}"
                if len(lang) > 12:
                    lang_text = f"{rank_emoji} {lang[:10]}..."
                dwg.add(
                    dwg.text(
                        lang_text,
                        insert=(35, y - 2),
                        font_size="14px",
                        font_weight="bold",
                        font_family="Segoe UI, Arial, sans-serif",
                        fill="#1A1A1A",
                    )
                )

                # LOC value at far right
                loc_text = f"{loc:,}"
                dwg.add(
                    dwg.text(
                        loc_text,
                        insert=(loc_x, y - 2),
                        font_size="13px",
                        font_weight="bold",
                        font_family="Segoe UI, Arial, sans-serif",
                        fill="#1A1A1A",
                        text_anchor="end",
                    )
                )
                # "LOC" label
                dwg.add(
                    dwg.text(
                        "LOC",
                        insert=(loc_x, y + 10),
                        font_size="10px",
                        font_family="Segoe UI, Arial, sans-serif",
                        fill="#666",
                        text_anchor="end",
                    )
                )
                # Percentage as before
                dwg.add(
                    dwg.text(
                        pct_text,
                        insert=(pct_x, pct_y),
                        font_size=f"{pct_font_size}px",
                        font_weight="bold",
                        font_family="Segoe UI, Arial, sans-serif",
                        fill=pct_fill,
                        text_anchor=pct_anchor,
                    )
                )

                processed_languages += 1
                y += bar_height

            except Exception as e:
                logger.error(f"Error processing language {lang}: {e}")
                continue

        # Add footer with timestamp and stats
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

        # Footer background
        footer_bg = dwg.rect(
            insert=(0, height - 25),
            size=(width, 25),
            fill="#F8F9FA",
            stroke="#E9ECEF",
            stroke_width=1,
        )
        dwg.add(footer_bg)

        # Footer text with excluded files info
        footer_text = f"📊 Generated on {timestamp} | Total: {total_loc:,} LOC | {len(sorted_langs)} languages | (excluded unnecessary files extensions like .svg, .json, .txt, .md, .log, .cfg, etc...)"
        dwg.add(
            dwg.text(
                footer_text,
                insert=(15, height - 8),
                font_size="10px",
                font_family="Segoe UI, Arial, sans-serif",
                fill="#666",
            )
        )

        dwg.save()
        logger.info(
            f"Successfully generated SVG with {processed_languages} languages at {output_path}"
        )

    except ImportError as e:
        logger.warning(f"svgwrite not available, creating text fallback: {e}")
        # Create a simple text-based fallback
        try:
            fallback_path = output_path.replace(".svg", ".txt")
            with open(fallback_path, "w") as f:
                f.write("Language Statistics (SVG not available):\n")
                for lang, stats in sorted(
                    language_stats.items(),
                    key=lambda x: x[1].get("lines", 0),
                    reverse=True,
                ):
                    f.write(f"{lang}: {stats.get('lines', 0):,} LOC\n")
            logger.info(f"Created text fallback at {fallback_path}")
        except Exception as fallback_error:
            logger.error(f"Failed to create text fallback: {fallback_error}")
    except Exception as e:
        log_and_raise(
            SvgGenerationError,
            f"Error generating SVG chart: {e}",
            error_code="SVG_GENERATION_ERROR",
        )


def load_unified_stats(
    unified_stats_path: str = "unified_stats.json",
) -> dict[str, Any]:
    """Load unified statistics from JSON file."""
    logger = get_logger(__name__)
    try:
        with open(unified_stats_path, encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"Loading unified stats from {unified_stats_path}")
        if isinstance(data, dict):
            return data
        else:
            logger.error("Unified stats data is not a dictionary")
            return {}
    except (FileNotFoundError, PermissionError) as e:
        logger.warning(f"Could not read {unified_stats_path}: {e}")
        return {}
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in {unified_stats_path}: {e}")
        return {}
    except OSError as e:
        logger.error(f"IO error reading {unified_stats_path}: {e}")
        return {}


def extract_language_stats(data: dict[str, Any]) -> dict[str, int]:
    """Extract language statistics from unified stats data."""
    logger = get_logger(__name__)
    try:
        language_stats = data.get("unified_language_stats", {})

        # Filter out non-code languages and configuration files
        filtered_stats = {}
        for lang, stats in language_stats.items():
            try:
                if isinstance(stats, dict) and "loc" in stats:
                    loc = stats.get("loc", 0)
                    if loc > 0 and lang.lower() not in [
                        "other",
                        "unknown",
                        "text",
                        "markdown",
                    ]:
                        filtered_stats[lang] = loc
            except (TypeError, AttributeError, KeyError) as e:
                logger.warning(f"Error processing language {lang}: {e}")
                continue

        return filtered_stats

    except (TypeError, AttributeError, KeyError) as e:
        logger.error(f"Error extracting language stats: {e}")
        return {}


def save_svg(svg_content: str, output_path: str) -> bool:
    """Save SVG content to file."""
    logger = get_logger(__name__)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        logger.info(f"SVG saved to {output_path}")
        return True
    except (PermissionError, OSError) as e:
        logger.error(f"Could not write to {output_path}: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Error writing SVG content: {e}")
        return False


def main() -> None:
    """Generate SVG from unified stats"""
    logger = get_logger(__name__)

    try:
        logger.info("Starting language SVG generation")

        # Load unified stats from project root (when running from scripts directory)
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent
        unified_stats_path = root_dir / "unified_stats.json"

        # If not found in root, try current directory (for local testing)
        if not unified_stats_path.exists():
            unified_stats_path = Path("unified_stats.json")

        if not unified_stats_path.exists():
            log_and_raise(
                SvgGenerationError(
                    f"unified_stats.json not found at {unified_stats_path}",
                    error_code="STATS_FILE_NOT_FOUND",
                )
            )

        logger.debug(f"Loading unified stats from {unified_stats_path}")
        with open(unified_stats_path, encoding="utf-8") as f:
            unified_stats = json.load(f)
            if not isinstance(unified_stats, dict):
                log_and_raise(
                    SvgGenerationError(
                        "Unified stats data is not a dictionary",
                        error_code="INVALID_DATA_FORMAT",
                    )
                )

        # Extract language stats
        language_stats = unified_stats.get("unified_language_stats", {})
        if not language_stats:
            log_and_raise(
                SvgGenerationError(
                    "No language stats data found in unified stats",
                    error_code="NO_LANGUAGE_DATA",
                )
            )

        # Convert language stats to the format expected by the SVG generator
        language_analysis = {}
        for lang, stats in language_stats.items():
            language_analysis[lang] = {
                "lines": stats.get("loc", 0),
                "commits": stats.get("commits", 0),
                "files": stats.get("files", 0),
                "percentage": 0,  # Will be calculated below
            }

        # Calculate percentages
        total_loc = sum(stats.get("loc", 0) for stats in language_stats.values())
        for lang in language_analysis:
            if total_loc > 0:
                language_analysis[lang]["percentage"] = round(
                    (language_analysis[lang]["lines"] / total_loc) * 100, 2
                )

        logger.info(f"Found language stats with {len(language_stats)} languages")
        logger.info(
            f"Converted to language analysis with {len(language_analysis)} languages"
        )
        if language_analysis:
            logger.info(f"Languages found: {list(language_analysis.keys())}")

        # Generate SVG
        svg_path = root_dir / "assets" / "language_stats.svg"
        svg_path.parent.mkdir(exist_ok=True)  # Ensure assets directory exists

        generate_language_svg_bar_chart(language_analysis, str(svg_path))
        logger.info(f"Language SVG successfully generated at {svg_path}")

    except SvgGenerationError as e:
        logger.error(f"SVG generation failed: {e}")
        raise
    except FileNotFoundError as e:
        log_and_raise(
            SvgGenerationError(
                f"Required file not found: {e}",
                error_code="FILE_NOT_FOUND",
            )
        )
    except json.JSONDecodeError as e:
        log_and_raise(
            SvgGenerationError(
                f"Invalid JSON in unified stats: {e}",
                error_code="INVALID_JSON",
            )
        )
    except PermissionError as e:
        log_and_raise(
            SvgGenerationError(
                f"Permission denied: {e}",
                error_code="PERMISSION_DENIED",
            )
        )
    except Exception as e:
        log_and_raise(
            SvgGenerationError(
                f"Unexpected error in SVG generation: {e}",
                error_code="UNEXPECTED_ERROR",
            )
        )


if __name__ == "__main__":
    try:
        main()
    except SvgGenerationError as e:
        get_logger(__name__).error(f"SVG generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        get_logger(__name__).error(
            f"Unexpected error in SVG generation: {e}", exc_info=True
        )
        sys.exit(1)
