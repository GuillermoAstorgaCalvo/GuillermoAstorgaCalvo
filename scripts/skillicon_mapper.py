#!/usr/bin/env python3
"""
Skillicon Mapper
Maps dependency names to valid skillicon IDs for the skillicons.dev service.
Only includes technologies that have corresponding icons in the service.
"""


# Valid skillicon IDs from the service
VALID_SKILLICONS = {
    # Frontend
    "react",
    "vue",
    "angular",
    "nextjs",
    "nuxtjs",
    "svelte",
    "solidjs",
    "astro",
    "gatsby",
    "remix",
    "tailwind",
    "bootstrap",
    "materialui",
    "styledcomponents",
    "emotion",
    "sass",
    "less",
    "css",
    "html",
    "js",
    "ts",
    "vite",
    "webpack",
    "rollupjs",
    "gulp",
    "lit",
    "htmx",
    "p5js",
    "threejs",
    "d3",
    # Backend
    "express",
    "fastapi",
    "django",
    "flask",
    "nestjs",
    "laravel",
    "rails",
    "spring",
    "dotnet",
    "go",
    "rust",
    "nodejs",
    "py",
    "php",
    "java",
    "cs",
    "cpp",
    "c",
    "kotlin",
    "scala",
    "clojure",
    "elixir",
    "haskell",
    "crystal",
    "nim",
    "zig",
    "v",
    "r",
    "matlab",
    "octave",
    "perl",
    "ruby",
    "dart",
    "lua",
    "haxe",
    # Databases
    "postgres",
    "mysql",
    "mongodb",
    "redis",
    "sqlite",
    "dynamodb",
    "cassandra",
    "planetscale",
    # DevOps & Cloud
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "heroku",
    "vercel",
    "netlify",
    "cloudflare",
    "nginx",
    "jenkins",
    "githubactions",
    "gitlab",
    "bitbucket",
    "terraform",
    "ansible",
    "prometheus",
    "grafana",
    "elasticsearch",
    "kafka",
    "rabbitmq",
    "ipfs",
    # Tools & Platforms
    "git",
    "github",
    "npm",
    "yarn",
    "pnpm",
    "bun",
    "deno",
    "vscode",
    "vim",
    "neovim",
    "emacs",
    "idea",
    "pycharm",
    "clion",
    "phpstorm",
    "webstorm",
    "rider",
    "sublime",
    "atom",
    "obsidian",
    "notion",
    "figma",
    "sketchup",
    "blender",
    "unity",
    "unreal",
    "godot",
    "gamemakerstudio",
    "arduino",
    "raspberrypi",
    "androidstudio",
    "eclipse",
    "maven",
    "gradle",
    # Frameworks & Libraries
    "prisma",
    "sequelize",
    "hibernate",
    "jquery",
    "jest",
    "cypress",
    "selenium",
    "playwright",
    "pytorch",
    "tensorflow",
    "sklearn",
    "opencv",
    "processing",
    "bevy",
    "gtk",
    "qt",
    "electron",
    "tauri",
    "flutter",
    "reactnative",
    "ionic",
    "capacitor",
    "cordova",
    "xamarin",
    # Authentication & Services
    "supabase",
    "firebase",
    "auth0",
    "stripe",
    "twilio",
    "sendgrid",
    "mailgun",
    "sentry",
    "discord",
    "discordjs",
    "telegram",
    "slack",
    "twitter",
    "instagram",
    "linkedin",
    "devto",
    "stackoverflow",
    "codepen",
    "replit",
    "webflow",
    # Other
    "md",
    "regex",
    "wasm",
    "workers",
    "ai",
    "bots",
    "fediverse",
    "mastodon",
    "misskey",
    "activitypub",
    "apple",
    "linux",
    "windows",
    "ubuntu",
    "debian",
    "arch",
    "bsd",
    "kali",
    "redhat",
    "fedora",
    "openshift",
    "openstack",
    "plan9",
    "ros",
    "forth",
    "fortran",
    "autocad",
    "ae",
    "ps",
    "au",
    "ableton",
    "gmail",
    "wordpress",
    "latex",
    "gherkin",
    "pkl",
    "yew",
    "elysia",
    "actix",
    "adonis",
    "apollo",
    "appwrite",
    "azul",
    "babel",
    "bash",
    "coffeescript",
    "ember",
    "haxeflixel",
    "ktor",
    "mint",
    "nix",
    "pinia",
    "postman",
    "powershell",
    "pr",
    "pug",
    "reactivex",
    "robloxstudio",
    "rocket",
    "solidity",
    "svg",
    "swift",
    "symfony",
    "vala",
    "visualstudio",
    "vitest",
    "vscodium",
    "vuetify",
    "windicss",
    "xd",
}


