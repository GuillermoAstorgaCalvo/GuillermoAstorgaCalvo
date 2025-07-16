"""
Language Mapper Module
Maps file extensions to programming languages using GitHub Linguist's mapping.
"""

import os
from typing import Any

from error_handling import LanguageMappingError, get_logger, log_and_raise


class LanguageMapper:
    """Maps file extensions to programming languages with high accuracy."""

    def __init__(self) -> None:
        """Initialize the language mapper with detailed mapping."""
        self.logger = get_logger(__name__)

        try:
            # Core programming languages with their extensions
            self.extension_to_language: dict[str, str] = {
                # Python
                ".py": "Python",
                ".pyw": "Python",
                ".pyi": "Python",
                ".pyx": "Python",
                ".pxd": "Python",
                ".pyo": "Python",
                ".pyd": "Python",
                ".pyc": "Python",
                # JavaScript/TypeScript
                ".js": "JavaScript",
                ".jsx": "JavaScript",
                ".mjs": "JavaScript",
                ".ts": "TypeScript",
                ".tsx": "TypeScript",
                # Java
                ".java": "Java",
                ".jav": "Java",
                ".class": "Java",
                # C/C++
                ".c": "C",
                ".h": "C",
                ".cpp": "C++",
                ".cc": "C++",
                ".cxx": "C++",
                ".c++": "C++",
                ".hpp": "C++",
                ".hxx": "C++",
                ".h++": "C++",
                # C#
                ".cs": "C#",
                ".csx": "C#",
                # PHP
                ".php": "PHP",
                ".phtml": "PHP",
                ".php3": "PHP",
                ".php4": "PHP",
                ".php5": "PHP",
                ".phps": "PHP",
                # Ruby
                ".rb": "Ruby",
                ".rbw": "Ruby",
                ".rake": "Ruby",
                ".gemspec": "Ruby",
                ".podspec": "Ruby",
                ".irbrc": "Ruby",
                ".pryrc": "Ruby",
                # Go
                ".go": "Go",
                # Rust
                ".rs": "Rust",
                # Swift
                ".swift": "Swift",
                # Kotlin
                ".kt": "Kotlin",
                ".kts": "Kotlin",
                # Scala
                ".scala": "Scala",
                ".sc": "Scala",
                # HTML/CSS
                ".html": "HTML",
                ".htm": "HTML",
                ".xhtml": "HTML",
                ".css": "CSS",
                ".scss": "SCSS",
                ".sass": "Sass",
                ".less": "Less",
                # Shell/Bash
                ".sh": "Shell",
                ".bash": "Shell",
                ".zsh": "Shell",
                ".fish": "Shell",
                ".ksh": "Shell",
                ".csh": "Shell",
                ".tcsh": "Shell",
                # PowerShell
                ".ps1": "PowerShell",
                ".psm1": "PowerShell",
                ".psd1": "PowerShell",
                # SQL
                ".sql": "SQL",
                ".ddl": "SQL",
                ".dml": "SQL",
                # R
                ".r": "R",
                ".R": "R",
                ".rdata": "R",
                ".rds": "R",
                ".rda": "R",
                # MATLAB
                ".m": "MATLAB",
                ".mat": "MATLAB",
                # Julia
                ".jl": "Julia",
                # Dart
                ".dart": "Dart",
                # Lua
                ".lua": "Lua",
                # Perl
                ".pl": "Perl",
                ".pm": "Perl",
                ".t": "Perl",
                ".pod": "Perl",
                # Haskell
                ".hs": "Haskell",
                ".lhs": "Haskell",
                # Clojure
                ".clj": "Clojure",
                ".cljs": "ClojureScript",
                ".cljc": "Clojure",
                # Elixir
                ".ex": "Elixir",
                ".exs": "Elixir",
                ".eex": "Elixir",
                ".heex": "Elixir",
                # Erlang
                ".erl": "Erlang",
                ".hrl": "Erlang",
                # OCaml
                ".ml": "OCaml",
                ".mli": "OCaml",
                # F#
                ".fs": "F#",
                ".fsi": "F#",
                ".fsx": "F#",
                # Assembly
                ".asm": "Assembly",
                ".s": "Assembly",
                ".S": "Assembly",
                ".a51": "Assembly",
                ".inc": "Assembly",
                ".nasm": "Assembly",
                # VHDL
                ".vhd": "VHDL",
                ".vhdl": "VHDL",
                # Verilog
                ".v": "Verilog",
                ".vh": "Verilog",
                ".sv": "SystemVerilog",
                # TeX/LaTeX
                ".tex": "TeX",
                ".ltx": "TeX",
                ".sty": "TeX",
                ".cls": "TeX",
                ".bbl": "TeX",
                ".bib": "BibTeX",
                # Markdown
                ".md": "Markdown",
                ".markdown": "Markdown",
                # YAML
                ".yml": "YAML",
                ".yaml": "YAML",
                # JSON
                ".json": "JSON",
                # XML
                ".xml": "XML",
                ".xsd": "XML",
                ".xsl": "XML",
                ".xslt": "XML",
                # CSV
                ".csv": "CSV",
                # Docker
                ".dockerfile": "Dockerfile",
                "Dockerfile": "Dockerfile",
                # Makefile
                "Makefile": "Makefile",
                ".mk": "Makefile",
                ".mak": "Makefile",
                # CMake
                "CMakeLists.txt": "CMake",
                ".cmake": "CMake",
                # Gradle
                ".gradle": "Gradle",
                "build.gradle": "Gradle",
                # Maven
                "pom.xml": "Maven",
                # NPM
                "package.json": "JSON",
                "package-lock.json": "JSON",
                # Yarn
                "yarn.lock": "YAML",
                # Pip
                "requirements.txt": "Python",
                "setup.py": "Python",
                "Pipfile": "Python",
                "pyproject.toml": "Python",
                # Cargo
                "Cargo.toml": "TOML",
                "Cargo.lock": "TOML",
                # Composer
                "composer.json": "JSON",
                "composer.lock": "JSON",
                # Gemfile
                "Gemfile": "Ruby",
                "Gemfile.lock": "Ruby",
                # Go modules
                "go.mod": "Go",
                "go.sum": "Go",
                # Rust
                ".toml": "TOML",
                # Config files - be more specific
                ".ini": "INI",
                ".cfg": "INI",
                ".conf": "INI",
                ".properties": "Properties",
                ".env": "Properties",
                # Logs
                ".log": "Log",
                # Documentation (excluding .txt files which are mostly logs)
                ".rst": "reStructuredText",
                ".adoc": "AsciiDoc",
                # Images (for completeness, but not code)
                ".png": "Image",
                ".jpg": "Image",
                ".jpeg": "Image",
                ".gif": "Image",
                ".svg": "Image",
                ".ico": "Image",
                ".bmp": "Image",
                ".tiff": "Image",
                # Fonts
                ".ttf": "Font",
                ".otf": "Font",
                ".woff": "Font",
                ".woff2": "Font",
                # Archives
                ".zip": "Archive",
                ".tar": "Archive",
                ".gz": "Archive",
                ".rar": "Archive",
                ".7z": "Archive",
                ".bz2": "Archive",
                # Binaries
                ".exe": "Binary",
                ".dll": "Binary",
                ".so": "Binary",
                ".dylib": "Binary",
                ".o": "Binary",
                ".obj": "Binary",
                ".a": "Binary",
                ".lib": "Binary",
            }

            # Specific filename mappings (case-sensitive)
            self.filename_to_language = {
                "Dockerfile": "Dockerfile",
                "Makefile": "Makefile",
                "CMakeLists.txt": "CMake",
                "package.json": "JSON",
                "package-lock.json": "JSON",
                "yarn.lock": "YAML",
                "requirements.txt": "Python",
                "setup.py": "Python",
                "Pipfile": "Python",
                "pyproject.toml": "Python",
                "Cargo.toml": "TOML",
                "Cargo.lock": "TOML",
                "composer.json": "JSON",
                "composer.lock": "JSON",
                "Gemfile": "Ruby",
                "Gemfile.lock": "Ruby",
                "go.mod": "Go",
                "go.sum": "Go",
                "pom.xml": "Maven",
                "build.gradle": "Gradle",
            }

            # Minimal aliases - only for very similar languages
            self.language_aliases = {
                "SCSS": "CSS",
                "Sass": "CSS",
                "Less": "CSS",
                "reStructuredText": "Documentation",
                "AsciiDoc": "Documentation",
                "Markdown": "Documentation",
                "BibTeX": "Documentation",
                "Log": "Documentation",
                "Image": "Assets",
                "Font": "Assets",
                "Archive": "Assets",
                "Binary": "Assets",
            }

            self.logger.info(
                f"LanguageMapper initialized with {len(self.extension_to_language)} extension mappings and {len(self.filename_to_language)} filename mappings"
            )

        except Exception as e:
            log_and_raise(
                LanguageMappingError,
                f"Error initializing LanguageMapper: {e}",
                error_code="INITIALIZATION_ERROR",
            )

    def map_extension_to_language(self, extension: str) -> str:
        """
        Map a file extension to a programming language.

        Args:
            extension: File extension (e.g., '.py', '.js')

        Returns:
            Language name or 'Unknown' if not found
        """
        try:
            if not extension:
                return "Unknown"

            # Normalize extension
            extension = extension.lower().strip()
            if not extension.startswith("."):
                extension = "." + extension

            # Check direct mapping
            if extension in self.extension_to_language:
                language = self.extension_to_language[extension]
                self.logger.debug(
                    f"Mapped extension '{extension}' to language '{language}'"
                )
                return language

            # Check aliases
            for aliased_language, aliases in self.language_aliases.items():
                if extension in aliases:
                    self.logger.debug(
                        f"Mapped extension '{extension}' to language '{aliased_language}'"
                    )
                    return aliased_language

            return "Unknown"

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error mapping extension '{extension}' to language: {e}")
            return "Unknown"

    def map_filename_to_language(self, filename: str) -> str:
        """
        Map a filename to a programming language.

        Args:
            filename: Filename (e.g., 'Dockerfile', 'Makefile')

        Returns:
            Language name or 'Unknown' if not found
        """
        try:
            if not filename:
                return "Unknown"

            # Normalize filename
            filename = filename.strip()
            basename = os.path.basename(filename)

            # Check special filenames
            if basename in self.filename_to_language:
                language = self.filename_to_language[basename]
                self.logger.debug(
                    f"Mapped filename '{basename}' to language '{language}'"
                )
                return language

            return "Unknown"

        except (TypeError, AttributeError, KeyError, OSError) as e:
            self.logger.error(f"Error mapping filename '{filename}' to language: {e}")
            return "Unknown"

    def get_supported_languages(self) -> list[str]:
        """
        Get a list of all supported programming languages.

        Returns:
            List of supported language names
        """
        try:
            # Get unique languages from all mappings
            languages: set[str] = set()

            # Add languages from extension mapping
            languages.update(self.extension_to_language.values())

            # Add languages from special filenames
            languages.update(self.filename_to_language.values())

            # Add aliased languages
            languages.update(self.language_aliases.keys())

            supported_languages = sorted(languages)
            self.logger.debug(
                f"Retrieved {len(supported_languages)} supported languages"
            )
            return supported_languages

        except (TypeError, AttributeError, KeyError) as e:
            self.logger.error(f"Error getting supported languages: {e}")
            return []

    def get_language_stats(
        self, extension_stats: dict[str, Any]
    ) -> dict[str, dict[str, int]]:
        """
        Convert extension-based stats to language-based stats.

        Args:
            extension_stats: Dictionary with extension as key and stats as value

        Returns:
            Dictionary with language as key and aggregated stats as value
        """
        try:
            if not extension_stats:
                self.logger.warning("Empty extension stats provided")
                return {}

            language_stats = {}

            # Languages to exclude as they are mostly configuration files
            excluded_languages = {
                "JSON",  # package.json, composer.json, etc.
                "YAML",  # .yml, .yaml files
                "TOML",  # Cargo.toml, pyproject.toml, etc.
                "INI",  # .ini, .cfg, .conf files
                "Properties",  # .properties, .env files
                "Log",  # .log files
                "Image",  # Image files
                "Font",  # Font files
                "Archive",  # Archive files
                "Binary",  # Binary files
            }

            processed_extensions = 0
            excluded_count = 0

            for extension, stats in extension_stats.items():
                try:
                    language = self.map_extension_to_language(extension)

                    # Skip configuration and non-code files
                    if language in excluded_languages:
                        excluded_count += 1
                        continue

                    if language not in language_stats:
                        language_stats[language] = {"loc": 0, "commits": 0, "files": 0}

                    # Aggregate stats
                    language_stats[language]["loc"] += stats.get("loc", 0)
                    language_stats[language]["commits"] += stats.get("commits", 0)
                    language_stats[language]["files"] += stats.get("files", 0)

                    processed_extensions += 1

                except Exception as e:
                    self.logger.error(f"Error processing extension '{extension}': {e}")
                    continue

            self.logger.info(
                f"Processed {processed_extensions} extensions into {len(language_stats)} languages (excluded {excluded_count} config/non-code files)"
            )
            return language_stats

        except Exception as e:
            log_and_raise(
                LanguageMappingError,
                f"Error converting extension stats to language stats: {e}",
                error_code="STATS_CONVERSION_ERROR",
            )
            return {}


def get_language_mapper() -> LanguageMapper:
    """
    Factory function to create and return a LanguageMapper instance.

    Returns:
        LanguageMapper instance
    """
    try:
        mapper = LanguageMapper()
        get_logger(__name__).debug("Created new LanguageMapper instance")
        return mapper
    except Exception as e:
        get_logger(__name__).error(f"Error creating LanguageMapper: {e}")
        raise
