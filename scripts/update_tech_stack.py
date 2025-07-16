#!/usr/bin/env python3
"""
Update Tech Stack Script
Updates the existing unified_stats.json to use the new tech stack format with actual technologies.
"""

import json
from pathlib import Path
from error_handling import (
    setup_logging, DataProcessingError, log_and_raise, get_logger, ErrorCodes, with_error_context
)

# Set up logging for this module
logger = get_logger(__name__)


@with_error_context({'component': 'update_tech_stack'})
def update_tech_stack_format():
    """Update the tech stack format in unified_stats.json."""
    
    try:
        # Load current unified stats
        with open('unified_stats.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update tech stack format
        if 'tech_stack' in data:
            tech_stack = data['tech_stack']
            updated_tech_stack = {}
            
            for category_name, category in tech_stack.items():
                try:
                    if isinstance(category, dict) and 'technologies' in category:
                        technologies = category['technologies']
                        total_loc = category.get('total_loc', 0)
                        
                        # Convert to new format
                        updated_tech_stack[category_name] = {
                            'technologies': technologies,
                            'total_loc': total_loc
                        }
                        
                        logger.debug(f"Category {category_name}: {len(category['technologies'])} unique technologies, {category['total_loc']} total LOC")
                    else:
                        logger.warning(f"Invalid category format for {category_name}")
                        
                except (TypeError, AttributeError, KeyError) as e:
                    logger.warning(f"Error processing category {category_name}: {e}")
                    continue
            
            # Update the data
            data['tech_stack'] = updated_tech_stack
            
            # Save updated data
            with open('unified_stats.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info("Tech stack format updated successfully")
            
        else:
            logger.info("No tech_stack found in unified_stats.json")
            
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"Could not read/write unified_stats.json: {e}")
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Invalid JSON in unified_stats.json: {e}")
    except (OSError, IOError) as e:
        logger.error(f"IO error processing unified_stats.json: {e}")


if __name__ == "__main__":
    try:
        update_tech_stack_format()
    except DataProcessingError as e:
        logger.error(f"Tech stack update failed: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in tech stack update: {e}", exc_info=True)
        exit(1) 