class SkilliconMapper:
    """Maps dependency names to valid skillicon IDs."""

    def __init__(self):
        # Frontend technology mappings to skillicon IDs
        self.frontend_mappings = {
            # React ecosystem
            "react": "react",
            "react-dom": "react",
            "@types/react": "react",
            "react-router-dom": "react",
            "react-hook-form": "react",
            "@hookform/resolvers": "react",
            "react-day-picker": "react",
            "react-resizable-panels": "react",
            "react-icons": "react",
            "react-hot-toast": "react",
            "react-konva": "react",
            "@xyflow/react": "react",
            "@react-google-maps/api": "react",
            "@googlemaps/js-api-loader": "react",
            "@googlemaps/markerclusterer": "react",
            "@tanstack/react-query": "react",
            # Vue ecosystem
            "vue": "vue",
            "@vue/cli": "vue",
            "vue-router": "vue",
            "pinia": "vue",
            "vuetify": "vuetify",
            # Angular
            "angular": "angular",
            "@angular/core": "angular",
            "@angular/common": "angular",
            # Next.js
            "next": "nextjs",
            "next.js": "nextjs",
            "@next/font": "nextjs",
            "next-themes": "nextjs",
            # Nuxt.js
            "nuxt": "nuxtjs",
            "nuxtjs": "nuxtjs",
            # Svelte
            "svelte": "svelte",
            "@sveltejs/kit": "svelte",
            # SolidJS
            "solid-js": "solidjs",
            "solidjs": "solidjs",
            # Astro
            "astro": "astro",
            # Gatsby
            "gatsby": "gatsby",
            # Remix
            "remix": "remix",
            # Styling
            "tailwindcss": "tailwind",
            "tailwind": "tailwind",
            "@tailwindcss/forms": "tailwind",
            "tailwind-merge": "tailwind",
            "tailwindcss-animate": "tailwind",
            "windicss": "windicss",
            "bootstrap": "bootstrap",
            "@bootstrap": "bootstrap",
            "styled-components": "styledcomponents",
            "styled": "styledcomponents",
            "@emotion/react": "emotion",
            "@emotion/styled": "emotion",
            "emotion": "emotion",
            "sass": "sass",
            "scss": "sass",
            "node-sass": "sass",
            "less": "less",
            # TypeScript & JavaScript
            "typescript": "ts",
            "@types/node": "ts",
            "javascript": "js",
            "js": "js",
            # Build tools
            "vite": "vite",
            "@vitejs/plugin-react-swc": "vite",
            "webpack": "webpack",
            "rollup": "rollupjs",
            "rollupjs": "rollupjs",
            "gulp": "gulp",
            "esbuild": "webpack",  # No esbuild icon, use webpack
            # Testing
            "jest": "jest",
            "cypress": "cypress",
            "playwright": "playwright",
            "@playwright/test": "playwright",
            "vitest": "vitest",
            # Utilities
            "lodash": "js",  # No lodash icon, use js
            "axios": "js",  # No axios icon, use js
            "zod": "ts",  # No zod icon, use ts
            # Maps and visualization
            "@turf/turf": "d3",  # No turf icon, use d3
            "proj4": "js",  # No proj4 icon, use js
            "konva": "js",  # No konva icon, use js
            "three": "threejs",
            "three.js": "threejs",
            "threejs": "threejs",
            "d3": "d3",
            # Authentication
            "@supabase/auth-helpers-react": "supabase",
            "@supabase/supabase-js": "supabase",
            "supabase": "supabase",
            "@stripe/stripe-js": "stripe",
            # Development tools
            "eslint": "eslint",
            "eslint-config-prettier": "eslint",
            "eslint-plugin-security": "eslint",
            "eslint-plugin-sonarjs": "eslint",
            "autoprefixer": "postcss",
            "postcss": "postcss",
            # File handling
            "html2canvas": "js",
            "jspdf": "js",
            "file-saver": "js",
            "dompurify": "js",
            "uuid": "js",
            "dotenv": "js",
        }

        # Backend technology mappings to skillicon IDs
        self.backend_mappings = {
            # Node.js ecosystem
            "express": "express",
            "express.js": "express",
            "@types/express": "express",
            "node": "nodejs",
            "nodejs": "nodejs",
            # Python ecosystem
            "fastapi": "fastapi",
            "fast-api": "fastapi",
            "uvicorn": "fastapi",
            "django": "django",
            "djangorestframework": "django",
            "django-cors-headers": "django",
            "flask": "flask",
            "flask-cors": "flask",
            "python": "py",
            "py": "py",
            # Java ecosystem
            "java": "java",
            "spring-boot": "spring",
            "spring": "spring",
            "maven": "maven",
            "gradle": "gradle",
            "hibernate": "hibernate",
            # PHP ecosystem
            "php": "php",
            "laravel": "laravel",
            "symfony": "symfony",
            # Ruby ecosystem
            "ruby": "ruby",
            "rails": "rails",
            # Go
            "go": "go",
            "golang": "go",
            # Rust
            "rust": "rust",
            # C#
            "csharp": "cs",
            "dotnet": "dotnet",
            ".net": "dotnet",
            # Kotlin
            "kotlin": "kotlin",
            "ktor": "ktor",
            # Scala
            "scala": "scala",
            # Security & middleware
            "cors": "cors",
            "helmet": "helmet",
            "bcrypt": "js",  # No bcrypt icon, use js
            "jsonwebtoken": "js",  # No JWT icon, use js
            "passport": "js",  # No passport icon, use js
            # Python specific
            "starlette": "fastapi",  # No starlette icon, use fastapi
            "pydantic": "py",  # No pydantic icon, use py
            "pydantic-settings": "py",
            "pydantic-core": "py",
            "python-jose": "py",
            "passlib": "py",
            "python-multipart": "py",
            "pyjwt": "py",
            "email-validator": "py",
            # Testing
            "jest": "jest",
            "pytest": "py",
            "unittest": "py",
            # Database
            "postgres": "postgres",
            "postgresql": "postgres",
            "mysql": "mysql",
            "mongodb": "mongodb",
            "redis": "redis",
            "sqlite": "sqlite",
            "dynamodb": "dynamodb",
            "cassandra": "cassandra",
            "planetscale": "planetscale",
            "prisma": "prisma",
            "sequelize": "sequelize",
            "sqlalchemy": "py",
            # Cloud & DevOps
            "aws": "aws",
            "aws-sdk": "aws",
            "azure": "azure",
            "gcp": "gcp",
            "google-cloud": "gcp",
            "heroku": "heroku",
            "vercel": "vercel",
            "netlify": "netlify",
            "cloudflare": "cloudflare",
            "docker": "docker",
            "kubernetes": "kubernetes",
            "k8s": "kubernetes",
            "nginx": "nginx",
            "jenkins": "jenkins",
            "github-actions": "githubactions",
            "githubactions": "githubactions",
            "gitlab-ci": "gitlab",
            "bitbucket-pipelines": "bitbucket",
            "terraform": "terraform",
            "ansible": "ansible",
            "prometheus": "prometheus",
            "grafana": "grafana",
            "elasticsearch": "elasticsearch",
            "kafka": "kafka",
            "rabbitmq": "rabbitmq",
            "ipfs": "ipfs",
            # Monitoring & logging
            "winston": "nodejs",  # No winston icon, use nodejs
            "pino": "nodejs",  # No pino icon, use nodejs
            "sentry": "sentry",
            # Other
            "cron": "nodejs",  # No cron icon, use nodejs
            "node-cron": "nodejs",
            "compression": "nodejs",  # No compression icon, use nodejs
            "rate-limiter": "nodejs",  # No rate limiter icon, use nodejs
            "lru-cache": "nodejs",  # No LRU cache icon, use nodejs
            "node-cache": "nodejs",
            "undici": "nodejs",  # No undici icon, use nodejs
            "xml2js": "nodejs",  # No xml2js icon, use nodejs
            "ts-jest": "jest",
            "ts-node-dev": "nodejs",
            "tsc-alias": "ts",
            "tsconfig-paths": "ts",
        }

        # Database technology mappings
        self.database_mappings = {
            "postgres": "postgres",
            "postgresql": "postgres",
            "mysql": "mysql",
            "mongodb": "mongodb",
            "redis": "redis",
            "sqlite": "sqlite",
            "dynamodb": "dynamodb",
            "cassandra": "cassandra",
            "planetscale": "planetscale",
            "prisma": "prisma",
            "sequelize": "sequelize",
            "hibernate": "hibernate",
            "sqlalchemy": "py",
        }

        # DevOps technology mappings
        self.devops_mappings = {
            "docker": "docker",
            "kubernetes": "kubernetes",
            "k8s": "kubernetes",
            "aws": "aws",
            "aws-sdk": "aws",
            "azure": "azure",
            "gcp": "gcp",
            "google-cloud": "gcp",
            "heroku": "heroku",
            "vercel": "vercel",
            "netlify": "netlify",
            "cloudflare": "cloudflare",
            "nginx": "nginx",
            "jenkins": "jenkins",
            "github-actions": "githubactions",
            "githubactions": "githubactions",
            "gitlab-ci": "gitlab",
            "bitbucket-pipelines": "bitbucket",
            "terraform": "terraform",
            "ansible": "ansible",
            "prometheus": "prometheus",
            "grafana": "grafana",
            "elasticsearch": "elasticsearch",
            "kafka": "kafka",
            "rabbitmq": "rabbitmq",
            "ipfs": "ipfs",
            "sentry": "sentry",
        }

        # AI/ML technology mappings
        self.ai_ml_mappings = {
            "tensorflow": "tensorflow",
            "pytorch": "pytorch",
            "scikit-learn": "sklearn",
            "sklearn": "sklearn",
            "opencv": "opencv",
            "opencv-python": "opencv",
            "numpy": "py",
            "pandas": "py",
            "matplotlib": "py",
            "seaborn": "py",
            "jupyter": "py",
            "ipython": "py",
        }

    def map_technologies(
        self, tech_stack: dict[str, dict[str, list[str]]]
    ) -> dict[str, dict[str, list[str]]]:
        """
        Map technology names to valid skillicon IDs.

        Args:
            tech_stack: Dictionary with categories and their technologies

        Returns:
            Dictionary with mapped skillicon IDs
        """
        mapped_stack = {}

        for category, data in tech_stack.items():
            if category == "frontend":
                mapped_techs = self._map_category(
                    data.get("technologies", []), self.frontend_mappings
                )
            elif category == "backend":
                mapped_techs = self._map_category(
                    data.get("technologies", []), self.backend_mappings
                )
            elif category == "database":
                mapped_techs = self._map_category(
                    data.get("technologies", []), self.database_mappings
                )
            elif category == "devops":
                mapped_techs = self._map_category(
                    data.get("technologies", []), self.devops_mappings
                )
            elif category == "ai_ml":
                mapped_techs = self._map_category(
                    data.get("technologies", []), self.ai_ml_mappings
                )
            else:
                mapped_techs = []

            # Only include categories that have valid technologies
            if mapped_techs:
                mapped_stack[category] = {
                    "technologies": mapped_techs,
                    "count": len(mapped_techs),
                }

        return mapped_stack

    def _map_category(
        self, technologies: list[str], mapping: dict[str, str]
    ) -> list[str]:
        """
        Map a list of technologies to skillicon IDs.

        Args:
            technologies: List of technology names
            mapping: Dictionary mapping technology names to skillicon IDs

        Returns:
            List of valid skillicon IDs
        """
        mapped_techs = set()

        for tech in technologies:
            # Try exact match first
            if tech in mapping:
                skillicon_id = mapping[tech]
                if skillicon_id in VALID_SKILLICONS:
                    mapped_techs.add(skillicon_id)
                continue

            # Try case-insensitive match
            tech_lower = tech.lower()
            for key, value in mapping.items():
                if key.lower() == tech_lower:
                    if value in VALID_SKILLICONS:
                        mapped_techs.add(value)
                    break

            # Try partial match for common patterns
            if not any(key.lower() in tech_lower for key in mapping):
                # Check if the tech name itself is a valid skillicon
                if tech in VALID_SKILLICONS:
                    mapped_techs.add(tech)

        return sorted(mapped_techs)
