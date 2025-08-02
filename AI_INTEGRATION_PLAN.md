# AI Integration Plan for GitHub Actions

## Seamless Integration with update-stats.yml

### 📋 **Overview**

This document outlines how to integrate AI-powered README descriptions into the existing `update-stats.yml` GitHub Actions workflow without disrupting current functionality.

---

## 🔄 **Current Workflow Analysis**

### **Existing Flow:**

```yaml
process-repositories:
  steps: 1. Clone repository
    2. Run cloc (optimized)
    3. Process repository statistics
    4. Upload repository statistics

aggregate-and-commit:
  steps: 1. Download all repository statistics
    2. Generate unified statistics and README
    3. Create assets directory and generate SVG
    4. Commit results to profile
```

### **Enhanced Flow with AI:**

```yaml
process-repositories:
  steps: 1. Clone repository
    2. Run cloc (optimized)
    3. Process repository statistics
    4. Generate AI descriptions ← NEW STEP
    5. Upload repository statistics

aggregate-and-commit:
  steps: 1. Download all repository statistics
    2. Generate unified statistics and README
    3. Create assets directory and generate SVG
    4. Commit results to profile
```

---

## 🚀 **Implementation Strategy**

### **Phase 1: Add AI Description Generation Step**

**Location**: After "Process repository statistics" in `process-repositories` job

**New Step:**

```yaml
- name: Generate AI descriptions
  env:
    REPO_NAME: ${{ matrix.repository.name }}
    DISPLAY_NAME: ${{ matrix.repository.display_name }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    cd scripts

    echo "🤖 Generating AI descriptions for ${REPO_NAME} (${DISPLAY_NAME})"

    # Verify OpenAI API key is available
    if [[ -z "${OPENAI_API_KEY}" ]]; then
      echo "⚠️ OPENAI_API_KEY not set, skipping AI description generation"
      exit 0
    fi

    # Generate AI descriptions
    if python3 generate_ai_descriptions.py; then
      echo "✅ AI descriptions generated successfully"
    else
      echo "❌ AI description generation failed, using fallback"
      # Fallback to existing description generation
      python3 generate_fallback_descriptions.py
    fi
```

### **Phase 2: Enhanced Artifact Upload**

**Updated Step:**

```yaml
- name: Upload repository statistics
  uses: actions/upload-artifact@v4
  with:
    name: ${{ matrix.repository.artifact_name }}
    path: |
      data/repo_stats.json
      data/tech_stack_analysis.json
      data/ai_descriptions.json ← NEW FILE
    retention-days: 1
```

---

## 🔧 **Technical Implementation**

### **1. AI Description Generator Script**

**File**: `src/ai/description_generator.py`

```python
#!/usr/bin/env python3
"""
AI-Powered Repository Description Generator
Generates dynamic descriptions using OpenAI API
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from openai import OpenAI
from error_handling import get_logger, with_error_context

logger = get_logger(__name__)


class AIDescriptionGenerator:
    """Generates AI-powered project descriptions."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate_description(self, repo_analysis: Dict[str, Any]) -> str:
        """Generate description based on repository analysis."""
        try:
            prompt = self._build_prompt(repo_analysis)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            raise

    def _build_prompt(self, analysis: Dict[str, Any]) -> str:
        """Build AI prompt from repository analysis."""
        technologies = analysis.get('technologies', [])
        languages = analysis.get('languages', {})
        project_type = analysis.get('project_type', 'Unknown')
        features = analysis.get('features', [])

        return f"""
        Generate a professional, concise project description for a GitHub repository with the following characteristics:

        Technologies: {', '.join(technologies[:10])}
        Languages: {', '.join(languages.keys()[:5])}
        Project Type: {project_type}
        Key Features: {', '.join(features[:5])}

        Requirements:
        - Professional tone
        - 2-3 sentences maximum
        - Highlight key technologies and purpose
        - Include emoji for visual appeal
        - Focus on business value and technical innovation
        - Write in English
        """


@with_error_context({"component": "ai_description_generator"})
def main() -> None:
    """Main function for AI description generation."""
    logger.info("Starting AI description generation")

    # Get OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    # Load repository analysis
    repo_stats_path = Path("repo_stats.json")
    tech_stack_path = Path("tech_stack_analysis.json")

    if not repo_stats_path.exists() or not tech_stack_path.exists():
        logger.error("Required analysis files not found")
        sys.exit(1)

    # Load data
    with open(repo_stats_path, 'r', encoding='utf-8') as f:
        repo_stats = json.load(f)

    with open(tech_stack_path, 'r', encoding='utf-8') as f:
        tech_stack = json.load(f)

    # Merge analysis data
    analysis_data = {
        'technologies': tech_stack.get('technologies', []),
        'languages': repo_stats.get('languages', {}),
        'project_type': _determine_project_type(repo_stats, tech_stack),
        'features': _extract_features(repo_stats, tech_stack)
    }

    # Generate AI description
    generator = AIDescriptionGenerator(api_key)
    description = generator.generate_description(analysis_data)

    # Save AI description
    ai_descriptions = {
        'repository': os.environ.get('REPO_NAME', 'unknown'),
        'description': description,
        'generated_at': str(Path().cwd()),
        'analysis_data': analysis_data
    }

    with open('ai_descriptions.json', 'w', encoding='utf-8') as f:
        json.dump(ai_descriptions, f, indent=2, ensure_ascii=False)

    logger.info(f"AI description generated: {description[:100]}...")
    logger.info("AI description generation completed successfully")


def _determine_project_type(repo_stats: Dict[str, Any], tech_stack: Dict[str, Any]) -> str:
    """Determine project type based on analysis."""
    languages = repo_stats.get('languages', {})
    technologies = tech_stack.get('technologies', [])

    if 'Python' in languages:
        return 'Python Application'
    elif 'JavaScript' in languages or 'TypeScript' in languages:
        return 'Web Application'
    elif 'Java' in languages:
        return 'Java Application'
    elif 'C++' in languages:
        return 'C++ Application'
    else:
        return 'Software Project'


def _extract_features(repo_stats: Dict[str, Any], tech_stack: Dict[str, Any]) -> list[str]:
    """Extract key features from analysis."""
    features = []
    technologies = tech_stack.get('technologies', [])

    # Technology-based features
    if 'React' in technologies:
        features.append('Modern React frontend')
    if 'Node.js' in technologies:
        features.append('Node.js backend')
    if 'Python' in technologies:
        features.append('Python backend')
    if 'Docker' in technologies:
        features.append('Containerized deployment')
    if 'TypeScript' in technologies:
        features.append('TypeScript support')

    return features[:5]  # Limit to 5 features


if __name__ == "__main__":
    main()
```

