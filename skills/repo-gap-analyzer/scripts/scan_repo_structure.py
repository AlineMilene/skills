#!/usr/bin/env python3
"""
Scan a repository structure to generate a token-efficient architectural overview.

Detects languages, frameworks, architecture layers, resilience libraries,
test coverage indicators, and potential red flags.

Usage:
    python scripts/scan_repo_structure.py <repo-path>
    python scripts/scan_repo_structure.py <repo-path> --format json
    python scripts/scan_repo_structure.py <repo-path> --out /tmp/repo-scan.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

IGNORE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "vendor", "target", "build", "dist",
    ".idea", ".vscode", "__pycache__", ".pytest_cache", ".tox", ".gradle",
    "bin", "obj", ".next", ".nuxt", "coverage", ".terraform", "venv", ".venv", "env",
    ".cache", ".yarn", ".cargo"
}

ARCH_PATTERNS = {
    "Clean/Hexagonal Architecture": [
        "domain", "entity", "entities", "usecase", "usecases", "use_cases",
        "port", "ports", "adapter", "adapters", "infrastructure", "infra",
        "application", "core", "boundary", "gateway", "gateways"
    ],
    "MVC / Traditional Layered": [
        "controller", "controllers", "service", "services", "repository", "repositories",
        "model", "models", "view", "views", "dao", "dto"
    ],
    "Event-Driven / Messaging": [
        "consumer", "consumers", "producer", "producers", "event", "events",
        "listener", "listeners", "handler", "handlers", "saga", "queue", "topic"
    ],
    "System Design / Resilience Markers": [
        "circuit_breaker", "resilience", "retry", "ratelimit", "rate_limit",
        "cache", "redis", "memcached", "kafka", "rabbitmq", "sqs", "bulkhead",
        "telemetry", "tracing", "otel", "metrics", "health", "liveness", "readiness"
    ]
}

TECH_STACK_SIGNATURES = {
    "package.json": "Node.js / TypeScript / JavaScript",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java / Kotlin (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "requirements.txt": "Python (pip)",
    "pyproject.toml": "Python (Modern)",
    "Pipfile": "Python (Pipenv)",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "composer.json": "PHP",
    "Gemfile": "Ruby",
    ".csproj": ".NET / C# Project",
    ".sln": ".NET Solution",
    "Directory.Build.props": ".NET Build Configuration",
    "Dockerfile": "Containerization (Docker)",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
    "k8s": "Kubernetes manifests",
    "helm": "Helm Charts",
    "main.tf": "Terraform (IaC)",
    "sonar-project.properties": "SonarQube Analysis"
}

def scan_repository(repo_path: str) -> dict:
    base = Path(repo_path).resolve()
    if not base.exists() or not base.is_dir():
        return {"error": f"Path '{repo_path}' is not a valid directory."}

    ext_counter = Counter()
    total_files = 0
    total_dirs = 0
    detected_stacks = set()
    layer_hits = {cat: set() for cat in ARCH_PATTERNS}
    has_tests = False
    has_ci_cd = False
    has_docker = False
    has_observability = False
    top_level_entries = []

    try:
        top_level_entries = [e.name for e in base.iterdir()]
    except Exception:
        pass

    # Check CI/CD
    github_workflows = base / ".github" / "workflows"
    gitlab_ci = base / ".gitlab-ci.yml"
    azure_pipelines = base / "azure-pipelines.yml"
    if github_workflows.exists() or gitlab_ci.exists() or azure_pipelines.exists():
        has_ci_cd = True

    for root, dirs, files in os.walk(base):
        # Exclude ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        total_dirs += len(dirs)

        rel_root = os.path.relpath(root, base)
        path_parts = set(re.split(r"[/\\_.-]", rel_root.lower()))

        for cat, markers in ARCH_PATTERNS.items():
            for m in markers:
                if m in path_parts:
                    layer_hits[cat].add(m)

        for f in files:
            total_files += 1
            f_lower = f.lower()

            if f in TECH_STACK_SIGNATURES:
                detected_stacks.add(TECH_STACK_SIGNATURES[f])
            elif f_lower.endswith(".csproj"):
                detected_stacks.add(".NET / C# (.csproj)")
            elif f_lower.endswith(".sln"):
                detected_stacks.add(".NET Solution (.sln)")

            if "test" in f_lower or "spec" in f_lower:
                has_tests = True

            if "docker" in f_lower:
                has_docker = True

            if any(term in f_lower for term in ["otel", "prometheus", "datadog", "telemetry", "trace", "metrics"]):
                has_observability = True

            ext = os.path.splitext(f)[1].lower()
            if ext:
                ext_counter[ext] += 1

    return {
        "repository_path": str(base),
        "total_files": total_files,
        "total_directories": total_dirs,
        "top_level_items": top_level_entries,
        "primary_file_types": ext_counter.most_common(8),
        "detected_tech_stacks": sorted(list(detected_stacks)),
        "architecture_indicators": {
            k: sorted(list(v)) for k, v in layer_hits.items() if v
        },
        "flags": {
            "has_automated_tests": has_tests,
            "has_ci_cd_pipelines": has_ci_cd,
            "has_container_support": has_docker,
            "has_observability_signals": has_observability
        }
    }

def print_text_report(data: dict):
    if "error" in data:
        print(f"Error: {data['error']}")
        return

    print("=" * 60)
    print(f"  Repository Structure Scan: {data['repository_path']}")
    print("=" * 60)
    print(f"Files scanned: {data['total_files']} | Dirs: {data['total_directories']}")
    print("\nDetected Stacks:")
    for s in data["detected_tech_stacks"]:
        print(f"  - {s}")

    print("\nArchitecture Layer Indicators:")
    for cat, markers in data["architecture_indicators"].items():
        print(f"  - {cat}: {', '.join(markers)}")

    print("\nQuality & Operational Signals:")
    for flag, val in data["flags"].items():
        status = "YES" if val else "NOT DETECTED"
        print(f"  - {flag}: {status}")

    print("\nTop File Extensions:")
    for ext, count in data["primary_file_types"]:
        print(f"  - {ext}: {count} files")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan repo structure for architectural audit")
    parser.add_argument("repo_path", help="Path to repository")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--out", help="Write JSON output to file")
    args = parser.parse_args()

    results = scan_repository(args.repo_path)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Report saved to {args.out}")

    if args.format == "json":
        print(json.dumps(results, indent=2))
    elif not args.out:
        print_text_report(results)
