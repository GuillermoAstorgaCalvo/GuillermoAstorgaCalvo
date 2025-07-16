#!/usr/bin/env python3
"""
Manual README Regenerator
Quick script to regenerate README from current analytics data
"""

import os
import sys
import subprocess
from error_handling import (
    setup_logging, DataProcessingError, log_and_raise, get_logger, ErrorCodes, with_error_context
)

# Set up logging for this module
logger = get_logger(__name__)


@with_error_context({'component': 'regenerate_readme'})
def main():
    """Main function to regenerate README."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logger.debug(f"Changing to script directory: {script_dir}")
        
        # Change to the script directory
        os.chdir(script_dir)
        
        # Run the enhanced README generator
        result = subprocess.run([
            sys.executable, 'enhanced_readme_generator.py'
        ], capture_output=True, text=True, timeout=300)
        
        logger.debug(f"README generation completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            logger.info("README regenerated successfully")
            if result.stdout:
                logger.debug(f"Generation output: {result.stdout}")
        else:
            logger.error(f"README generation failed with return code {result.returncode}")
            if result.stderr:
                logger.error(f"Error output: {result.stderr}")
                
    except subprocess.TimeoutExpired as e:
        logger.error(f"README generation timed out after 300 seconds: {e}")
    except subprocess.CalledProcessError as e:
        logger.error(f"README generation process error: {e}")
    except (OSError, IOError) as e:
        logger.error(f"IO error during README generation: {e}")
    except (TypeError, ValueError) as e:
        logger.error(f"Error during README generation: {e}")


if __name__ == "__main__":
    try:
        main()
    except DataProcessingError as e:
        logger.error(f"README regeneration failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in README regeneration: {e}", exc_info=True)
        sys.exit(1) 