# MCP Rules Documentation

## GuillermoAstorgaCalvo GitHub Profile Repository

### 🎯 **Core Mission & Scope**

This repository is a **dynamic GitHub profile system** that automatically generates professional, data-driven content based on real repository analysis. The system combines automated data collection, intelligent processing, and human-like content generation.

---

## 📋 **Project Context Rules**

### **1. Repository Purpose**

- **Primary Goal**: Create an authentic, professional GitHub profile that showcases real development work
- **Data Source**: Private and public repositories with actual code contributions
- **Output**: Dynamic README.md with real-time statistics and technology stack
- **Audience**: Recruiters, fellow developers, potential collaborators

### **2. Key Principles**

- **Authenticity First**: All content must be based on real data, not fabricated
- **Professional Tone**: Human-written, engaging, but professional content
- **Data-Driven**: Statistics and metrics come from actual repository analysis
- **Privacy Respect**: Handle private repository data securely
- **Performance**: Optimize for GitHub Actions execution time and API limits

### **3. Technical Architecture**

- **Language**: Python 3.12+ (primary), with shell scripts for git operations
- **Automation**: GitHub Actions for scheduled updates
- **Data Storage**: JSON files (unified_stats.json, enhanced_tech_stack.json)
- **APIs**: GitHub API for repository analysis
- **Tools**: git-fame, cloc, dependency analyzers

---

## 🔧 **Development Rules**

### **1. Code Quality Standards**

```python
# Always follow these patterns:
- Type hints for all functions
- Comprehensive error handling with custom exceptions
- Logging with structured context
- Docstrings for all public functions
- Unit tests for critical functions
```

### **2. Error Handling Pattern**

```python
from error_handling import with_error_context, get_logger

@with_error_context({"component": "component_name"})
def function_name():
    logger = get_logger(__name__)
    try:
        # Implementation
        pass
    except SpecificError as e:
        logger.error(f"Specific error occurred: {e}")
        raise
```

### **3. Advanced Error Patterns**

- **Context-Aware Errors**: Rich error context with decorators
- **Error Recovery**: Graceful degradation and fallback strategies
- **Error Classification**: Categorized error types and handling
- **Error Reporting**: Structured error reporting and logging
- **Error Prevention**: Proactive error detection and validation

### **3. Configuration Management**

- **Primary Config**: `config.yml` (repositories, tokens, settings)
- **Environment Variables**: GitHub Secrets for tokens
- **Validation**: Always validate configuration before use
- **Fallbacks**: Provide sensible defaults for missing values

### **4. Advanced Configuration Management**

- **YAML Validation**: Comprehensive configuration file validation
- **Repository Validation**: Repository configuration verification and error detection
- **Token Validation**: Token type and permission validation
- **Duplicate Detection**: Repository name and configuration conflict resolution
- **Format Validation**: Data type and format verification
- **Error Reporting**: Detailed validation error messages with context
- **Configuration Testing**: Automated configuration validation in CI/CD

### **4. Data Processing Rules**

- **Source of Truth**: Repository analysis results
- **Aggregation**: Combine data from multiple sources intelligently
- **Validation**: Ensure data consistency and completeness
- **Caching**: Implement caching for API responses to respect rate limits

### **5. Language Processing System**

- **GitHub Linguist Compatibility**: Extension-to-language mapping with 100+ languages
- **Language Detection**: Automatic language identification from file extensions
- **Statistics Aggregation**: Language-specific metrics and visualization
- **Custom Mappings**: Support for custom language definitions
- **Visualization**: SVG generation for language statistics display
- **File Type Filtering**: Exclude non-code files (.txt, .json, etc.) from statistics

### **6. Performance Optimization**

- **File Size Limits**: 2MB maximum per file for processing
- **Execution Timeouts**: 120s for cloc, 60s for processing operations
- **Memory Management**: Optimize memory usage for large repositories
- **Parallel Processing**: Matrix strategy for multi-repository analysis
- **Resource Cleanup**: Automatic cleanup of temporary files and data
- **Caching Implementation**: Redis-based caching for API responses and analysis results

---

## 📊 **Content Generation Rules**

