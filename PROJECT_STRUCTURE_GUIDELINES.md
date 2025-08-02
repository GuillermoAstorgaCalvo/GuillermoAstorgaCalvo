# Project Structure Guidelines

## GuillermoAstorgaCalvo GitHub Profile Repository

### 📋 **Overview**

This document defines the standard project structure and development guidelines that must be followed after the refactoring. These guidelines ensure consistency, maintainability, and scalability across the entire project.

**Purpose**: Establish clear standards for file organization, naming conventions, and architectural patterns that align with MCP documentation and enterprise best practices.

---

## 🏗️ **Folder Structure Standards**

### **Root Level Organization**

```
GuillermoAstorgaCalvo/
├── src/                    # Main source code (REQUIRED)
├── tests/                  # Test suite (REQUIRED)
├── docs/                   # Documentation (REQUIRED)
├── scripts/                # Entry point scripts (REQUIRED)
├── data/                   # Data storage (REQUIRED)
├── config/                 # Configuration files (REQUIRED)
├── assets/                 # Static assets (REQUIRED)
├── requirements/           # Dependency management (REQUIRED)
├── .github/                # GitHub Actions (REQUIRED)
├── README.md               # Project README (REQUIRED)
├── MCP_RULES.md            # MCP rules (REQUIRED)
├── PROMPT_GUIDELINES.md    # Prompt guidelines (REQUIRED)
├── pyproject.toml          # Project configuration (REQUIRED)
└── .gitignore              # Git ignore rules (REQUIRED)
```

### **Source Code Structure (`src/`)**

#### **Core Module (`src/core/`)**

```
src/core/
├── __init__.py             # Module initialization
├── exceptions.py           # Custom exceptions
├── constants.py            # Application constants
├── types.py                # Type definitions
└── base.py                 # Base classes and interfaces
```

**Purpose**: Foundation classes, exceptions, and types used throughout the application.

#### **Analyzers Module (`src/analyzers/`)**

```
src/analyzers/
├── __init__.py
├── repository/             # Repository analysis
│   ├── __init__.py
│   ├── api_analyzer.py
│   ├── dependency_analyzer.py
│   ├── enhanced_analyzer.py
│   └── stats_analyzer.py
├── language/               # Language analysis
│   ├── __init__.py
│   ├── mapper.py
│   ├── processor.py
│   └── detector.py
└── tech_stack/             # Technology stack analysis
    ├── __init__.py
    ├── skillicon_mapper.py
    ├── categorizer.py
    └── validator.py
```

**Purpose**: All analysis and data extraction logic.

#### **Generators Module (`src/generators/`)**

```
src/generators/
├── __init__.py
├── readme/                 # README generation
│   ├── __init__.py
│   ├── generator.py
│   ├── sections/
│   │   ├── __init__.py
│   │   ├── hero.py
│   │   ├── about.py
│   │   ├── stats.py
│   │   ├── projects.py
│   │   ├── tech_stack.py
│   │   ├── experience.py
│   │   └── contact.py
│   └── templates/
│       ├── __init__.py
│       └── base.py
├── reports/                # Report generation
│   ├── __init__.py
│   ├── markdown/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   ├── formatters.py
│   │   └── templates.py
│   ├── json/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── formatters.py
│   └── base.py
└── visualizations/         # Visualization generation
    ├── __init__.py
    ├── svg/
    │   ├── __init__.py
    │   ├── generator.py
    │   ├── charts.py
    │   ├── styles.py
    │   └── themes.py
    └── base.py
```

**Purpose**: All content generation logic (README, reports, visualizations).

#### **Processors Module (`src/processors/`)**

```
src/processors/
├── __init__.py
├── stats/                  # Statistics processing
│   ├── __init__.py
│   ├── aggregator.py
│   ├── processor.py
│   ├── git_fame.py
│   └── cloc.py
├── analytics/              # Analytics processing
│   ├── __init__.py
│   ├── manager.py
│   ├── reporter.py
│   ├── trends.py
│   └── insights.py
└── dependencies/           # Dependency processing
    ├── __init__.py
    ├── manager.py
    ├── scanner.py
    ├── updater.py
    └── validator.py
```

**Purpose**: Data processing and transformation logic.

#### **Managers Module (`src/managers/`)**

```
src/managers/
├── __init__.py
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── manager.py
│   ├── validator.py
│   └── loader.py
├── environment/            # Environment management
│   ├── __init__.py
│   ├── manager.py
│   ├── tokens.py
│   └── secrets.py
└── cache/                  # Cache management
    ├── __init__.py
    ├── manager.py
    ├── redis.py
    └── memory.py
```

**Purpose**: System management and coordination logic.

#### **Utils Module (`src/utils/`)**

