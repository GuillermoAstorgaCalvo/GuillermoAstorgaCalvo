"""
Git Fame Parser Module
Handles parsing and processing of git fame output data.
"""

import json
import subprocess
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class GitFameParser:
    """Handles git fame execution and data parsing."""
    
    def __init__(self, timeout_seconds: int = 120):
        """
        Initialize the git fame parser.
        
        Args:
            timeout_seconds: Timeout for git fame execution
        """
        self.timeout_seconds = timeout_seconds
        self._check_git_fame_version()
    
    def _check_git_fame_version(self):
        """Check git fame version for compatibility."""
        try:
            result = subprocess.run(
                ['git', 'fame', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Git fame version: {version}")
            else:
                print("⚠️ Could not determine git fame version")
        except Exception as e:
            print(f"⚠️ Error checking git fame version: {e}")
    
    def execute_git_fame(self, repo_path: str, output_format: str = "json", by_type: bool = False) -> Optional[Dict[str, Any]]:
        """
        Execute git fame on a repository and return parsed data.
        
        Args:
            repo_path: Path to the git repository
            output_format: Output format for git fame (default: json)
            by_type: Whether to include --bytype flag for per-extension stats
            
        Returns:
            Parsed git fame data or None if execution failed
        """
        original_cwd = os.getcwd()
        
        try:
            if not Path(repo_path).exists():
                raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
            
            os.chdir(repo_path)
            
            # Build git fame command with optimizations for speed
            cmd = ['git', 'fame', '--format', output_format]
            if by_type:
                cmd.append('--bytype')
            
            # Execute git fame
            print(f"🔍 Running git fame command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=self.timeout_seconds
            )
            
            if result.returncode != 0:
                print(f"❌ Error running git fame: {result.stderr}")
                print(f"🔍 Command that failed: {' '.join(cmd)}")
                print(f"🔍 Return code: {result.returncode}")
                return None
            
            # Parse JSON output
            data = json.loads(result.stdout)
            return data
            
        except subprocess.TimeoutExpired:
            print(f"❌ Git fame execution timed out after {self.timeout_seconds} seconds")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse git fame JSON output: {e}")
            return None
        except Exception as e:
            print(f"❌ Exception during git fame execution: {e}")
            return None
        finally:
            os.chdir(original_cwd)
    
    def parse_author_data(self, author_data: Any) -> Optional[Tuple[str, int, int, int]]:
        """
        Parse individual author data from git fame output.
        
        Args:
            author_data: Raw author data from git fame (dict or list)
            
        Returns:
            Tuple of (author_name, loc, commits, files) or None if parsing failed
        """
        try:
            if isinstance(author_data, dict):
                author_name = author_data.get('author', '')
                loc = max(0, author_data.get('loc', 0))
                commits = max(0, author_data.get('commits', 0))
                files = max(0, author_data.get('files', 0))
            elif isinstance(author_data, list) and len(author_data) >= 4:
                author_name = author_data[0] if len(author_data) > 0 else ''
                loc = max(0, int(author_data[1]) if str(author_data[1]).isdigit() else 0)
                commits = max(0, int(author_data[2]) if str(author_data[2]).isdigit() else 0)
                files = max(0, int(author_data[3]) if str(author_data[3]).isdigit() else 0)
            else:
                return None
            
            return (author_name, loc, commits, files)
            
        except (ValueError, IndexError, TypeError):
            return None
    
    def get_repository_summary(self, data: Dict[str, Any]) -> Dict[str, int]:
        """
        Extract repository summary statistics from git fame data.
        
        Args:
            data: Parsed git fame data
            
        Returns:
            Dictionary with total_loc, total_commits, total_files
        """
        return {
            'total_loc': data.get('total_loc', 0),
            'total_commits': data.get('total_commits', 0),
            'total_files': data.get('total_files', 0)
        }
    
    def validate_git_fame_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate that git fame data contains expected fields.
        
        Args:
            data: Parsed git fame data
            
        Returns:
            True if data is valid, False otherwise
        """
        if not isinstance(data, dict):
            return False
        
        # Check for required fields
        required_fields = ['data']
        for field in required_fields:
            if field not in data:
                return False
        
        # Check that data is a list
        if not isinstance(data.get('data'), list):
            return False
        
        return True
    
    def extract_authors(self, data: Dict[str, Any]) -> List[Tuple[str, int, int, int]]:
        """
        Extract all author data from git fame output.
        
        Args:
            data: Parsed git fame data
            
        Returns:
            List of tuples (author_name, loc, commits, files)
        """
        authors = []
        
        for author_data in data.get('data', []):
            parsed_author = self.parse_author_data(author_data)
            if parsed_author:
                authors.append(parsed_author)
        
        return authors
    
    def extract_extension_stats(self, data: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
        """
        Extract per-extension statistics from git fame --bytype output.
        
        Args:
            data: Parsed git fame data with --bytype flag
            
        Returns:
            Dictionary with extension as key and stats as value
        """
        extension_stats = {}
        
        # Git fame --bytype puts extension stats in the 'total' section
        total_data = data.get('total', {})
        
        # Extract file extensions and their stats
        for key, value in total_data.items():
            if key.startswith('.') or key in ['Makefile', 'Dockerfile', 'CMakeLists.txt', 'package.json', 'requirements.txt', 'go.mod', 'Cargo.toml', 'composer.json', 'Gemfile']:
                # This is a file extension or special filename
                extension = key
                loc = value if isinstance(value, (int, float)) else 0
                
                # For --bytype, we get LOC per extension
                # Estimate file count based on LOC (roughly 1 file per 500 LOC)
                # This is a reasonable estimate since we can't get exact file counts from --bytype
                estimated_files = max(1, loc // 500) if loc > 0 else 0
                
                extension_stats[extension] = {
                    'loc': loc,
                    'commits': 0,  # Will be distributed from author analysis
                    'files': estimated_files
                }
        
        return extension_stats 