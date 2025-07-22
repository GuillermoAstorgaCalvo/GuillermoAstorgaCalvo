#!/usr/bin/env python3
"""
Skillicon Mapper
Maps dependency names to valid skillicon IDs for the skillicons.dev service.
Only includes technologies that have corresponding icons in the service.
"""


# Valid skillicon IDs from the service (comprehensive list)
VALID_SKILLICONS = {
    "ableton",
    "activitypub",
    "actix",
    "adonis",
    "ae",
    "aiscript",
    "alpinejs",
    "anaconda",
    "androidstudio",
    "angular",
    "ansible",
    "apollo",
    "apple",
    "appwrite",
    "arch",
    "arduino",
    "astro",
    "atom",
    "au",
    "autocad",
    "aws",
    "azul",
    "azure",
    "babel",
    "bash",
    "bevy",
    "bitbucket",
    "blender",
    "bootstrap",
    "bsd",
    "bun",
    "c",
    "cs",
    "cpp",
    "crystal",
    "cassandra",
    "clion",
    "clojure",
    "cloudflare",
    "cmake",
    "codepen",
    "coffeescript",
    "css",
    "cypress",
    "d3",
    "dart",
    "debian",
    "deno",
    "devto",
    "discord",
    "bots",
    "discordjs",
    "django",
    "docker",
    "dotnet",
    "dynamodb",
    "eclipse",
    "elasticsearch",
    "electron",
    "elixir",
    "elysia",
    "emacs",
    "ember",
    "emotion",
    "express",
    "fastapi",
    "fediverse",
    "figma",
    "firebase",
    "flask",
    "flutter",
    "forth",
    "fortran",
    "gamemakerstudio",
    "gatsby",
    "gcp",
    "git",
    "github",
    "githubactions",
    "gitlab",
    "gmail",
    "gherkin",
    "go",
    "gradle",
    "godot",
    "grafana",
    "graphql",
    "gtk",
    "gulp",
    "haskell",
    "haxe",
    "haxeflixel",
    "heroku",
    "hibernate",
    "html",
    "htmx",
    "idea",
    "ai",
    "instagram",
    "ipfs",
    "java",
    "js",
    "jenkins",
    "jest",
    "jquery",
    "kafka",
    "kali",
    "kotlin",
    "ktor",
    "kubernetes",
    "laravel",
    "latex",
    "less",
    "linkedin",
    "linux",
    "lit",
    "lua",
    "md",
    "mastodon",
    "materialui",
    "matlab",
    "maven",
    "mint",
    "misskey",
    "mongodb",
    "mysql",
    "neovim",
    "nestjs",
    "netlify",
    "nextjs",
    "nginx",
    "nim",
    "nix",
    "nodejs",
    "notion",
    "npm",
    "nuxtjs",
    "obsidian",
    "ocaml",
    "octave",
    "opencv",
    "openshift",
    "openstack",
    "p5js",
    "perl",
    "ps",
    "php",
    "phpstorm",
    "pinia",
    "pkl",
    "plan9",
    "planetscale",
    "pnpm",
    "postgres",
    "postman",
    "powershell",
    "pr",
    "prisma",
    "processing",
    "prometheus",
    "pug",
    "pycharm",
    "py",
    "pytorch",
    "qt",
    "r",
    "rabbitmq",
    "rails",
    "raspberrypi",
    "react",
    "reactivex",
    "redhat",
    "redis",
    "redux",
    "regex",
    "remix",
    "replit",
    "rider",
    "robloxstudio",
    "rocket",
    "rollupjs",
    "ros",
    "ruby",
    "rust",
    "sass",
    "spring",
    "sqlite",
    "stackoverflow",
    "styledcomponents",
    "sublime",
    "supabase",
    "scala",
    "sklearn",
    "selenium",
    "sentry",
    "sequelize",
    "sketchup",
    "solidity",
    "solidjs",
    "svelte",
    "svg",
    "swift",
    "symfony",
    "tailwind",
    "tauri",
    "tensorflow",
    "terraform",
    "threejs",
    "twitter",
    "ts",
    "ubuntu",
    "unity",
    "unreal",
    "v",
    "vala",
    "vercel",
    "vim",
    "visualstudio",
    "vite",
    "vitest",
    "vscode",
    "vscodium",
    "vue",
    "vuetify",
    "wasm",
    "webflow",
    "webpack",
    "webstorm",
    "windicss",
    "windows",
    "wordpress",
    "workers",
    "xd",
    "yarn",
    "yew",
    "zig",
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
            "pinia": "pinia",
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
            # Alpine.js
            "alpinejs": "alpinejs",
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
            "selenium": "selenium",
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
            "p5js": "p5js",
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
            # Additional frontend frameworks
            "htmx": "htmx",
            "lit": "lit",
            "ember": "ember",
            "alpine": "alpinejs",
        }

        # Backend technology mappings to skillicon IDs
        self.backend_mappings = {
            # Node.js ecosystem
            "express": "express",
            "express.js": "express",
            "@types/express": "express",
            "node": "nodejs",
            "nodejs": "nodejs",
            "nestjs": "nestjs",
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
            "Python": "py",
            "anaconda": "anaconda",
            # Java ecosystem
            "java": "java",
            "spring-boot": "spring",
            "spring": "spring",
            "maven": "maven",
            "gradle": "gradle",
            "hibernate": "hibernate",
            "kotlin": "kotlin",
            "ktor": "ktor",
            "scala": "scala",
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
            "actix": "actix",
            # C#
            "csharp": "cs",
            "dotnet": "dotnet",
            ".net": "dotnet",
            # C/C++
            "c": "c",
            "cpp": "cpp",
            "c++": "cpp",
            # Other languages
            "clojure": "clojure",
            "elixir": "elixir",
            "haskell": "haskell",
            "crystal": "crystal",
            "nim": "nim",
            "zig": "zig",
            "v": "v",
            "r": "r",
            "matlab": "matlab",
            "octave": "octave",
            "perl": "perl",
            "dart": "dart",
            "lua": "lua",
            "haxe": "haxe",
            "haxeflixel": "haxeflixel",
            "forth": "forth",
            "fortran": "fortran",
            "ocaml": "ocaml",
            "swift": "swift",
            "vala": "vala",
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
            # Additional backend frameworks
            "adonis": "adonis",
            "elysia": "elysia",
            "rocket": "rocket",
            "bevy": "bevy",
            "godot": "godot",
            "unity": "unity",
            "unreal": "unreal",
            "gamemakerstudio": "gamemakerstudio",
            "robloxstudio": "robloxstudio",
        }

        # Database technology mappings
        self.database_mappings = {
            "postgres": "postgres",
            "postgresql": "postgres",
            "PostgreSQL": "postgres",
            "mysql": "mysql",
            "MySQL": "mysql",
            "mongodb": "mongodb",
            "MongoDB": "mongodb",
            "redis": "redis",
            "Redis": "redis",
            "sqlite": "sqlite",
            "SQLite": "sqlite",
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
            "Docker": "docker",
            "kubernetes": "kubernetes",
            "Kubernetes": "kubernetes",
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
            "Nginx": "nginx",
            "jenkins": "jenkins",
            "github-actions": "githubactions",
            "githubactions": "githubactions",
            "GitHub Actions": "githubactions",
            "gitlab-ci": "gitlab",
            "GitLab": "gitlab",
            "bitbucket-pipelines": "bitbucket",
            "bitbucket": "bitbucket",
            "terraform": "terraform",
            "Terraform": "terraform",
            "ansible": "ansible",
            "prometheus": "prometheus",
            "grafana": "grafana",
            "elasticsearch": "elasticsearch",
            "kafka": "kafka",
            "rabbitmq": "rabbitmq",
            "ipfs": "ipfs",
            "sentry": "sentry",
            # Additional DevOps tools
            "cmake": "cmake",
            "openshift": "openshift",
            "openstack": "openstack",
            "redhat": "redhat",
            "ubuntu": "ubuntu",
            "debian": "debian",
            "arch": "arch",
            "bsd": "bsd",
            "kali": "kali",
            "linux": "linux",
            "windows": "windows",
            "apple": "apple",
            "plan9": "plan9",
            "ros": "ros",
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
            "ai": "ai",
            "aiscript": "aiscript",
            "processing": "processing",
        }

        # Development tools and IDEs
        self.tools_mappings = {
            "vscode": "vscode",
            "vscodium": "vscodium",
            "vim": "vim",
            "neovim": "neovim",
            "emacs": "emacs",
            "idea": "idea",
            "pycharm": "pycharm",
            "clion": "clion",
            "phpstorm": "phpstorm",
            "webstorm": "webstorm",
            "rider": "rider",
            "sublime": "sublime",
            "atom": "atom",
            "obsidian": "obsidian",
            "visualstudio": "visualstudio",
            "eclipse": "eclipse",
            "androidstudio": "androidstudio",
            "xcode": "apple",  # No xcode icon, use apple
            "notion": "notion",
            "figma": "figma",
            "sketchup": "sketchup",
            "blender": "blender",
            "autocad": "autocad",
            "ae": "ae",
            "ps": "ps",
            "au": "au",
            "ableton": "ableton",
            "xd": "xd",
            "sketch": "figma",  # No sketch icon, use figma
        }

        # Package managers and build tools
        self.package_mappings = {
            "npm": "npm",
            "yarn": "yarn",
            "pnpm": "pnpm",
            "bun": "bun",
            "deno": "deno",
            "maven": "maven",
            "gradle": "gradle",
            "pip": "py",
            "conda": "anaconda",
            "cargo": "rust",
            "go.mod": "go",
            "composer": "php",
            "gem": "ruby",
            "hex": "elixir",
            "stack": "haskell",
            "cabal": "haskell",
        }

        # Social and communication platforms
        self.social_mappings = {
            "discord": "discord",
            "discordjs": "discordjs",
            "twitter": "twitter",
            "instagram": "instagram",
            "linkedin": "linkedin",
            "devto": "devto",
            "stackoverflow": "stackoverflow",
            "codepen": "codepen",
            "replit": "replit",
            "github": "github",
            "gitlab": "gitlab",
            "bitbucket": "bitbucket",
            "gmail": "gmail",
            "mastodon": "mastodon",
            "misskey": "misskey",
            "fediverse": "fediverse",
            "activitypub": "activitypub",
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
                # Try all mappings for unknown categories
                all_mappings = {
                    **self.frontend_mappings,
                    **self.backend_mappings,
                    **self.database_mappings,
                    **self.devops_mappings,
                    **self.ai_ml_mappings,
                    **self.tools_mappings,
                    **self.package_mappings,
                    **self.social_mappings,
                }
                mapped_techs = self._map_category(
                    data.get("technologies", []), all_mappings
                )

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
