---
name: package-version-lookup
description: Find the latest package versions from official registries. Use when adding new packages to dependency files, updating existing package versions, or before suggesting any package installation.
compatibility: opencode
---

# Package Version Lookup

## Overview

This skill provides guidance for finding accurate package version information before adding or updating dependencies. Default to the latest stable version unless the user has explicitly specified a particular version.

## When to Use

- Adding new packages to package.json, requirements.txt, Cargo.toml, etc.
- Updating existing package versions
- Before suggesting any package installation
- When user asks "what's the latest version of X?"

## Methods (In Priority Order)

### 1. Context7 (Preferred for Technical Documentation)

Use `context7_resolve-library-id` to find the Context7-compatible library ID, then use `context7_query-docs` to get version information.

**Best for:** Libraries with comprehensive documentation (e.g., Next.js, React, FastAPI)

### 2. WebFetch (Preferred for Package Registries)

Use `webfetch` to scrape version information directly from official package registries:

| Ecosystem | Registry URL |
|-----------|-------------|
| npm/Node.js | https://www.npmjs.com/package/{package-name} |
| Python (PyPI) | https://pypi.org/project/{package-name}/ |
| Rust (crates.io) | https://crates.io/crates/{package-name} |
| Go | https://pkg.go.dev/{package-path} |
| Ruby (RubyGems) | https://rubygems.org/gems/{package-name} |
| PHP (Packagist) | https://packagist.org/packages/{vendor}/{package} |

**Best for:** Quick lookups when the package registry page is reliable

### 3. Web Search (Fallback)

If the above methods fail, search for "{package name} latest version" or visit the package's GitHub releases page.

**Best for:** Niche packages or when registry pages are blocked

## Version Selection Rules

1. **Default to latest stable** unless user explicitly requests a specific version
2. **Avoid pre-release versions** (alpha, beta, rc) unless user asks for them
3. **Check multiple sources** if version numbers conflict
4. **Never guess** - always verify from official sources

## Examples

### npm Package
```
User: "Add react-query to my project"
→ Use webfetch on https://www.npmjs.com/package/@tanstack/react-query
→ Extract latest version from the page
```

### Python Package
```
User: "Update fastapi version"
→ Use context7_resolve-library-id with "fastapi"
→ Query docs for latest version
```

### Rust Package
```
User: "Add serde"
→ Use webfetch on https://crates.io/crates/serde
→ Extract version from the page
```

## Important Notes

- Always check the **official package registry**, not blogs or tutorials
- Look for the version number prominently displayed on the package page
- If a version is specified in AGENTS.md or project files, follow that unless updating
- Never use versions from previous projects without verifying