```
src/utils/
├── __init__.py
├── logging/                # Logging utilities
│   ├── __init__.py
│   ├── setup.py
│   ├── formatters.py
│   └── filters.py
├── error_handling/         # Error handling utilities
│   ├── __init__.py
│   ├── decorators.py
│   ├── exceptions.py
│   └── handlers.py
├── validation/             # Validation utilities
│   ├── __init__.py
│   ├── validators.py
│   ├── schemas.py
│   └── sanitizers.py
└── helpers/                # General utilities
    ├── __init__.py
    ├── file_utils.py
    ├── text_utils.py
    ├── date_utils.py
    └── math_utils.py
```

**Purpose**: Reusable utilities and helper functions.

#### **Config Module (`src/config/`)**

```
src/config/
├── __init__.py
├── settings.py             # Application settings
├── paths.py                # Path configurations
└── defaults.py             # Default values
```

**Purpose**: Configuration and settings management.

#### **AI Module (`src/ai/`)**

```
src/ai/
├── __init__.py
├── description_generator.py    # AI description generation
├── prompt_manager.py          # Prompt management and optimization
├── cost_optimizer.py          # Cost control and rate limiting
├── fallback_handler.py        # Fallback description generation
├── cache_manager.py           # AI response caching
└── config/                    # AI configuration
    ├── __init__.py
    ├── settings.py            # AI-specific settings
    └── prompts.py             # Prompt templates
```

**Purpose**: AI-powered content generation and optimization.

---

## 📝 **File Naming Conventions**

### **Python Files**

- **snake_case**: All Python files use snake_case
- **Descriptive Names**: File names should clearly indicate their purpose
- **Module Prefix**: Use module prefix for clarity (e.g., `api_analyzer.py`)

### **Directory Names**

- **snake_case**: All directory names use snake_case
- **Plural for Collections**: Use plural for directories containing multiple files
- **Singular for Single Purpose**: Use singular for focused directories

### **Class Names**

- **PascalCase**: All class names use PascalCase
- **Descriptive**: Class names should clearly indicate their purpose
- **Suffix Convention**: Use appropriate suffixes (e.g., `Manager`, `Analyzer`, `Generator`)

### **Function Names**

- **snake_case**: All function names use snake_case
- **Verb-Noun**: Use verb-noun pattern for clarity
- **Descriptive**: Function names should clearly indicate their purpose

### **Variable Names**

- **snake_case**: All variable names use snake_case
- **Descriptive**: Variable names should be self-documenting
- **Constants**: Use UPPER_SNAKE_CASE for constants

---

## 🎯 **Code Organization Standards**

### **1. File Size Limits**

- **Maximum 500 lines** per file
- **Maximum 200 lines** per class
- **Maximum 50 lines** per function
- **Maximum 10 imports** per file

### **2. Import Organization**

```python
# Standard library imports (alphabetical)
import json
import os
from pathlib import Path
from typing import Any, Dict, List

# Third-party imports (alphabetical)
import requests
import yaml

# Local imports (alphabetical, grouped by module)
from src.core.exceptions import DataProcessingError
from src.core.types import ConfigDict
from src.utils.logging import get_logger
from src.utils.validation import validate_config
```

### **3. Class Structure**

```python
"""Module docstring following MCP documentation standards."""

from typing import Any, Dict

from src.core.exceptions import ComponentError
from src.utils.logging import get_logger


class ComponentName:
    """Component description following MCP documentation standards."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize component with configuration.

        Args:
            config: Configuration dictionary

        Raises:
            ComponentError: If configuration is invalid
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate component configuration."""
        # Implementation

    @with_error_context({"component": "component_name"})
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data with proper error handling.

        Args:
            data: Input data to process

        Returns:
            Processed data

        Raises:
            ComponentError: If processing fails
        """
        try:
            # Implementation
            return processed_data
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            raise ComponentError(f"Processing failed: {e}") from e
```

### **4. Function Structure**

```python
@with_error_context({"component": "component_name"})
def function_name(param1: str, param2: int) -> Dict[str, Any]:
    """Function description following MCP documentation standards.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        Description of return value

    Raises:
        ValueError: If parameters are invalid
        ComponentError: If processing fails
    """
    logger = get_logger(__name__)

    try:
        # Validate inputs
        if not param1:
            raise ValueError("param1 cannot be empty")

        # Implementation
        result = process_data(param1, param2)

        logger.info(f"Successfully processed {param1}")
        return result

    except Exception as e:
        logger.error(f"Error in function_name: {e}")
        raise
```

---

## 🔧 **Module Organization Standards**

### **1. Module Initialization (`__init__.py`)**

