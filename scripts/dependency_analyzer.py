#!/usr/bin/env python3
"""
Dependency Analyzer
Analyzes package.json and requirements.txt files to extract actual technologies and frameworks used.
"""

import json
import os
from pathlib import Path
from typing import Any

from error_handling import (
    DependencyAnalysisError,
    ErrorCodes,
    get_logger,
    log_and_raise,
    with_error_context,
)

logger = get_logger(__name__)


class DependencyAnalyzer:
    """Analyzes dependencies from package.json and requirements.txt files."""

    def __init__(self) -> None:
        """Initialize the dependency analyzer."""

        # Technology mappings
        self.frontend_tech = {
            "react": "React",
            "react-dom": "React",
            "@types/react": "React",
            "vue": "Vue.js",
            "@vue/cli": "Vue.js",
            "vue-router": "Vue.js",
            "angular": "Angular",
            "@angular/core": "Angular",
            "@angular/common": "Angular",
            "next": "Next.js",
            "next.js": "Next.js",
            "@next/font": "Next.js",
            "tailwindcss": "TailwindCSS",
            "tailwind": "TailwindCSS",
            "@tailwindcss/forms": "TailwindCSS",
            "bootstrap": "Bootstrap",
            "@bootstrap": "Bootstrap",
            "framer-motion": "Framer Motion",
            "framer": "Framer Motion",
            "styled-components": "Styled Components",
            "styled": "Styled Components",
            "sass": "Sass",
            "scss": "Sass",
            "node-sass": "Sass",
            "less": "Less",
            "typescript": "TypeScript",
            "@types/node": "TypeScript",
            # "@types/react": "TypeScript",  # Duplicate key removed
            "javascript": "JavaScript",
            "js": "JavaScript",
            "axios": "Axios",
            "fetch": "Fetch API",
            "lodash": "Lodash",
            "underscore": "Underscore",
            "moment": "Moment.js",
            "date-fns": "date-fns",
            "chart.js": "Chart.js",
            "d3": "D3.js",
            "recharts": "Recharts",
            # Radix UI components
            "@radix-ui/react-accordion": "Radix UI",
            "@radix-ui/react-alert-dialog": "Radix UI",
            "@radix-ui/react-aspect-ratio": "Radix UI",
            "@radix-ui/react-avatar": "Radix UI",
            "@radix-ui/react-checkbox": "Radix UI",
            "@radix-ui/react-collapsible": "Radix UI",
            "@radix-ui/react-context-menu": "Radix UI",
            "@radix-ui/react-dialog": "Radix UI",
            "@radix-ui/react-dropdown-menu": "Radix UI",
            "@radix-ui/react-hover-card": "Radix UI",
            "@radix-ui/react-label": "Radix UI",
            "@radix-ui/react-menubar": "Radix UI",
            "@radix-ui/react-navigation-menu": "Radix UI",
            "@radix-ui/react-popover": "Radix UI",
            "@radix-ui/react-progress": "Radix UI",
            "@radix-ui/react-radio-group": "Radix UI",
            "@radix-ui/react-scroll-area": "Radix UI",
            "@radix-ui/react-select": "Radix UI",
            "@radix-ui/react-separator": "Radix UI",
            "@radix-ui/react-slider": "Radix UI",
            "@radix-ui/react-slot": "Radix UI",
            "@radix-ui/react-switch": "Radix UI",
            "@radix-ui/react-tabs": "Radix UI",
            "@radix-ui/react-toast": "Radix UI",
            "@radix-ui/react-toggle": "Radix UI",
            "@radix-ui/react-toggle-group": "Radix UI",
            "@radix-ui/react-tooltip": "Radix UI",
            # Other frontend libraries
            "@tanstack/react-query": "TanStack Query",
            "@hookform/resolvers": "React Hook Form",
            "react-hook-form": "React Hook Form",
            "react-router-dom": "React Router",
            "react-day-picker": "React Day Picker",
            "react-resizable-panels": "React Resizable Panels",
            "react-icons": "React Icons",
            "react-hot-toast": "React Hot Toast",
            "sonner": "Sonner",
            "lucide-react": "Lucide React",
            "class-variance-authority": "CVA",
            "clsx": "clsx",
            "tailwind-merge": "Tailwind Merge",
            "tailwindcss-animate": "Tailwind Animate",
            "cmdk": "cmdk",
            "embla-carousel-react": "Embla Carousel",
            "input-otp": "Input OTP",
            "next-themes": "Next Themes",
            "vaul": "Vaul",
            "zod": "Zod",
            # "framer-motion": "Framer Motion",  # Duplicate key removed
            "vite": "Vite",
            "@vitejs/plugin-react-swc": "Vite",
            # Maps and visualization
            "@react-google-maps/api": "Google Maps",
            "@googlemaps/js-api-loader": "Google Maps",
            "@googlemaps/markerclusterer": "Google Maps",
            "@turf/turf": "Turf.js",
            "proj4": "Proj4js",
            "marzipano": "Marzipano",
            "konva": "Konva",
            "react-konva": "React Konva",
            "@xyflow/react": "React Flow",
            # Authentication and backend
            "@supabase/auth-helpers-react": "Supabase",
            "@supabase/supabase-js": "Supabase",
            "supabase": "Supabase",
            "@stripe/stripe-js": "Stripe",
            "bcrypt": "bcrypt",
            "bcryptjs": "bcryptjs",
            # File handling and utilities
            "html2canvas": "html2canvas",
            "jspdf": "jsPDF",
            "file-saver": "File Saver",
            "dompurify": "DOMPurify",
            "uuid": "UUID",
            "crypto": "Crypto",
            "dotenv": "dotenv",
            # Development tools
            "eslint": "ESLint",
            # "typescript": "TypeScript",  # Duplicate key removed
            "autoprefixer": "Autoprefixer",
            "postcss": "PostCSS",
            "esbuild": "esbuild",
            "playwright": "Playwright",
            "@playwright/test": "Playwright",
            "eslint-config-prettier": "ESLint Prettier",
            "eslint-plugin-security": "ESLint Security",
            "eslint-plugin-sonarjs": "ESLint SonarJS",
        }

        self.backend_tech = {
            "express": "Express.js",
            "express.js": "Express.js",
            "@types/express": "Express.js",
            "fastapi": "FastAPI",
            "fast-api": "FastAPI",
            "uvicorn": "FastAPI",
            "django": "Django",
            "djangorestframework": "Django REST",
            "django-cors-headers": "Django",
            "flask": "Flask",
            "flask-cors": "Flask",
            "node": "Node.js",
            "nodejs": "Node.js",
            "python": "Python",
            "java": "Java",
            "spring-boot": "Spring Boot",
            "spring": "Spring",
            "php": "PHP",
            "laravel": "Laravel",
            "symfony": "Symfony",
            "ruby": "Ruby",
            "rails": "Ruby on Rails",
            "go": "Go",
            "golang": "Go",
            "rust": "Rust",
            "cors": "CORS",
            "helmet": "Helmet",
            "bcrypt": "bcrypt",
            "jsonwebtoken": "JWT",
            "passport": "Passport",
            # Python specific
            "starlette": "Starlette",
            "pydantic": "Pydantic",
            "pydantic-settings": "Pydantic Settings",
            "pydantic-core": "Pydantic Core",
            "python-jose": "PyJWT",
            "passlib": "Passlib",
            "python-multipart": "Python Multipart",
            "pyjwt": "PyJWT",
            "email-validator": "Email Validator",
            "python-dotenv": "Python dotenv",
            "python-magic": "Python Magic",
            "aiofiles": "aiofiles",
            "tenacity": "Tenacity",
            "requests": "Requests",
            "httpx": "httpx",
            # Additional backend technologies
            "compression": "Compression",
            "express-rate-limit": "Rate Limiting",
            "fast-xml-parser": "XML Parser",
            "ioredis": "Redis",
            "lru-cache": "LRU Cache",
            "node-cache": "Node Cache",
            "node-cron": "Cron Jobs",
            "proj4": "Proj4",
            "prom-client": "Prometheus",
            "undici": "Undici",
            "winston": "Winston",
            "xml2js": "XML2JS",
            "beautifulsoup4": "BeautifulSoup",
            "apscheduler": "APScheduler",
            "joblib": "Joblib",
            "tabulate": "Tabulate",
            # Testing and development
            "pytest": "pytest",
            "pytest-asyncio": "pytest-asyncio",
            "pytest-cov": "pytest-cov",
            "ruff": "Ruff",
            "black": "Black",
            "mypy": "MyPy",
            "setuptools": "setuptools",
            "artillery": "Artillery",
            "ts-jest": "ts-jest",
            "ts-node-dev": "ts-node-dev",
            "tsc-alias": "tsc-alias",
            "tsconfig-paths": "tsconfig-paths",
        }

        self.database_tech = {
            "postgresql": "PostgreSQL",
            "pg": "PostgreSQL",
            "postgres": "PostgreSQL",
            "postgresql-client": "PostgreSQL",
            "mysql": "MySQL",
            "mysql2": "MySQL",
            "mysql-connector": "MySQL",
            "mongodb": "MongoDB",
            "mongoose": "MongoDB",
            "mongodb-driver": "MongoDB",
            "redis": "Redis",
            "ioredis": "Redis",
            "sqlite": "SQLite",
            "sqlite3": "SQLite",
            "prisma": "Prisma",
            "@prisma/client": "Prisma",
            "sequelize": "Sequelize",
            "sequelize-cli": "Sequelize",
            "sqlalchemy": "SQLAlchemy",
            # "alembic": "SQLAlchemy",  # Duplicate key removed
            "typeorm": "TypeORM",
            "typeorm-reflect-metadata": "TypeORM",
            # Python database
            "asyncpg": "asyncpg",
            "psycopg2-binary": "psycopg2",
            "alembic": "Alembic",
        }

        self.devops_tech = {
            "docker": "Docker",
            "docker-compose": "Docker Compose",
            "@types/docker": "Docker",
            "kubernetes": "Kubernetes",
            "k8s": "Kubernetes",
            "aws": "AWS",
            "aws-sdk": "AWS SDK",
            "@aws-sdk/client-s3": "AWS",
            "@aws-sdk/client-ses": "AWS SES",
            "azure": "Azure",
            "@azure/identity": "Azure",
            "@azure/storage-blob": "Azure",
            "gcp": "Google Cloud",
            "google-cloud": "Google Cloud",
            "@google-cloud/storage": "Google Cloud",
            "terraform": "Terraform",
            "jenkins": "Jenkins",
            "github-actions": "GitHub Actions",
            "gitlab-ci": "GitLab CI",
            "nginx": "Nginx",
            "apache": "Apache",
            "vite": "Vite",
            "esbuild": "esbuild",
            "rollup": "Rollup",
            "webpack": "Webpack",
        }

        self.ai_ml_tech = {
            "openai": "OpenAI",
            "openai-api": "OpenAI",
            "@openai/api": "OpenAI",
            "tensorflow": "TensorFlow",
            "tf": "TensorFlow",
            "tensorflow-gpu": "TensorFlow",
            "pytorch": "PyTorch",
            "torch": "PyTorch",
            "torchvision": "PyTorch",
            "scikit-learn": "Scikit-learn",
            "sklearn": "Scikit-learn",
            "pandas": "Pandas",
            "numpy": "NumPy",
            "matplotlib": "Matplotlib",
            "seaborn": "Seaborn",
            "transformers": "Transformers",
            "huggingface": "Hugging Face",
            "langchain": "LangChain",
            "langchain-community": "LangChain",
            "anthropic": "Anthropic",
            "claude": "Anthropic",
            "spacy": "spaCy",
            "nltk": "NLTK",
            # Image processing and OCR
            "pytesseract": "Tesseract OCR",
            "pillow": "Pillow",
            "opencv-python": "OpenCV",
            "replicate": "Replicate",
        }

    @with_error_context({"component": "dependency_analyzer"})
    def analyze_repository_dependencies(self, repo_path: Path) -> dict[str, set[str]]:
        """Analyze dependencies from a repository."""
        categories: dict[str, set[str]] = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }
        try:
            # Look for package.json files (Node.js/JavaScript)
            package_json_files = list(repo_path.rglob("package.json"))
            for package_file in package_json_files:
                try:
                    with open(package_file, encoding="utf-8") as f:
                        data = json.load(f)
                    # Analyze dependencies
                    deps = data.get("dependencies", {})
                    dev_deps = data.get("devDependencies", {})
                    all_deps = {**deps, **dev_deps}
                    for dep_name in all_deps.keys():
                        dep_lower = dep_name.lower()
                        # Categorize the dependency
                        if dep_lower in self.frontend_tech:
                            categories["frontend"].add(self.frontend_tech[dep_lower])
                        elif dep_lower in self.backend_tech:
                            categories["backend"].add(self.backend_tech[dep_lower])
                        elif dep_lower in self.database_tech:
                            categories["database"].add(self.database_tech[dep_lower])
                        elif dep_lower in self.devops_tech:
                            categories["devops"].add(self.devops_tech[dep_lower])
                        elif dep_lower in self.ai_ml_tech:
                            categories["ai_ml"].add(self.ai_ml_tech[dep_lower])
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    logger.warning(
                        f"Failed to parse {package_file}: {e}",
                        extra={"file": str(package_file)},
                    )
                except Exception as e:
                    log_and_raise(
                        DependencyAnalysisError(
                            f"Unexpected error analyzing {package_file}: {e}",
                            error_code=ErrorCodes.DEPENDENCY_ANALYSIS_FAILED,
                            context={"file": str(package_file)},
                        ),
                        logger=logger,
                    )

            # Look for Python dependency files
            python_files = (
                list(repo_path.rglob("requirements.txt"))
                + list(repo_path.rglob("pyproject.toml"))
                + list(repo_path.rglob("setup.py"))
            )
            for py_file in python_files:
                try:
                    if py_file.name == "requirements.txt":
                        with open(py_file, encoding="utf-8") as f:
                            lines = f.readlines()
                        for line in lines:
                            pkg = (
                                line.strip()
                                .split("==")[0]
                                .split(">=")[0]
                                .split("<=")[0]
                                .lower()
                            )
                            if pkg in self.backend_tech:
                                categories["backend"].add(self.backend_tech[pkg])
                            elif pkg in self.database_tech:
                                categories["database"].add(self.database_tech[pkg])
                            elif pkg in self.devops_tech:
                                categories["devops"].add(self.devops_tech[pkg])
                            elif pkg in self.ai_ml_tech:
                                categories["ai_ml"].add(self.ai_ml_tech[pkg])
                    elif py_file.name == "pyproject.toml":
                        # Add Python as backend technology when pyproject.toml is found
                        categories["backend"].add("Python")
                    elif py_file.name == "setup.py":
                        # Add Python as backend technology when setup.py is found
                        categories["backend"].add("Python")
                except FileNotFoundError:
                    logger.warning(
                        f"Python file not found: {py_file}",
                        extra={"file": str(py_file)},
                    )
                except Exception as e:
                    log_and_raise(
                        DependencyAnalysisError(
                            f"Unexpected error analyzing {py_file}: {e}",
                            error_code=ErrorCodes.DEPENDENCY_ANALYSIS_FAILED,
                            context={"file": str(py_file)},
                        ),
                        logger=logger,
                    )

            # Look for Docker files
            docker_files = (
                list(repo_path.rglob("Dockerfile"))
                + list(repo_path.rglob("docker-compose.yml"))
                + list(repo_path.rglob("docker-compose.yaml"))
            )
            if docker_files:
                categories["devops"].add("Docker")

            # Look for Kubernetes files
            k8s_files = list(repo_path.rglob("*.yaml")) + list(repo_path.rglob("*.yml"))
            for k8s_file in k8s_files:
                try:
                    with open(k8s_file, encoding="utf-8") as f:
                        content = f.read().lower()
                        if "apiVersion:" in content and ("kind:" in content):
                            categories["devops"].add("Kubernetes")
                            break
                except Exception:
                    continue

            # Look for Terraform files
            terraform_files = list(repo_path.rglob("*.tf")) + list(
                repo_path.rglob("*.tfvars")
            )
            if terraform_files:
                categories["devops"].add("Terraform")

            # Look for GitHub Actions
            github_actions_dir = repo_path / ".github" / "workflows"
            if github_actions_dir.exists():
                categories["devops"].add("GitHub Actions")

            # Look for GitLab CI
            gitlab_ci_files = list(repo_path.rglob(".gitlab-ci.yml"))
            if gitlab_ci_files:
                categories["devops"].add("GitLab")

            # Look for Nginx configuration
            nginx_files = list(repo_path.rglob("nginx.conf")) + list(
                repo_path.rglob("*.nginx")
            )
            if nginx_files:
                categories["devops"].add("Nginx")

            # Look for Redis configuration
            redis_files = list(repo_path.rglob("redis.conf")) + list(
                repo_path.rglob("*.redis")
            )
            if redis_files:
                categories["database"].add("Redis")

            # Look for PostgreSQL configuration
            postgres_files = list(repo_path.rglob("*.sql")) + list(
                repo_path.rglob("postgresql.conf")
            )
            if postgres_files:
                categories["database"].add("PostgreSQL")

                # Look for MongoDB configuration
            mongo_files = list(repo_path.rglob("mongod.conf")) + list(
                repo_path.rglob("*.mongo")
            )
            if mongo_files:
                categories["database"].add("MongoDB")

            # Look for additional technology indicators
            # React/Next.js
            react_files = list(repo_path.rglob("*.jsx")) + list(
                repo_path.rglob("*.tsx")
            )
            if react_files:
                categories["frontend"].add("React")

            # Vue.js
            vue_files = list(repo_path.rglob("*.vue"))
            if vue_files:
                categories["frontend"].add("Vue")

            # Angular
            angular_files = list(repo_path.rglob("angular.json")) + list(
                repo_path.rglob("*.component.ts")
            )
            if angular_files:
                categories["frontend"].add("Angular")

            # Svelte
            svelte_files = list(repo_path.rglob("*.svelte"))
            if svelte_files:
                categories["frontend"].add("Svelte")

            # Astro
            astro_files = list(repo_path.rglob("astro.config.*"))
            if astro_files:
                categories["frontend"].add("Astro")

            # Gatsby
            gatsby_files = list(repo_path.rglob("gatsby-config.*"))
            if gatsby_files:
                categories["frontend"].add("Gatsby")

            # Remix
            remix_files = list(repo_path.rglob("remix.config.*"))
            if remix_files:
                categories["frontend"].add("Remix")

            # Tailwind CSS
            tailwind_files = list(repo_path.rglob("tailwind.config.*"))
            if tailwind_files:
                categories["frontend"].add("Tailwind")

            # Bootstrap
            bootstrap_files = list(repo_path.rglob("bootstrap.*")) + list(
                repo_path.rglob("*.bootstrap.*")
            )
            if bootstrap_files:
                categories["frontend"].add("Bootstrap")

            # Material UI
            material_files = list(repo_path.rglob("*.mui.*")) + list(
                repo_path.rglob("material-ui.*")
            )
            if material_files:
                categories["frontend"].add("MaterialUI")

            # Styled Components
            styled_files = list(repo_path.rglob("*.styled.*")) + list(
                repo_path.rglob("styled-components.*")
            )
            if styled_files:
                categories["frontend"].add("StyledComponents")

            # SASS/SCSS
            sass_files = list(repo_path.rglob("*.scss")) + list(
                repo_path.rglob("*.sass")
            )
            if sass_files:
                categories["frontend"].add("Sass")

            # LESS
            less_files = list(repo_path.rglob("*.less"))
            if less_files:
                categories["frontend"].add("Less")

            # TypeScript
            ts_files = (
                list(repo_path.rglob("*.ts"))
                + list(repo_path.rglob("*.tsx"))
                + list(repo_path.rglob("tsconfig.*"))
            )
            if ts_files:
                categories["frontend"].add("TypeScript")

            # JavaScript
            js_files = list(repo_path.rglob("*.js")) + list(repo_path.rglob("*.jsx"))
            if js_files:
                categories["frontend"].add("JavaScript")

            # Vite
            vite_files = list(repo_path.rglob("vite.config.*"))
            if vite_files:
                categories["frontend"].add("Vite")

            # Webpack
            webpack_files = list(repo_path.rglob("webpack.config.*"))
            if webpack_files:
                categories["frontend"].add("Webpack")

            # Rollup
            rollup_files = list(repo_path.rglob("rollup.config.*"))
            if rollup_files:
                categories["frontend"].add("RollupJS")

            # Gulp
            gulp_files = list(repo_path.rglob("gulpfile.*"))
            if gulp_files:
                categories["frontend"].add("Gulp")

            # HTMX
            htmx_files = list(repo_path.rglob("*.htmx.*")) + list(
                repo_path.rglob("htmx.*")
            )
            if htmx_files:
                categories["frontend"].add("HTMX")

            # Three.js
            threejs_files = list(repo_path.rglob("*.three.*")) + list(
                repo_path.rglob("three.*")
            )
            if threejs_files:
                categories["frontend"].add("ThreeJS")

            # D3.js
            d3_files = list(repo_path.rglob("*.d3.*")) + list(repo_path.rglob("d3.*"))
            if d3_files:
                categories["frontend"].add("D3")

            # P5.js
            p5_files = list(repo_path.rglob("*.p5.*")) + list(repo_path.rglob("p5.*"))
            if p5_files:
                categories["frontend"].add("P5JS")

            # Express.js
            express_files = list(repo_path.rglob("express.*")) + list(
                repo_path.rglob("*.express.*")
            )
            if express_files:
                categories["backend"].add("Express")

            # FastAPI
            fastapi_files = list(repo_path.rglob("fastapi.*")) + list(
                repo_path.rglob("*.fastapi.*")
            )
            if fastapi_files:
                categories["backend"].add("FastAPI")

            # Django
            django_files = (
                list(repo_path.rglob("django.*"))
                + list(repo_path.rglob("*.django.*"))
                + list(repo_path.rglob("manage.py"))
            )
            if django_files:
                categories["backend"].add("Django")

            # Flask
            flask_files = list(repo_path.rglob("flask.*")) + list(
                repo_path.rglob("*.flask.*")
            )
            if flask_files:
                categories["backend"].add("Flask")

            # NestJS
            nestjs_files = list(repo_path.rglob("nest-cli.*")) + list(
                repo_path.rglob("*.nestjs.*")
            )
            if nestjs_files:
                categories["backend"].add("NestJS")

            # Laravel
            laravel_files = list(repo_path.rglob("artisan")) + list(
                repo_path.rglob("*.laravel.*")
            )
            if laravel_files:
                categories["backend"].add("Laravel")

            # Rails
            rails_files = list(repo_path.rglob("Gemfile")) + list(
                repo_path.rglob("*.rails.*")
            )
            if rails_files:
                categories["backend"].add("Rails")

            # Spring
            spring_files = list(repo_path.rglob("*.spring.*")) + list(
                repo_path.rglob("spring.*")
            )
            if spring_files:
                categories["backend"].add("Spring")

            # .NET
            dotnet_files = list(repo_path.rglob("*.csproj")) + list(
                repo_path.rglob("*.sln")
            )
            if dotnet_files:
                categories["backend"].add(".NET")

            # Go
            go_files = list(repo_path.rglob("*.go")) + list(repo_path.rglob("go.mod"))
            if go_files:
                categories["backend"].add("Go")

            # Rust
            rust_files = list(repo_path.rglob("*.rs")) + list(
                repo_path.rglob("Cargo.toml")
            )
            if rust_files:
                categories["backend"].add("Rust")

            # Java
            java_files = list(repo_path.rglob("*.java")) + list(
                repo_path.rglob("pom.xml")
            )
            if java_files:
                categories["backend"].add("Java")

            # Kotlin
            kotlin_files = list(repo_path.rglob("*.kt")) + list(
                repo_path.rglob("*.kts")
            )
            if kotlin_files:
                categories["backend"].add("Kotlin")

            # Scala
            scala_files = list(repo_path.rglob("*.scala"))
            if scala_files:
                categories["backend"].add("Scala")

            # PHP
            php_files = list(repo_path.rglob("*.php"))
            if php_files:
                categories["backend"].add("PHP")

            # Ruby
            ruby_files = list(repo_path.rglob("*.rb"))
            if ruby_files:
                categories["backend"].add("Ruby")

            # Clojure
            clojure_files = list(repo_path.rglob("*.clj")) + list(
                repo_path.rglob("project.clj")
            )
            if clojure_files:
                categories["backend"].add("Clojure")

            # Elixir
            elixir_files = list(repo_path.rglob("*.ex")) + list(
                repo_path.rglob("mix.exs")
            )
            if elixir_files:
                categories["backend"].add("Elixir")

            # Haskell
            haskell_files = list(repo_path.rglob("*.hs")) + list(
                repo_path.rglob("*.cabal")
            )
            if haskell_files:
                categories["backend"].add("Haskell")

            # Crystal
            crystal_files = list(repo_path.rglob("*.cr")) + list(
                repo_path.rglob("shard.yml")
            )
            if crystal_files:
                categories["backend"].add("Crystal")

            # Nim
            nim_files = list(repo_path.rglob("*.nim")) + list(
                repo_path.rglob("*.nimble")
            )
            if nim_files:
                categories["backend"].add("Nim")

            # Zig
            zig_files = list(repo_path.rglob("*.zig")) + list(
                repo_path.rglob("build.zig")
            )
            if zig_files:
                categories["backend"].add("Zig")

            # V
            v_files = list(repo_path.rglob("*.v"))
            if v_files:
                categories["backend"].add("V")

            # R
            r_files = list(repo_path.rglob("*.r")) + list(repo_path.rglob("*.R"))
            if r_files:
                categories["backend"].add("R")

            # MATLAB
            matlab_files = list(repo_path.rglob("*.m"))
            if matlab_files:
                categories["backend"].add("MATLAB")

            # Octave
            octave_files = list(repo_path.rglob("*.octave.*")) + list(
                repo_path.rglob("octave.*")
            )
            if octave_files:
                categories["backend"].add("Octave")

            # Perl
            perl_files = list(repo_path.rglob("*.pl")) + list(repo_path.rglob("*.pm"))
            if perl_files:
                categories["backend"].add("Perl")

            # Dart
            dart_files = list(repo_path.rglob("*.dart")) + list(
                repo_path.rglob("pubspec.yaml")
            )
            if dart_files:
                categories["backend"].add("Dart")

            # Lua
            lua_files = list(repo_path.rglob("*.lua"))
            if lua_files:
                categories["backend"].add("Lua")

            # Haxe
            haxe_files = list(repo_path.rglob("*.hx")) + list(repo_path.rglob("*.hxml"))
            if haxe_files:
                categories["backend"].add("Haxe")

            # Forth
            forth_files = list(repo_path.rglob("*.fs")) + list(repo_path.rglob("*.fth"))
            if forth_files:
                categories["backend"].add("Forth")

            # Fortran
            fortran_files = list(repo_path.rglob("*.f90")) + list(
                repo_path.rglob("*.f95")
            )
            if fortran_files:
                categories["backend"].add("Fortran")

            # OCaml
            ocaml_files = list(repo_path.rglob("*.ml")) + list(repo_path.rglob("*.mli"))
            if ocaml_files:
                categories["backend"].add("OCaml")

            # Swift
            swift_files = list(repo_path.rglob("*.swift"))
            if swift_files:
                categories["backend"].add("Swift")

            # Vala
            vala_files = list(repo_path.rglob("*.vala"))
            if vala_files:
                categories["backend"].add("Vala")

            # C/C++
            c_files = (
                list(repo_path.rglob("*.c"))
                + list(repo_path.rglob("*.cpp"))
                + list(repo_path.rglob("*.h"))
                + list(repo_path.rglob("*.hpp"))
            )
            if c_files:
                categories["backend"].add("C")

            # Additional DevOps tools
            # Ansible
            ansible_files = list(repo_path.rglob("*.yml")) + list(
                repo_path.rglob("*.yaml")
            )
            for ansible_file in ansible_files:
                try:
                    with open(ansible_file, encoding="utf-8") as f:
                        content = f.read().lower()
                        if "ansible" in content and (
                            "hosts:" in content or "tasks:" in content
                        ):
                            categories["devops"].add("Ansible")
                            break
                except Exception:
                    continue

            # Prometheus
            prometheus_files = list(repo_path.rglob("prometheus.*")) + list(
                repo_path.rglob("*.prometheus.*")
            )
            if prometheus_files:
                categories["devops"].add("Prometheus")

            # Grafana
            grafana_files = list(repo_path.rglob("grafana.*")) + list(
                repo_path.rglob("*.grafana.*")
            )
            if grafana_files:
                categories["devops"].add("Grafana")

            # Elasticsearch
            elasticsearch_files = list(repo_path.rglob("elasticsearch.*")) + list(
                repo_path.rglob("*.elasticsearch.*")
            )
            if elasticsearch_files:
                categories["devops"].add("Elasticsearch")

            # Kafka
            kafka_files = list(repo_path.rglob("kafka.*")) + list(
                repo_path.rglob("*.kafka.*")
            )
            if kafka_files:
                categories["devops"].add("Kafka")

            # RabbitMQ
            rabbitmq_files = list(repo_path.rglob("rabbitmq.*")) + list(
                repo_path.rglob("*.rabbitmq.*")
            )
            if rabbitmq_files:
                categories["devops"].add("RabbitMQ")

            # IPFS
            ipfs_files = list(repo_path.rglob("ipfs.*")) + list(
                repo_path.rglob("*.ipfs.*")
            )
            if ipfs_files:
                categories["devops"].add("IPFS")

            # Sentry
            sentry_files = list(repo_path.rglob("sentry.*")) + list(
                repo_path.rglob("*.sentry.*")
            )
            if sentry_files:
                categories["devops"].add("Sentry")

            # Additional AI/ML tools
            # TensorFlow
            tensorflow_files = list(repo_path.rglob("tensorflow.*")) + list(
                repo_path.rglob("*.tensorflow.*")
            )
            if tensorflow_files:
                categories["ai_ml"].add("TensorFlow")

            # PyTorch
            pytorch_files = list(repo_path.rglob("pytorch.*")) + list(
                repo_path.rglob("*.pytorch.*")
            )
            if pytorch_files:
                categories["ai_ml"].add("PyTorch")

            # Scikit-learn
            sklearn_files = list(repo_path.rglob("sklearn.*")) + list(
                repo_path.rglob("*.sklearn.*")
            )
            if sklearn_files:
                categories["ai_ml"].add("Scikit-learn")

            # OpenCV
            opencv_files = list(repo_path.rglob("opencv.*")) + list(
                repo_path.rglob("*.opencv.*")
            )
            if opencv_files:
                categories["ai_ml"].add("OpenCV")

            # Processing
            processing_files = list(repo_path.rglob("*.pde"))
            if processing_files:
                categories["ai_ml"].add("Processing")

            return categories
        except Exception as e:
            log_and_raise(
                DependencyAnalysisError(
                    f"Failed to analyze repository dependencies: {e}",
                    error_code=ErrorCodes.DEPENDENCY_ANALYSIS_FAILED,
                    context={"repo_path": str(repo_path)},
                ),
                logger=logger,
            )
            return {
                "frontend": set(),
                "backend": set(),
                "database": set(),
                "devops": set(),
                "ai_ml": set(),
            }  # This line will never be reached due to log_and_raise

    @with_error_context({"component": "dependency_analyzer"})
    def analyze_all_repositories(self, repos_dir: Path) -> dict[str, Any]:
        """Analyze dependencies from all repositories."""
        all_technologies: dict[str, set[str]] = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }
        try:
            if repos_dir.exists():
                for repo_dir in repos_dir.iterdir():
                    if repo_dir.is_dir():
                        # Check root of repo_dir
                        for fname in ["package.json", "requirements.txt"]:
                            root_file = repo_dir / fname
                            if root_file.exists():
                                repo_tech = self.analyze_repository_dependencies(
                                    repo_dir
                                )
                                for category, techs in repo_tech.items():
                                    all_technologies[category].update(techs)
                        # Recursively search subdirectories
                        for _ in repo_dir.rglob("package.json"):
                            repo_tech = self.analyze_repository_dependencies(_.parent)
                            for category, techs in repo_tech.items():
                                all_technologies[category].update(techs)
                        for _ in repo_dir.rglob("requirements.txt"):
                            repo_tech = self.analyze_repository_dependencies(_.parent)
                            for category, techs in repo_tech.items():
                                all_technologies[category].update(techs)
            # Convert sets to sorted lists
            result = {}
            for category, techs in all_technologies.items():
                result[category] = {
                    "technologies": sorted(techs),
                    "count": len(techs),
                }
            return result
        except Exception as e:
            log_and_raise(
                DependencyAnalysisError(
                    f"Failed to analyze all repositories: {e}",
                    error_code=ErrorCodes.DEPENDENCY_ANALYSIS_FAILED,
                    context={"repos_dir": str(repos_dir)},
                ),
                logger=logger,
            )
            return {}  # This line will never be reached due to log_and_raise

    def analyze_python_dependencies(self, repo_path: str) -> dict[str, Any]:
        """Analyze Python dependencies in a repository."""
        try:
            requirements_files = []

            # Find requirements files
            for pattern in [
                "requirements.txt",
                "requirements/*.txt",
                "pyproject.toml",
                "setup.py",
            ]:
                try:
                    for file_path in Path(repo_path).glob(pattern):
                        if file_path.is_file():
                            requirements_files.append(str(file_path))
                except OSError as e:
                    logger.warning(f"Error searching for {pattern} in {repo_path}: {e}")
                    continue

            if not requirements_files:
                logger.info(f"No Python dependency files found in {repo_path}")
                return {}

            dependencies = {}
            for req_file in requirements_files:
                try:
                    file_deps = self._parse_requirements_file(req_file)
                    dependencies[req_file] = file_deps
                except (FileNotFoundError, PermissionError) as e:
                    logger.warning(f"Could not read {req_file}: {e}")
                except (TypeError, ValueError) as e:
                    logger.warning(f"Error parsing {req_file}: {e}")
                except OSError as e:
                    logger.warning(f"IO error reading {req_file}: {e}")

            return dependencies

        except (TypeError, AttributeError, KeyError) as e:
            logger.error(f"Error analyzing Python dependencies in {repo_path}: {e}")
            return {}
        except OSError as e:
            logger.error(f"IO error analyzing dependencies in {repo_path}: {e}")
            return {}

    def analyze_node_dependencies(self, repo_path: str) -> dict[str, Any]:
        """Analyze Node.js dependencies in a repository."""
        try:
            package_json_path = Path(repo_path) / "package.json"

            if not package_json_path.exists():
                logger.info(f"No package.json found in {repo_path}")
                return {}

            try:
                with open(package_json_path, encoding="utf-8") as f:
                    package_data = json.load(f)

                dependencies = {
                    "dependencies": package_data.get("dependencies", {}),
                    "devDependencies": package_data.get("devDependencies", {}),
                    "peerDependencies": package_data.get("peerDependencies", {}),
                    "optionalDependencies": package_data.get(
                        "optionalDependencies", {}
                    ),
                }

                return dependencies

            except (FileNotFoundError, PermissionError) as e:
                logger.warning(f"Could not read package.json in {repo_path}: {e}")
                return {}
            except (json.JSONDecodeError, TypeError) as e:
                logger.warning(f"Invalid JSON in package.json in {repo_path}: {e}")
                return {}
            except OSError as e:
                logger.warning(f"IO error reading package.json in {repo_path}: {e}")
                return {}

        except (TypeError, AttributeError, KeyError) as e:
            logger.error(f"Error analyzing Node.js dependencies in {repo_path}: {e}")
            return {}
        except OSError as e:
            logger.error(f"IO error analyzing Node.js dependencies in {repo_path}: {e}")
            return {}

    def _parse_requirements_file(self, file_path: str) -> dict[str, str]:
        """Parse a requirements.txt file and return package name to version mapping."""
        try:
            dependencies = {}
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Handle different formats: package==version, package>=version, etc.
                        if "==" in line:
                            package, version = line.split("==", 1)
                        elif ">=" in line:
                            package, version = line.split(">=", 1)
                        elif "<=" in line:
                            package, version = line.split("<=", 1)
                        elif ">" in line:
                            package, version = line.split(">", 1)
                        elif "<" in line:
                            package, version = line.split("<", 1)
                        else:
                            package, version = line, ""

                        package = package.strip().lower()
                        version = version.strip()
                        if package:
                            dependencies[package] = version

            return dependencies
        except (FileNotFoundError, PermissionError) as e:
            logger.warning(f"Could not read requirements file {file_path}: {e}")
            return {}
        except (TypeError, ValueError) as e:
            logger.warning(f"Error parsing requirements file {file_path}: {e}")
            return {}
        except OSError as e:
            logger.warning(f"IO error reading requirements file {file_path}: {e}")
            return {}


def main() -> None:
    """Main function to analyze dependencies."""
    analyzer = DependencyAnalyzer()

    from pathlib import Path

    repos_dir = Path(os.environ.get("REPOS_DIR", "repo-stats"))
    if not repos_dir.exists():
        repos_dir = Path.cwd()

    tech_stack = analyzer.analyze_all_repositories(repos_dir)

    # Save results
    output_file = repos_dir / "tech_stack_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tech_stack, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
