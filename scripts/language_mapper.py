"""
Language Mapper Module
Maps file extensions to programming languages using GitHub Linguist's mapping.
"""

from typing import Dict, List, Optional, Any


class LanguageMapper:
    """Maps file extensions to programming languages."""
    
    def __init__(self):
        """Initialize the language mapper with GitHub Linguist's extension mapping."""
        # GitHub Linguist's extension to language mapping
        self.extension_to_language = {
            # Python
            '.py': 'Python', '.pyw': 'Python', '.pyi': 'Python', '.pyx': 'Python',
            '.pxd': 'Python', '.pyx': 'Python', '.pyo': 'Python', '.pyd': 'Python',
            
            # JavaScript/TypeScript
            '.js': 'JavaScript', '.jsx': 'JavaScript', '.mjs': 'JavaScript',
            '.ts': 'TypeScript', '.tsx': 'TypeScript',
            
            # Java
            '.java': 'Java', '.jav': 'Java',
            
            # C/C++
            '.c': 'C', '.h': 'C', '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++',
            '.c++': 'C++', '.hpp': 'C++', '.hxx': 'C++', '.h++': 'C++',
            
            # C#
            '.cs': 'C#', '.csx': 'C#',
            
            # PHP
            '.php': 'PHP', '.phtml': 'PHP', '.php3': 'PHP', '.php4': 'PHP',
            '.php5': 'PHP', '.phps': 'PHP',
            
            # Ruby
            '.rb': 'Ruby', '.rbw': 'Ruby', '.rake': 'Ruby', '.gemspec': 'Ruby',
            '.podspec': 'Ruby', '.irbrc': 'Ruby', '.pryrc': 'Ruby',
            
            # Go
            '.go': 'Go',
            
            # Rust
            '.rs': 'Rust',
            
            # Swift
            '.swift': 'Swift',
            
            # Kotlin
            '.kt': 'Kotlin', '.kts': 'Kotlin',
            
            # Scala
            '.scala': 'Scala', '.sc': 'Scala',
            
            # HTML/CSS
            '.html': 'HTML', '.htm': 'HTML', '.xhtml': 'HTML',
            '.css': 'CSS', '.scss': 'SCSS', '.sass': 'Sass', '.less': 'Less',
            
            # Shell/Bash
            '.sh': 'Shell', '.bash': 'Shell', '.zsh': 'Shell', '.fish': 'Shell',
            '.ksh': 'Shell', '.csh': 'Shell', '.tcsh': 'Shell',
            
            # PowerShell
            '.ps1': 'PowerShell', '.psm1': 'PowerShell', '.psd1': 'PowerShell',
            
            # SQL
            '.sql': 'SQL', '.ddl': 'SQL', '.dml': 'SQL',
            
            # R
            '.r': 'R', '.R': 'R', '.rdata': 'R', '.rds': 'R', '.rda': 'R',
            
            # MATLAB
            '.m': 'MATLAB', '.mat': 'MATLAB',
            
            # Julia
            '.jl': 'Julia',
            
            # Dart
            '.dart': 'Dart',
            
            # Lua
            '.lua': 'Lua',
            
            # Perl
            '.pl': 'Perl', '.pm': 'Perl', '.t': 'Perl', '.pod': 'Perl',
            
            # Haskell
            '.hs': 'Haskell', '.lhs': 'Haskell',
            
            # Clojure
            '.clj': 'Clojure', '.cljs': 'ClojureScript', '.cljc': 'Clojure',
            
            # Elixir
            '.ex': 'Elixir', '.exs': 'Elixir', '.eex': 'Elixir', '.heex': 'Elixir',
            
            # Erlang
            '.erl': 'Erlang', '.hrl': 'Erlang',
            
            # OCaml
            '.ml': 'OCaml', '.mli': 'OCaml',
            
            # F#
            '.fs': 'F#', '.fsi': 'F#', '.fsx': 'F#',
            
            # Assembly
            '.asm': 'Assembly', '.s': 'Assembly', '.S': 'Assembly',
            '.a51': 'Assembly', '.inc': 'Assembly', '.nasm': 'Assembly',
            
            # VHDL
            '.vhd': 'VHDL', '.vhdl': 'VHDL',
            
            # Verilog
            '.v': 'Verilog', '.vh': 'Verilog', '.sv': 'SystemVerilog',
            
            # TeX/LaTeX
            '.tex': 'TeX', '.ltx': 'TeX', '.sty': 'TeX', '.cls': 'TeX',
            '.bbl': 'TeX', '.bib': 'BibTeX',
            
            # Markdown
            '.md': 'Markdown', '.markdown': 'Markdown',
            
            # YAML
            '.yml': 'YAML', '.yaml': 'YAML',
            
            # JSON
            '.json': 'JSON',
            
            # XML
            '.xml': 'XML', '.xsd': 'XML', '.xsl': 'XML', '.xslt': 'XML',
            
            # CSV
            '.csv': 'CSV',
            
            # Docker
            '.dockerfile': 'Dockerfile', 'Dockerfile': 'Dockerfile',
            
            # Makefile
            'Makefile': 'Makefile', '.mk': 'Makefile', '.mak': 'Makefile',
            
            # CMake
            'CMakeLists.txt': 'CMake', '.cmake': 'CMake',
            
            # Gradle
            '.gradle': 'Gradle', 'build.gradle': 'Gradle',
            
            # Maven
            'pom.xml': 'Maven',
            
            # NPM
            'package.json': 'JSON', 'package-lock.json': 'JSON',
            
            # Yarn
            'yarn.lock': 'YAML',
            
            # Pip
            'requirements.txt': 'Text', 'setup.py': 'Python',
            
            # Cargo
            'Cargo.toml': 'TOML', 'Cargo.lock': 'TOML',
            
            # Composer
            'composer.json': 'JSON', 'composer.lock': 'JSON',
            
            # Gemfile
            'Gemfile': 'Ruby', 'Gemfile.lock': 'Ruby',
            
            # Go modules
            'go.mod': 'Go', 'go.sum': 'Go',
            
            # Rust
            '.toml': 'TOML',
            
            # Config files
            '.ini': 'INI', '.cfg': 'INI', '.conf': 'INI',
            '.properties': 'Properties', '.env': 'Properties',
            
            # Logs
            '.log': 'Log',
            
            # Documentation
            '.txt': 'Text', '.rst': 'reStructuredText', '.adoc': 'AsciiDoc',
            
            # Images (for completeness, but not code)
            '.png': 'Image', '.jpg': 'Image', '.jpeg': 'Image', '.gif': 'Image',
            '.svg': 'Image', '.ico': 'Image', '.bmp': 'Image', '.tiff': 'Image',
            
            # Fonts
            '.ttf': 'Font', '.otf': 'Font', '.woff': 'Font', '.woff2': 'Font',
            
            # Archives
            '.zip': 'Archive', '.tar': 'Archive', '.gz': 'Archive', '.rar': 'Archive',
            '.7z': 'Archive', '.bz2': 'Archive',
            
            # Binaries
            '.exe': 'Binary', '.dll': 'Binary', '.so': 'Binary', '.dylib': 'Binary',
            '.o': 'Binary', '.obj': 'Binary', '.a': 'Binary', '.lib': 'Binary',
        }
        
        # Language aliases for better categorization
        self.language_aliases = {
            'SCSS': 'CSS',
            'Sass': 'CSS',
            'Less': 'CSS',
            'reStructuredText': 'Documentation',
            'AsciiDoc': 'Documentation',
            'Markdown': 'Documentation',
            'BibTeX': 'Documentation',
            'Text': 'Documentation',
            'Log': 'Documentation',
            'Properties': 'Configuration',
            'INI': 'Configuration',
            'TOML': 'Configuration',
            'YAML': 'Configuration',
            'JSON': 'Configuration',
            'XML': 'Configuration',
            'CSV': 'Data',
            'Image': 'Assets',
            'Font': 'Assets',
            'Archive': 'Assets',
            'Binary': 'Assets',
        }
    
    def get_language_from_extension(self, extension: str) -> str:
        """
        Get language name from file extension.
        
        Args:
            extension: File extension (with or without dot)
            
        Returns:
            Language name or 'Unknown' if not recognized
        """
        # Normalize extension
        if not extension.startswith('.'):
            extension = '.' + extension
        
        # Get language from extension mapping
        language = self.extension_to_language.get(extension.lower(), 'Unknown')
        
        # Apply aliases for better categorization
        return self.language_aliases.get(language, language)
    
    def get_language_from_filename(self, filename: str) -> str:
        """
        Get language name from filename.
        
        Args:
            filename: Filename (with or without path)
            
        Returns:
            Language name or 'Unknown' if not recognized
        """
        # Handle special filenames (like Makefile, Dockerfile, etc.)
        basename = filename.split('/')[-1].split('\\')[-1]
        
        # Check for special filenames first
        if basename in self.extension_to_language:
            language = self.extension_to_language[basename]
            return self.language_aliases.get(language, language)
        
        # Extract extension
        if '.' in basename:
            extension = '.' + basename.split('.')[-1]
            return self.get_language_from_extension(extension)
        
        return 'Unknown'
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of all supported languages.
        
        Returns:
            List of unique language names
        """
        languages = set()
        for language in self.extension_to_language.values():
            aliased = self.language_aliases.get(language, language)
            languages.add(aliased)
        return sorted(list(languages))
    
    def get_language_stats(self, extension_stats: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
        """
        Convert extension-based stats to language-based stats.
        
        Args:
            extension_stats: Dictionary with extension as key and stats as value
            
        Returns:
            Dictionary with language as key and aggregated stats as value
        """
        language_stats = {}
        
        for extension, stats in extension_stats.items():
            language = self.get_language_from_extension(extension)
            
            if language not in language_stats:
                language_stats[language] = {
                    'loc': 0,
                    'commits': 0,
                    'files': 0
                }
            
            # Aggregate stats
            language_stats[language]['loc'] += stats.get('loc', 0)
            language_stats[language]['commits'] += stats.get('commits', 0)
            language_stats[language]['files'] += stats.get('files', 0)
        
        return language_stats


def get_language_mapper() -> LanguageMapper:
    """
    Factory function to create and return a LanguageMapper instance.
    
    Returns:
        LanguageMapper instance
    """
    return LanguageMapper() 