```python
"""Module description following MCP documentation standards."""

from .component_name import ComponentName
from .another_component import AnotherComponent

__all__ = [
    "ComponentName",
    "AnotherComponent",
]

__version__ = "1.0.0"
```

### **2. Module Dependencies**

- **Minimal Dependencies**: Each module should have minimal external dependencies
- **Clear Interfaces**: Define clear interfaces between modules
- **Dependency Injection**: Use dependency injection for flexibility
- **Circular Dependencies**: Avoid circular dependencies at all costs

### **3. Module Responsibilities**

- **Single Responsibility**: Each module has one clear purpose
- **High Cohesion**: Related functionality is grouped together
- **Low Coupling**: Modules depend on interfaces, not implementations
- **Clear Boundaries**: Module boundaries are well-defined

---

## 🧪 **Testing Standards**

### **Test Structure**

```
tests/
├── __init__.py
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_analyzers/
│   ├── test_generators/
│   ├── test_processors/
│   ├── test_managers/
│   └── test_utils/
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_workflows/
│   └── test_end_to_end/
├── fixtures/                # Test fixtures
│   ├── __init__.py
│   ├── sample_data/
│   └── mock_responses/
└── conftest.py              # pytest configuration
```

### **Test File Naming**

- **test\_\*.py**: All test files start with `test_`
- **test\_\*.py**: Test files mirror the source structure
- **conftest.py**: pytest configuration files

### **Test Coverage Requirements**

- **Minimum 90%** line coverage
- **Minimum 80%** branch coverage
- **100%** coverage for critical functions
- **Integration tests** for all workflows

---

## 📊 **Documentation Standards**

### **Documentation Structure**

```
docs/
├── api/                     # API documentation
├── guides/                  # User guides
├── development/             # Development docs
└── architecture/            # Architecture docs
```

### **Code Documentation**

- **Docstrings**: All public functions and classes must have docstrings
- **Type Hints**: All functions must have type hints
- **Examples**: Complex functions should include usage examples
- **MCP Compliance**: All documentation must follow MCP standards

---

## 🔒 **Security Standards**

### **Configuration Security**

- **No Secrets in Code**: Never commit secrets to version control
- **Environment Variables**: Use environment variables for sensitive data
- **Validation**: Validate all configuration inputs
- **Sanitization**: Sanitize all user inputs

### **Error Handling**

- **No Information Leakage**: Don't expose sensitive information in error messages
- **Proper Logging**: Log errors without exposing sensitive data
- **Graceful Degradation**: Handle errors gracefully
- **Recovery**: Implement error recovery mechanisms

---

## 🚀 **Performance Standards**

### **Performance Targets**

- **Execution Time**: <2 seconds for main workflows
- **Memory Usage**: <512MB for typical operations
- **API Calls**: Minimize external API calls
- **Caching**: Implement appropriate caching strategies

### **Optimization Guidelines**

- **Lazy Loading**: Load modules only when needed
- **Resource Management**: Properly manage file handles and connections
- **Parallel Processing**: Use parallel processing where appropriate
- **Memory Management**: Avoid memory leaks and excessive memory usage

---

## 📋 **Compliance Checklist**

### **Before Creating New Files**

- [ ] File follows naming conventions
- [ ] File is in the correct directory
- [ ] File has proper imports
- [ ] File has type hints
- [ ] File has docstrings
- [ ] File follows error handling patterns
- [ ] File is under 500 lines

### **Before Committing Code**

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] No sensitive data in code
- [ ] Proper error handling
- [ ] Documentation updated
- [ ] Performance acceptable

### **Before Merging Pull Requests**

- [ ] Code review completed
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Performance benchmarks pass
- [ ] Security review completed
- [ ] MCP compliance verified

---

## 🎯 **Enforcement**

### **Automated Checks**

- **Pre-commit Hooks**: Automated style and quality checks
- **CI/CD Pipeline**: Automated testing and validation
- **Code Quality Tools**: ruff, black, mypy integration
- **Security Scanning**: Automated security checks

### **Manual Reviews**

- **Code Reviews**: All changes require code review
- **Architecture Reviews**: Major changes require architecture review
- **Security Reviews**: Security-sensitive changes require security review
- **Performance Reviews**: Performance-critical changes require performance review

---

## 🏆 **Conclusion**

These guidelines ensure that the project maintains high quality standards, follows MCP documentation requirements, and remains scalable and maintainable as it grows.

**Key Principles:**

- **Consistency**: Follow established patterns and conventions
- **Quality**: Maintain high code quality and test coverage
- **Security**: Implement proper security practices
- **Performance**: Optimize for performance and resource usage
- **Documentation**: Maintain comprehensive documentation
- **Compliance**: Follow MCP documentation standards

**These guidelines are mandatory for all development work and must be followed to maintain project quality and consistency.**