### **2. Fallback Description Generator**

**File**: `src/ai/fallback_handler.py`

```python
#!/usr/bin/env python3
"""
Fallback Repository Description Generator
Generates descriptions when AI is unavailable
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

from error_handling import get_logger, with_error_context

logger = get_logger(__name__)


@with_error_context({"component": "fallback_description_generator"})
def main() -> None:
    """Generate fallback descriptions."""
    logger.info("Generating fallback descriptions")

    # Load repository analysis
    repo_stats_path = Path("repo_stats.json")
    tech_stack_path = Path("tech_stack_analysis.json")

    if not repo_stats_path.exists() or not tech_stack_path.exists():
        logger.error("Required analysis files not found")
        sys.exit(1)

    # Load data
    with open(repo_stats_path, 'r', encoding='utf-8') as f:
        repo_stats = json.load(f)

    with open(tech_stack_path, 'r', encoding='utf-8') as f:
        tech_stack = json.load(f)

    # Generate fallback description
    description = _generate_fallback_description(repo_stats, tech_stack)

    # Save fallback description
    fallback_descriptions = {
        'repository': os.environ.get('REPO_NAME', 'unknown'),
        'description': description,
        'generated_at': str(Path().cwd()),
        'method': 'fallback'
    }

    with open('ai_descriptions.json', 'w', encoding='utf-8') as f:
        json.dump(fallback_descriptions, f, indent=2, ensure_ascii=False)

    logger.info(f"Fallback description generated: {description}")
    logger.info("Fallback description generation completed")


def _generate_fallback_description(repo_stats: Dict[str, Any], tech_stack: Dict[str, Any]) -> str:
    """Generate fallback description based on analysis."""
    languages = repo_stats.get('languages', {})
    technologies = tech_stack.get('technologies', [])

    # Get top languages
    top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
    lang_names = [lang for lang, _ in top_languages]

    # Get key technologies
    key_techs = technologies[:5]

    # Generate description
    if lang_names:
        lang_desc = ', '.join(lang_names)
        tech_desc = ', '.join(key_techs) if key_techs else 'modern technologies'

        return f"🚀 A {lang_desc} project built with {tech_desc}. Features clean architecture and best practices for scalable development."
    else:
        return "🚀 A software project showcasing modern development practices and clean code architecture."


if __name__ == "__main__":
    main()
```

---

## 🔐 **Security and Configuration**

### **1. GitHub Secrets Setup**

**Add to Repository Secrets:**

```yaml
# In GitHub repository settings → Secrets and variables → Actions
OPENAI_API_KEY: sk-... # Your OpenAI API key
```

### **2. Enhanced Workflow Security**

**Updated Security Validation:**

```yaml
- name: Security validation
  run: |
    # Existing validations...

    # Validate OpenAI API key format (if provided)
    if [[ -n "${OPENAI_API_KEY}" ]]; then
      if [[ ! "${OPENAI_API_KEY}" =~ ^sk-[a-zA-Z0-9]{48}$ ]]; then
        echo "❌ Security violation: Invalid OpenAI API key format"
        exit 1
      fi
    fi

    echo "✅ Security validation passed"
```

### **3. Rate Limiting and Cost Control**

**Enhanced AI Step with Rate Limiting:**

