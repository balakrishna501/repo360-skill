---
title: Getting Started with Repo360
---

# Getting Started with Repo360

This guide will help you quickly get started with Repo360 to analyze your GitHub repositories.

## Quick Start

### 1. Basic Analysis Command

Simply provide a GitHub repository URL:

```
Analyze https://github.com/username/repository
```

Repo360 will:
- Clone the repository
- Detect the programming languages and frameworks
- Perform comprehensive analysis
- Generate metrics reports

### 2. Specify a Branch

```
Analyze https://github.com/username/repository branch:develop
```

### 3. View Results

After analysis completes, check the `repo360-output/` directory:

```
repo360-output/
├── metrics-summary.json          # Start here!
├── quality-metrics.json
├── security-metrics.json
├── architecture-metrics.json
├── test-metrics.json
├── technical-debt.json
└── reports/
    └── executive-summary.md      # Human-readable summary
```

## Understanding Your Results

### Overall Score (0-100)

- **90-100**: Excellent - Production-ready code
- **75-89**: Good - Solid quality, minor improvements needed
- **60-74**: Fair - Needs attention
- **40-59**: Poor - Significant issues
- **0-39**: Critical - Major refactoring required

### Issue Severity

- **Critical**: Must fix immediately (security, data loss)
- **High**: Fix soon (major bugs, vulnerabilities)
- **Medium**: Address in near term (quality issues)
- **Low**: Nice to have (minor improvements)

## Common First Steps

### 1. Address Critical Security Issues

Check `security-metrics.json` for critical vulnerabilities:
- SQL injection
- Hardcoded secrets
- Vulnerable dependencies

### 2. Reduce High Complexity

Check `quality-metrics.json` for functions with complexity > 15.
Break them down into smaller, focused functions.

### 3. Increase Test Coverage

Check `test-metrics.json` for coverage gaps, especially in:
- Payment/financial logic
- Authentication/authorization
- Core business logic

### 4. Resolve Architectural Issues

Check `architecture-metrics.json` for:
- Circular dependencies
- God objects
- Layer violations

## Example Workflow

### Step 1: Initial Scan
```
Analyze https://github.com/mycompany/api-service branch:main
```

### Step 2: Review Summary
```
Open repo360-output/reports/executive-summary.md
```

### Step 3: Prioritize Issues
Focus on:
1. Critical security issues
2. High-complexity functions in critical paths
3. Low test coverage on important features

### Step 4: Fix and Rescan
After making fixes:
```
Analyze https://github.com/mycompany/api-service branch:feature/improvements
```

Compare results to see improvement.

## Tips for Best Results

### 1. Ensure Code Compiles
Analysis works best on code that compiles successfully.

### 2. Include Tests
Make sure your test files are included in the repository.

### 3. Use Standard Structure
Follow standard project layouts for your framework:
- Java: Maven/Gradle standard structure
- Python: Standard package layout
- React: Create React App or Next.js structure

### 4. Keep Dependencies Updated
Outdated dependencies affect security scores significantly.

## Focused Analysis

### Security-Only Scan
```
Run security scan on https://github.com/username/repo
```

### Quality-Only Review
```
Check code quality for https://github.com/username/repo
```

### Architecture Review
```
Review architecture of https://github.com/username/repo
```

## Understanding Metrics

### Quality Score Components
- Code complexity (25%)
- Maintainability (25%)
- Duplication (20%)
- Readability (20%)
- Best practices (10%)

### Security Score Components
- Critical vulnerabilities: -20 points each
- High vulnerabilities: -10 points each
- Medium vulnerabilities: -5 points each
- Low vulnerabilities: -1 point each

### Architecture Score Components
- Pattern adherence (25%)
- Dependency health (25%)
- SOLID compliance (20%)
- Modularity (15%)
- Scalability (15%)

## Next Steps

1. **Read Executive Summary**: Start with high-level overview
2. **Fix Critical Issues**: Address security and major bugs
3. **Reduce Complexity**: Refactor complex functions
4. **Improve Tests**: Increase coverage on critical paths
5. **Refactor Architecture**: Address structural issues
6. **Monitor Progress**: Re-run analysis periodically

## Getting Help

### Common Questions

**Q: Why is my score low?**
A: Check the detailed metrics JSONs for specific issues. Common reasons: high complexity, security issues, low test coverage.

**Q: How often should I analyze?**
A: Before major releases, after significant changes, or weekly for active projects.

**Q: Can I customize the analysis?**
A: Yes! Create `.repo360/config.yml` in your repository. See "Custom Rules" steering guide.

**Q: What languages are supported?**
A: Primary: Java, Python, React/TypeScript. Also: JavaScript, Go, C#, and more.

## Support

For issues or questions:
- Check detailed metric files
- Review specific file issues in `file-details/`
- Consult framework-specific documentation
