---
title: Enterprise Setup Guide
---

# Enterprise Setup Guide

Configure Repo360 for large-scale enterprise use with custom standards, CI/CD integration, and team workflows.

## Enterprise Configuration

### Organization-Wide Standards

Create `.repo360/standards/` directory with your organization's coding standards:

```yaml
# .repo360/standards/quality.yml
quality:
  max_complexity: 10
  max_function_length: 50
  max_class_length: 300
  min_maintainability: 70
  
naming_conventions:
  java:
    classes: PascalCase
    methods: camelCase
    constants: UPPER_SNAKE_CASE
  python:
    classes: PascalCase
    functions: snake_case
    constants: UPPER_SNAKE_CASE

code_style:
  java: google-java-format
  python: black
  javascript: prettier
```

```yaml
# .repo360/standards/security.yml
security:
  fail_on_critical: true
  fail_on_high: true
  allowed_licenses:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
  
  forbidden_patterns:
    - type: hardcoded_password
      severity: critical
    - type: sql_injection
      severity: critical
  
  required_headers:
    - Content-Security-Policy
    - X-Frame-Options
    - X-Content-Type-Options
```

```yaml
# .repo360/standards/architecture.yml
architecture:
  required_layers:
    - presentation
    - business
    - data
  
  forbidden_dependencies:
    - from: data
      to: presentation
    - from: data
      to: business
  
  max_dependencies_per_class: 7
  max_circular_dependencies: 0
  min_abstractness: 0.2
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/repo360-analysis.yml
name: Repo360 Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Repo360 Analysis
        run: |
          # Install Kiro with Repo360 power
          curl -fsSL https://kiro.dev/install.sh | sh
          kiro power install repo360
          
          # Run analysis
          kiro analyze-repo . --output json
      
      - name: Check Quality Gates
        run: |
          # Fail if quality score < 70
          score=$(jq .overall_score repo360-output/metrics-summary.json)
          if [ $score -lt 70 ]; then
            echo "Quality score $score below threshold 70"
            exit 1
          fi
      
      - name: Check Security
        run: |
          # Fail if critical security issues found
          critical=$(jq .summary.critical_issues repo360-output/security-metrics.json)
          if [ $critical -gt 0 ]; then
            echo "$critical critical security issues found"
            exit 1
          fi
      
      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: repo360-reports
          path: repo360-output/
```

### GitLab CI

```yaml
# .gitlab-ci.yml
repo360-analysis:
  stage: test
  script:
    - curl -fsSL https://kiro.dev/install.sh | sh
    - kiro power install repo360
    - kiro analyze-repo . --output json
    - |
      score=$(jq .overall_score repo360-output/metrics-summary.json)
      if [ $score -lt 70 ]; then
        exit 1
      fi
  artifacts:
    paths:
      - repo360-output/
    expire_in: 30 days
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Repo360 Analysis') {
            steps {
                sh 'curl -fsSL https://kiro.dev/install.sh | sh'
                sh 'kiro power install repo360'
                sh 'kiro analyze-repo . --output json'
            }
        }
        
        stage('Quality Gates') {
            steps {
                script {
                    def summary = readJSON file: 'repo360-output/metrics-summary.json'
                    if (summary.overall_score < 70) {
                        error "Quality score ${summary.overall_score} below threshold"
                    }
                }
            }
        }
        
        stage('Publish Reports') {
            steps {
                publishHTML([
                    reportDir: 'repo360-output/reports',
                    reportFiles: 'executive-summary.md',
                    reportName: 'Repo360 Report'
                ])
            }
        }
    }
}
```

## Quality Gates

### Define Thresholds

```yaml
# .repo360/quality-gates.yml
gates:
  overall_score:
    min: 70
    blocking: true
  
  security:
    max_critical: 0
    max_high: 5
    blocking: true
  
  quality:
    min_score: 70
    max_complexity: 15
    max_duplication: 5
    blocking: false
  
  test_coverage:
    min_line_coverage: 80
    min_branch_coverage: 75
    blocking: false
  
  technical_debt:
    max_hours: 500
    max_critical_issues: 10
    blocking: false
```

### Enforcement in CI