### **1. README Content Standards**

- **Tone**: Professional but approachable, like a real developer
- **Structure**: Hero → About → Stats → Projects → Tech Stack → Contact
- **Dynamic Elements**: Real statistics, actual project data
- **Static Elements**: Personal bio, contact information, professional story

### **2. Statistics Display**

- **Accuracy**: Only show real, calculated statistics
- **Context**: Provide meaningful context for numbers
- **Formatting**: Use human-readable formats (e.g., "40.8K lines" not "40800")
- **Updates**: Clearly indicate when data was last updated

### **3. Technology Stack Rules**

- **Source**: Actual dependencies from package.json, requirements.txt, etc.
- **Mapping**: Use skillicon.dev for consistent icon display
- **Categorization**: Frontend, Backend, Database, DevOps, AI/ML
- **Validation**: Only include technologies actually used in projects

### **4. Skillicon Integration**

- **Technology Mapping**: 900+ technology mappings to skillicon.dev
- **Automatic Fallback**: Graceful handling of unmapped technologies
- **Category Organization**: Structured technology categorization
- **Visual Consistency**: Standardized icon display across all sections
- **Technology Validation**: Cleanup and validation of technology names
- **Mapping Summary**: Detailed tracking of mapped vs unmapped technologies

### **5. Advanced Visualization System**

- **SVG Generation**: Modern bar charts with gradients and trends
- **Language Statistics**: Dynamic visualization with historical data
- **Custom Styling**: Professional gradients and color schemes
- **Responsive Design**: Adaptive charts for different screen sizes
- **Trend Analysis**: Historical data integration in visualizations
- **Chart Customization**: Configurable colors, dimensions, and styling

---

## 🔄 **Automation Rules**

### **1. GitHub Actions Workflows**

- **Scheduling**: Weekly for stats, daily for tech stack analysis
- **Concurrency**: Prevent overlapping executions
- **Timeout**: Respect GitHub Actions time limits
- **Error Handling**: Continue on non-critical failures

### **2. API Usage**

- **Rate Limiting**: Respect GitHub API rate limits
- **Token Management**: Use appropriate tokens for different repository types
- **Fallbacks**: Implement fallback strategies when API fails
- **Caching**: Cache responses to minimize API calls

### **3. Data Flow**

```
Repository Analysis → Statistics Processing → Aggregation → Content Generation → README Update
```

---

## 🛡️ **Security & Privacy Rules**

### **1. Token Management**

- **Storage**: GitHub Secrets only, never in code
- **Permissions**: Minimal required permissions for each token
- **Rotation**: Regular token rotation and validation
- **Scope**: Separate tokens for different repository types

### **2. Data Handling**

- **Private Repos**: Handle with extra care, respect confidentiality
- **Logging**: Never log sensitive data (tokens, private content)
- **Validation**: Validate all inputs to prevent injection attacks
- **Cleanup**: Remove temporary files and sensitive data

---

## 📈 **Analytics & Monitoring Rules**

### **1. Metrics to Track**

- **Performance**: Execution time, API call counts
- **Reliability**: Success/failure rates, error types
- **Data Quality**: Repository coverage, data completeness
- **User Impact**: README view counts, engagement metrics

### **2. Historical Data**

- **Retention**: Keep 90 days of analytics history
- **Trends**: Track growth patterns and velocity metrics
- **Backup**: Regular backups of critical data
- **Cleanup**: Automatic cleanup of old data

### **3. Advanced Analytics & Insights**

- **Historical Trend Analysis**: Velocity metrics and growth patterns
- **Language Usage Tracking**: Technology adoption and usage trends
- **Growth Pattern Prediction**: Forecasting based on historical data
- **Technology Maturity Assessment**: Skill level evaluation and recommendations
- **Productivity Insights**: Development velocity and efficiency metrics
- **Custom Analytics Dashboard**: Automated report generation with insights

### **4. Analytics Reporter**

- **Growth Trends Visualization**: Weekly, monthly, quarterly trend analysis
- **Velocity Metrics**: LOC/day, commits/day, files/day calculations
- **Language Usage Analysis**: Technology stack evolution tracking
- **Trend Visualization**: Simple chart generation for data presentation
- **Insights Generation**: Automated analysis and recommendations
- **Analytics Summary**: Comprehensive overview of development patterns