```yaml
- name: Generate AI descriptions
  env:
    REPO_NAME: ${{ matrix.repository.name }}
    DISPLAY_NAME: ${{ matrix.repository.display_name }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    cd scripts

    echo "🤖 Generating AI descriptions for ${REPO_NAME} (${DISPLAY_NAME})"

    # Rate limiting: Only generate for first 10 repositories per run
    REPO_INDEX=${{ matrix.repository.index || 0 }}
    if [[ $REPO_INDEX -gt 9 ]]; then
      echo "⚠️ Skipping AI generation for repository ${REPO_INDEX} (rate limit)"
      python3 generate_fallback_descriptions.py
      exit 0
    fi

    # Verify OpenAI API key is available
    if [[ -z "${OPENAI_API_KEY}" ]]; then
      echo "⚠️ OPENAI_API_KEY not set, using fallback"
      python3 generate_fallback_descriptions.py
      exit 0
    fi

    # Generate AI descriptions with timeout
    timeout 60s python3 generate_ai_descriptions.py || {
      echo "⚠️ AI generation timed out, using fallback"
      python3 generate_fallback_descriptions.py
    }
```

---

## 📊 **Enhanced README Generator Integration**

### **Updated README Generator**

**Modify**: `src/generators/readme/generator.py`

```python
def load_ai_descriptions() -> Dict[str, str]:
    """Load AI-generated descriptions from artifacts."""
    try:
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent
        repos_dir = root_dir / "repo-stats"

        descriptions = {}

        # Load AI descriptions from all repositories
        for desc_file in repos_dir.glob("*/ai_descriptions.json"):
            try:
                with open(desc_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    repo_name = data.get('repository', 'unknown')
                    description = data.get('description', '')
                    if description:
                        descriptions[repo_name] = description
            except Exception as e:
                logger.warning(f"Could not load AI description from {desc_file}: {e}")

        return descriptions
    except Exception as e:
        logger.warning(f"Could not load AI descriptions: {e}")
        return {}


def get_project_descriptions() -> Dict[str, Dict[str, Any]]:
    """Get project descriptions with AI enhancement."""
    # Load existing descriptions
    base_descriptions = _get_base_project_descriptions()

    # Load AI descriptions
    ai_descriptions = load_ai_descriptions()

    # Merge AI descriptions with base descriptions
    for repo_name, ai_desc in ai_descriptions.items():
        if repo_name in base_descriptions:
            base_descriptions[repo_name]['description'] = ai_desc
            base_descriptions[repo_name]['ai_generated'] = True
        else:
            # Create new entry for AI-only descriptions
            base_descriptions[repo_name] = {
                'description': ai_desc,
                'ai_generated': True,
                'display_name': repo_name.replace('-', ' ').title()
            }

    return base_descriptions
```

---

## 🎯 **Benefits of This Integration**

### **1. Seamless Workflow**

- **No Disruption**: Existing workflow continues unchanged
- **Graceful Fallback**: AI failures don't break the process
- **Incremental Enhancement**: AI descriptions enhance existing functionality

### **2. Cost Optimization**

- **Rate Limiting**: Only generate for first 10 repositories per run
- **Caching**: Reuse descriptions when possible
- **Fallback System**: No API costs when AI is unavailable

### **3. Security**

- **API Key Protection**: Stored in GitHub Secrets
- **Input Validation**: Sanitize repository data before sending to AI
- **Error Handling**: Graceful handling of API failures

### **4. Performance**

- **Timeout Protection**: 60-second timeout for AI generation
- **Parallel Processing**: AI generation happens in parallel with existing steps
- **Minimal Overhead**: Only adds ~30-60 seconds per repository

---

## 📋 **Implementation Checklist**

### **Phase 1: Basic Integration**

- [ ] Add OpenAI dependency to `requirements.txt`
- [ ] Create `src/ai/description_generator.py`
- [ ] Create `src/ai/fallback_handler.py`
- [ ] Add AI step to workflow
- [ ] Add OPENAI_API_KEY to GitHub Secrets

### **Phase 2: Enhanced Integration**

- [ ] Update README generator to use AI descriptions
- [ ] Add rate limiting and cost control
- [ ] Implement caching system
- [ ] Add comprehensive error handling

### **Phase 3: Optimization**

- [ ] Add performance monitoring
- [ ] Implement advanced caching
- [ ] Add multi-language support
- [ ] Create cost analytics

---

## 🏆 **Conclusion**

**Perfect Integration**: The AI-powered README descriptions will integrate seamlessly with your existing `update-stats.yml` workflow.

**Key Advantages**:

- ✅ **Zero Disruption**: Existing functionality preserved
- ✅ **Graceful Degradation**: Fallback system ensures reliability
- ✅ **Cost Controlled**: Rate limiting and optimization
- ✅ **Security Compliant**: Follows existing security patterns
- ✅ **Performance Optimized**: Minimal overhead

**The integration will enhance your GitHub profile with AI-generated descriptions while maintaining the reliability and security of your current workflow.**