```bash
#!/bin/bash
# check-quality-gates.sh

set -e

SUMMARY="repo360-output/metrics-summary.json"
GATES=".repo360/quality-gates.yml"

# Parse thresholds (simplified - use proper YAML parser in production)
MIN_SCORE=$(grep "min:" $GATES | head -1 | awk '{print $2}')
score=$(jq .overall_score $SUMMARY)

if [ $score -lt $MIN_SCORE ]; then
  echo "❌ Quality gate failed: Score $score < $MIN_SCORE"
  exit 1
fi

echo "✅ All quality gates passed"
```

## Team Workflows

### 1. Pre-Commit Analysis (Fast Check)

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Quick analysis on changed files only

changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(java|py|ts|tsx)$')

if [ -n "$changed_files" ]; then
  kiro analyze-files $changed_files --quick
fi
```

### 2. Pull Request Review

```markdown
## Repo360 PR Analysis

**Branch**: feature/new-api
**Quality Score**: 82/100 (+3 from main)
**New Issues**: 2 medium, 1 low
**Fixed Issues**: 1 high complexity

### Summary
- ✅ No new security issues
- ✅ Test coverage maintained at 85%
- ⚠️ One new function with complexity 12 (threshold: 10)

### Recommendations
1. Refactor `ApiHandler.processRequest()` to reduce complexity
2. Add integration test for new endpoint
```

### 3. Scheduled Analysis

```bash
# Daily analysis cron job
0 2 * * * cd /path/to/repo && kiro analyze-repo . --branch main --save-history
```

## Multi-Repository Management

### Organization Dashboard

```python
# aggregate-metrics.py
import json
import os

repos = [
    'api-service',
    'web-app',
    'mobile-backend',
    'data-pipeline'
]

dashboard = {
    'organization': 'MyCompany',
    'analyzed_at': datetime.now().isoformat(),
    'repositories': []
}

for repo in repos:
    summary_path = f'{repo}/repo360-output/metrics-summary.json'
    with open(summary_path) as f:
        data = json.load(f)
        dashboard['repositories'].append({
            'name': repo,
            'score': data['overall_score'],
            'critical_issues': data['issue_summary']['critical'],
            'test_coverage': data['scores']['test_coverage']
        })

# Generate organization report
with open('organization-dashboard.json', 'w') as f:
    json.dump(dashboard, f, indent=2)
```

## Custom Reporting

### Executive Dashboard API

```python
# dashboard-api.py
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/dashboard')
def dashboard():
    with open('repo360-output/metrics-summary.json') as f:
        data = json.load(f)
    
    return jsonify({
        'health': 'good' if data['overall_score'] > 75 else 'needs_attention',
        'score': data['overall_score'],
        'critical_issues': data['issue_summary']['critical'],
        'trends': get_historical_trends()
    })

@app.route('/api/security')
def security():
    with open('repo360-output/security-metrics.json') as f:
        return jsonify(json.load(f))
```

## Compliance Reporting

### Generate Compliance Reports

```yaml
# .repo360/compliance.yml
compliance:
  standards:
    - PCI-DSS
    - SOC2
    - GDPR
    - HIPAA
  
  requirements:
    pci_dss:
      - no_hardcoded_credentials
      - encryption_at_rest
      - secure_logging
      - access_control
    
    soc2:
      - code_review_required
      - automated_testing
      - security_scanning
      - change_management
```

## Best Practices

### 1. Start Small
- Begin with one critical repository
- Establish baseline metrics
- Set achievable improvement targets

### 2. Automate Everything
- CI/CD integration for every PR
- Scheduled scans
- Automated reporting

### 3. Track Progress
- Store historical metrics
- Track trends over time
- Celebrate improvements

### 4. Foster Ownership
- Share reports with teams
- Make metrics visible
- Reward quality improvements

### 5. Continuous Improvement
- Review thresholds quarterly
- Update standards as needed
- Learn from patterns

## Troubleshooting

### Large Repositories
```yaml
# .repo360/config.yml
performance:
  parallel_analysis: true
  max_threads: 8
  cache_enabled: true
  incremental_analysis: true  # Only analyze changed files
```

### Private Dependencies
```yaml
# .repo360/config.yml
dependencies:
  private_registries:
    - url: https://npm.internal.company.com
      token: ${NPM_TOKEN}
    - url: https://maven.internal.company.com
      credentials: ${MAVEN_CREDS}
```

### Custom Rules
See "Custom Rules" steering guide for detailed rule configuration.