---

## 🎨 **UI/UX Rules**

### **1. Badge Standards**

- **Consistency**: Use consistent colors and styling
- **Accessibility**: Ensure proper contrast and alt text
- **Performance**: Optimize badge loading times
- **Fallbacks**: Handle badge service failures gracefully

### **2. Content Layout**

- **Responsive**: Ensure good display on different screen sizes
- **Readability**: Use clear typography and spacing
- **Visual Hierarchy**: Important information should stand out
- **Professional**: Maintain professional appearance

---

## 🔍 **Troubleshooting Rules**

### **1. Common Issues**

- **API Rate Limits**: Implement exponential backoff
- **Repository Access**: Validate permissions before analysis
- **Data Inconsistency**: Cross-validate data sources
- **Performance Issues**: Monitor execution times and optimize

### **2. Debugging Approach**

- **Logging**: Use structured logging with context
- **Validation**: Validate data at each processing step
- **Isolation**: Test components independently
- **Documentation**: Document known issues and solutions

---

## 📝 **Documentation Rules**

### **1. Code Documentation**

- **README**: Comprehensive setup and usage instructions
- **Inline Comments**: Explain complex logic and business rules
- **API Documentation**: Document all public functions
- **Examples**: Provide usage examples for key functions

### **2. Process Documentation**

- **Workflow**: Document GitHub Actions workflow logic
- **Configuration**: Explain all configuration options
- **Troubleshooting**: Document common issues and solutions
- **Updates**: Document changes and their impact

### **3. Advanced Reporting**

- **Multi-format Generation**: Markdown and JSON report formats
- **Historical Trend Visualization**: Growth pattern charts and analysis
- **Technology Maturity Assessment**: Skill level evaluation and recommendations
- **Productivity Insights**: Development velocity and efficiency analysis
- **Customizable Templates**: Flexible report structure and content
- **Automated Scheduling**: Regular report generation and distribution
- **Complexity Analysis**: Code complexity metrics and insights
- **Predictive Analytics**: Growth forecasting and technology adoption predictions

---

## 🤖 **AI Integration Rules**

### **1. AI Implementation Standards**

- **API Management**: OpenAI API key security and rotation
- **Cost Control**: Rate limiting and usage monitoring
- **Fallback Systems**: Graceful degradation when AI unavailable
- **Error Handling**: AI-specific error patterns and recovery
- **Input Validation**: Sanitize repository data before AI processing
- **Output Validation**: Validate AI-generated content for quality and safety

### **2. AI Performance Standards**

- **Response Time**: <60 seconds for AI generation
- **Cost Limits**: Maximum $20 per workflow run
- **Caching**: Implement AI response caching for cost optimization
- **Rate Limiting**: Respect API rate limits and implement backoff strategies
- **Memory Usage**: <256MB for AI operations
- **Concurrent Requests**: Maximum 3 concurrent AI requests

### **3. AI Security Standards**

- **API Key Protection**: Secure storage in GitHub Secrets only
- **Input Sanitization**: Clean repository data before AI processing
- **Output Validation**: Validate AI-generated content
- **Privacy Protection**: No sensitive data sent to AI APIs
- **Access Control**: Implement proper access controls for AI features
- **Audit Logging**: Log all AI operations for security monitoring

### **4. AI Error Handling Patterns**

```python
@with_error_context({"component": "ai_description_generator"})
def generate_ai_description(repo_data: dict) -> str:
    """Generate AI description with comprehensive error handling."""
    logger = get_logger(__name__)

    try:
        # Validate input data
        if not _validate_repo_data(repo_data):
            raise ValueError("Invalid repository data")

        # Generate AI description
        description = ai_client.generate_description(repo_data)

        # Validate output
        if not _validate_ai_output(description):
            raise AIOutputError("Invalid AI output")

        return description

    except AIAPIError as e:
        logger.error(f"AI API error: {e}")
        return _generate_fallback_description(repo_data)
    except AICostLimitError as e:
        logger.warning(f"AI cost limit reached: {e}")
        return _generate_fallback_description(repo_data)
    except Exception as e:
        logger.error(f"Unexpected AI error: {e}")
        return _generate_fallback_description(repo_data)
```

