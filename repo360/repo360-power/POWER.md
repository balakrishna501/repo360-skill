# Repo360 - Engineering Intelligence Layer for AI-Generated Software

## Overview

Repo360 is an enterprise-grade engineering intelligence layer that analyzes GitHub repositories to detect code quality issues, security vulnerabilities, architectural problems, and technical debt. It goes beyond traditional code analysis by using AI to understand, explain, and monitor your codebase comprehensively.

## Problem Statement

AI coding assistants accelerate development but introduce challenges:
- Inconsistent code structure and architecture
- Poor readability & maintainability
- Duplicate or unnecessary code
- Inconsistent design patterns
- Insufficient test coverage
- Increased technical debt
- Security & dependency risks
- Harder debugging & root-cause analysis
- Non-compliance with org standards

## Solution

Repo360 analyzes repositories line-by-line across multiple dimensions:

### Core Capabilities

1. **Code Quality Analysis**
   - Detects AI-generated vs human-written code patterns
   - Analyzes code structure, readability, and maintainability
   - Identifies duplicate or unnecessary code
   - Evaluates design pattern consistency

2. **Security & Dependencies**
   - Finds security vulnerabilities
   - Identifies outdated or risky dependencies
   - Detects hardcoded secrets and credentials
   - Analyzes access control patterns

3. **Architecture & Design**
   - Maps component relationships and dependencies
   - Identifies architectural anti-patterns
   - Evaluates separation of concerns
   - Assesses scalability patterns

4. **Testing & Quality Standards**
   - Measures test coverage
   - Evaluates test quality and effectiveness
   - Checks compliance with org standards
   - Identifies untested critical paths

5. **Technical Debt & Maintainability**
   - Calculates technical debt score
   - Identifies refactoring opportunities
   - Measures code complexity
   - Tracks code smells

## Language Support

Primary focus on enterprise-grade applications:
- ☕ **Java** (Spring Boot, Jakarta EE, Microservices)
- 🐍 **Python** (Django, Flask, FastAPI)
- ⚛️ **React/TypeScript** (Next.js, React Enterprise Apps)
- **JavaScript/Node.js**
- **Go, C#, and other languages** (extensible)

## Quick Start

### 1. Install Repo360 Power
```bash
# Power is automatically available once installed in Kiro
```

### 2. Clone and Analyze a Repository
Ask Kiro:
```
@repo360 analyze https://github.com/username/repo branch:main
```

### 3. View Metrics
Metrics are generated as JSON reports in the `repo360-output/` directory:
- `metrics-summary.json` - High-level overview
- `quality-metrics.json` - Code quality details
- `security-metrics.json` - Security findings
- `architecture-metrics.json` - Architectural analysis
- `test-metrics.json` - Testing coverage and quality
- `technical-debt.json` - Debt and refactoring opportunities

## Usage Examples

### Basic Analysis
```
Analyze the main branch of https://github.com/company/api-service
```

### Focused Analysis
```
Analyze security issues in https://github.com/company/web-app branch:develop
```

### Compare Branches
```
Compare code quality between main and develop in https://github.com/company/app
```

### Custom Standards
```
Analyze https://github.com/company/service using our coding standards from .repo360/standards.yml
```

## Output Metrics

### Metrics Summary Structure
```json
{
  "repository": "...",
  "branch": "...",
  "analyzed_at": "...",
  "total_files": 0,
  "total_lines": 0,
  "languages": {},
  "overall_score": 0,
  "quality_score": 0,
  "security_score": 0,
  "maintainability_score": 0,
  "test_coverage": 0,
  "critical_issues": 0,
  "warnings": 0
}
```

## Configuration

Create `.repo360/config.yml` in your repository:

```yaml
analysis:
  languages:
    - java
    - python
    - typescript
  exclude_patterns:
    - "**/node_modules/**"
    - "**/target/**"
    - "**/build/**"
    - "**/__pycache__/**"
  
quality_thresholds:
  min_score: 70
  max_complexity: 15
  max_file_length: 500

security:
  check_dependencies: true
  check_secrets: true
  fail_on_critical: true

testing:
  min_coverage: 80
  require_integration_tests: true
```

## Available Agents

### 1. repo360-analyzer
Main analysis agent that orchestrates complete repository analysis.

### 2. repo360-quality-checker
Specialized agent for code quality and maintainability analysis.

### 3. repo360-security-scanner
Specialized agent for security vulnerability detection.

### 4. repo360-architect
Specialized agent for architectural analysis and design patterns.

## Workflows

1. **Complete Repository Scan** - Full analysis of all aspects
2. **Quick Health Check** - Fast overview of repository health
3. **Security Audit** - Focused security and dependency analysis
4. **Quality Review** - Code quality and maintainability focus
5. **Architecture Review** - Architectural patterns and design analysis

## Keywords

repo360, repository analysis, code quality, security scanning, technical debt, code metrics, static analysis, architectural review, test coverage, dependency analysis, enterprise code analysis, ai code detection, code maintainability, github analysis