## 🚀 **Improvement Guidelines**

### **1. Feature Development**

- **User Value**: Focus on features that improve user experience
- **Data Quality**: Prioritize accuracy and reliability
- **Performance**: Consider execution time and resource usage
- **Maintainability**: Write clean, well-documented code
- **AI Integration**: Consider AI enhancement opportunities

### **2. Optimization Priorities**

1. **Reliability**: Ensure consistent, error-free operation
2. **Performance**: Optimize execution time and resource usage
3. **User Experience**: Improve content quality and presentation
4. **Maintainability**: Simplify code and improve documentation
5. **AI Efficiency**: Optimize AI usage and cost management

### **3. Testing Framework**

- **Unit Testing**: Comprehensive tests for critical functions
- **Integration Testing**: End-to-end workflow validation
- **Performance Benchmarking**: Execution time and resource usage tests
- **Security Testing**: Vulnerability scanning and token validation
- **Error Scenario Testing**: Edge case and failure mode validation
- **Continuous Testing**: Automated testing in CI/CD pipeline
- **AI Testing**: AI-specific testing and fallback validation
- **Cost Testing**: AI cost optimization and limit testing

### **4. Dependency Management System**

- **Security Scanning**: Automated vulnerability detection and reporting
- **Version Pinning**: Exact version management for critical packages
- **Update Analysis**: Major/minor update classification and recommendations
- **Missing Dependencies**: Code import analysis and dependency detection
- **Unused Dependencies**: Cleanup recommendations and removal suggestions
- **Dependency Reports**: Comprehensive analysis with actionable recommendations
- **Security Critical Packages**: Special handling for security-sensitive dependencies
- **AI Dependencies**: Special handling for AI-related packages and API clients

---

## 🎯 **Response Guidelines**

### **When Asked About:**

- **Code Changes**: Always consider impact on existing functionality
- **New Features**: Evaluate against core mission and user value
- **Bug Fixes**: Prioritize by impact and frequency
- **Optimization**: Focus on measurable improvements

### **Always Consider:**

- **Backward Compatibility**: Don't break existing functionality
- **Error Handling**: Implement proper error handling for new features
- **Testing**: Ensure new code is testable and tested
- **Documentation**: Update documentation for any changes

---

## 📋 **Quick Reference Commands**

### **Common Operations**

```bash
# Run all checks (Post-refactoring)
python scripts/run_all_checks.py

# Update tech stack (Post-refactoring)
python scripts/update_tech_stack.py

# Generate README (Post-refactoring)
python scripts/generate_readme.py

# Process repository stats (Post-refactoring)
python scripts/update_stats.py

# Aggregate all stats (Post-refactoring)
python scripts/update_stats.py

# Pre-refactoring commands (legacy)
# python scripts/enhanced_readme_generator.py
# python scripts/process_repo_stats.py
# python scripts/aggregate_stats.py
```

### **Configuration Files**

- `config.yml`: Main configuration
- `requirements.txt`: Python dependencies
- `pyproject.toml`: Project metadata
- `.github/workflows/`: GitHub Actions workflows

### **Output Files**

- `README.md`: Generated profile content
- `unified_stats.json`: Aggregated statistics
- `enhanced_tech_stack.json`: Technology stack analysis
- `assets/language_stats.svg`: Language statistics visualization

---

## 🔄 **Workflow Integration**

### **Default Workflow**

1. **Analysis**: Repository statistics and tech stack analysis
2. **Processing**: Data aggregation and validation
3. **Generation**: Content creation and formatting
4. **Deployment**: Automatic README updates via GitHub Actions

### **Manual Triggers**

- **Immediate Update**: `workflow_dispatch` for urgent changes
- **Scheduled Updates**: Daily/weekly automated runs
- **Event-Driven**: Updates on configuration changes

---

This MCP rules documentation serves as the foundation for all interactions and development decisions. It ensures consistency, quality, and alignment with the project's core mission.
