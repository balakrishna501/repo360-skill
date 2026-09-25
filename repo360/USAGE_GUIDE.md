# Repo360 Usage Guide

Complete guide for using Repo360 to analyze code repositories.

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Understanding the Dashboard](#understanding-the-dashboard)
4. [Command-Line Options](#command-line-options)
5. [Output Files](#output-files)
6. [For Project Managers](#for-project-managers)
7. [For Developers](#for-developers)
8. [CI/CD Integration](#cicd-integration)
9. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- Git 2.0 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd repo360
pip install -r requirements.txt
```

This installs:
- `gitpython` - Git operations
- `radon` - Python complexity metrics
- `javalang` - Java parsing
- `esprima` - JavaScript parsing
- Other analysis libraries

### Step 2: Verify Installation

```bash
python run.py --help
```

You should see the help message.

## Basic Usage

### Analyze a Public Repository

```bash
python run.py --repo https://github.com/spring-projects/spring-petclinic
```

### Analyze a Specific Branch

```bash
python run.py --repo https://github.com/django/django --branch stable/4.2.x
```

### Faster Analysis (Shallow Clone)

```bash
python run.py --repo https://github.com/torvalds/linux --shallow
```

### Custom Output Directory

```bash
python run.py --repo https://github.com/facebook/react --output react-analysis
```

### Skip Test Files

```bash
python run.py --repo https://github.com/user/repo --skip-tests
```

## Understanding the Dashboard

After analysis, open `output/dashboard.html` in your browser.

### Main Sections

#### 1. Score Cards (Top)

**Overall Score** (0-100)
- Weighted average of all metrics
- Quick health indicator
- Color-coded: Green (good), Yellow (fair), Red (poor)

**Quality Score**
- Code maintainability
- Complexity levels
- Code structure

**Security Score**
- Vulnerabilities found
- Secrets detected
- Risk assessment

**Complexity Score**
- Average cyclomatic complexity
- Distribution across codebase

#### 2. Statistics Bar

- **Source Files**: Total files analyzed
- **Critical Issues**: Must-fix problems
- **High Issues**: Important fixes
- **Medium Issues**: Should address

#### 3. Language Distribution

Visual bar chart showing:
- Languages detected
- File counts
- Percentage breakdown
- Color-coded by language

#### 4. Critical Issues

Red-highlighted must-fix problems:
- SQL injection risks
- Hardcoded secrets
- Security vulnerabilities
- Severe code quality issues

Each issue shows:
- **Type**: Category of issue
- **Message**: What's wrong
- **Location**: File and line number

#### 5. High Priority Issues

Orange-highlighted important fixes:
- High complexity functions
- Design problems
- Moderate security risks

#### 6. Security Scan

Summary of security findings:
- Secrets found (API keys, passwords)
- Vulnerabilities by type
- Severity breakdown

#### 7. Metrics Summary

Technical metrics:
- **Avg Complexity**: Should be < 10
- **Maintainability Index**: Higher is better (aim for > 65)
- **Technical Debt**: Hours and cost estimate

## Command-Line Options

```bash
python run.py [OPTIONS]

Required:
  --repo URL              GitHub repository URL

Optional:
  --branch NAME           Branch to analyze (default: main)
  --output DIR            Output directory (default: output)
  --shallow               Shallow clone for speed
  --skip-tests            Skip test file analysis
```

## Output Files

After analysis, find these in the output directory:

### dashboard.html
**For project managers and stakeholders**
- Beautiful interactive visualization
- All metrics in one place
- Shareable, printable
- Works offline

**Open in any browser:**
```bash
# Windows
start output/dashboard.html

# Mac
open output/dashboard.html

# Linux
xdg-open output/dashboard.html
```

### metrics.json
**Complete analysis data**
```json
{
  "repository": { ... },
  "statistics": { ... },
  "scores": { ... },
  "files": [ ... ],
  "metrics": { ... },
  "security": { ... }
}
```

**For:** Integration, automation, custom tooling

### summary.json
**Executive summary**
```json
{
  "overall_score": 78.5,
  "health_status": "good",
  "critical_issues": 3,
  "technical_debt": {
    "total_hours": 234.5,
    "total_cost_usd": 23450.00
  }
}
```

**For:** Dashboards, reporting, trend tracking

### issues.json
**All detected issues**
```json
{
  "total_issues": 156,
  "by_severity": {
    "critical": [ ... ],
    "high": [ ... ],
    "medium": [ ... ],
    "low": [ ... ]
  }
}
```

**For:** Issue tracking, prioritization

## For Project Managers

### Quick Health Check

1. Run analysis:
   ```bash
   python run.py --repo YOUR_REPO_URL
   ```

2. Open `output/dashboard.html`

3. Look at **Overall Score**:
   - **90-100**: ✅ Excellent - Ship it!
   - **75-89**: ✅ Good - Minor fixes
   - **60-74**: ⚠️ Fair - Schedule refactoring
   - **40-59**: ❌ Poor - Needs work
   - **0-39**: 🚨 Critical - Don't ship

### Weekly Reports

Run analysis every week and compare scores:

```bash
# Monday analysis
python run.py --repo YOUR_REPO --output reports/week-$(date +%Y%W)
```

Track trends:
- Is quality improving?
- Are critical issues decreasing?
- Is technical debt going up or down?

### Cost Estimation

Technical Debt section shows:
- **Hours**: Estimated time to fix all issues
- **Cost**: Hours × $100/hour (default rate)

Use this for:
- Sprint planning
- Budget allocation
- ROI calculations

### Sharing Reports

Dashboard is a single HTML file:
- Email to stakeholders
- Upload to internal wiki
- Print for meetings
- No dependencies needed

## For Developers

### Before Code Review

```bash
# Analyze your branch
python run.py --repo YOUR_REPO --branch feature/your-branch

# Check critical issues
cat output/issues.json | grep "critical"
```

Fix critical issues before review.

### Continuous Monitoring

```bash
# Daily check
python run.py --repo YOUR_REPO --output daily/$(date +%Y%m%d)
```

### Understanding Metrics

**Cyclomatic Complexity**
- Measures decision points (if, for, while, etc.)
- **1-5**: Simple, easy to test
- **6-10**: Moderate
- **11-20**: Complex, needs refactoring
- **21+**: Very complex, high risk

**Maintainability Index**
- Formula: MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
- **> 85**: Highly maintainable
- **65-85**: Moderately maintainable
- **< 65**: Difficult to maintain

**Technical Debt**
- Estimated effort to fix all issues
- Calculated from:
  - High complexity functions
  - Code quality issues
  - Security vulnerabilities

## CI/CD Integration

### GitHub Actions

```yaml
name: Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install Repo360
        run: |
          pip install -r requirements.txt
      
      - name: Run Analysis
        run: |
          python run.py --repo ${{ github.repository }} --branch ${{ github.ref_name }}
      
      - name: Check Quality Gate
        run: |
          score=$(python -c "import json; print(json.load(open('output/summary.json'))['overall_score'])")
          if [ $score -lt 70 ]; then
            echo "Quality score $score below threshold 70"
            exit 1
          fi
      
      - name: Upload Dashboard
        uses: actions/upload-artifact@v2
        with:
          name: code-analysis
          path: output/dashboard.html
```

### GitLab CI

```yaml
code-analysis:
  stage: test
  script:
    - pip install -r requirements.txt
    - python run.py --repo $CI_PROJECT_URL --branch $CI_COMMIT_REF_NAME
    - |
      score=$(python -c "import json; print(json.load(open('output/summary.json'))['overall_score'])")
      if [ $score -lt 70 ]; then exit 1; fi
  artifacts:
    paths:
      - output/
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Analyze') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python run.py --repo ${env.GIT_URL} --branch ${env.BRANCH_NAME}'
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    def summary = readJSON file: 'output/summary.json'
                    if (summary.overall_score < 70) {
                        error "Quality score below threshold"
                    }
                }
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'output',
                reportFiles: 'dashboard.html',
                reportName: 'Code Analysis'
            ])
        }
    }
}
```

## Troubleshooting

### Problem: "Git not found"

**Solution:**
```bash
# Install Git
# Windows: Download from https://git-scm.com/download/win
# Mac: brew install git
# Linux: sudo apt-get install git
```

### Problem: "Permission denied" (SSH)

**Solution:**
```bash
# Use HTTPS instead
python run.py --repo https://github.com/user/repo

# Or set up SSH keys
ssh-keygen -t ed25519
# Add to GitHub: Settings > SSH keys
```

### Problem: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "Repository too large"

**Solution:**
```bash
# Use shallow clone
python run.py --repo URL --shallow
```

### Problem: "Analysis taking too long"

**Solution:**
```bash
# Skip test files
python run.py --repo URL --skip-tests --shallow
```

### Problem: "Out of memory"

**Solution:**
- Close other applications
- Use shallow clone
- Analyze smaller batches

### Problem: "Can't open dashboard"

**Solution:**
```bash
# Check file exists
ls output/dashboard.html

# Open manually
# Windows: start output\dashboard.html
# Mac: open output/dashboard.html
# Linux: xdg-open output/dashboard.html
```

## Best Practices

### 1. Regular Analysis
Run weekly or after major changes

### 2. Track Trends
Save outputs with timestamps to compare over time

### 3. Fix Critical First
Always address critical issues before other work

### 4. Set Quality Gates
Define minimum scores for your team (e.g., > 75)

### 5. Share Results
Make dashboards visible to entire team

### 6. Incremental Improvement
Don't try to fix everything at once

### 7. Automate
Integrate into CI/CD pipeline

## Examples

### Example 1: Quick Health Check

```bash
python run.py --repo https://github.com/your-org/api-service
open output/dashboard.html
```

**Look for:**
- Overall score
- Critical issues count
- Security vulnerabilities

### Example 2: Pre-Release Analysis

```bash
python run.py --repo https://github.com/your-org/app --branch release/v2.0
python run.py --repo https://github.com/your-org/app --branch main

# Compare scores
diff output-release/summary.json output-main/summary.json
```

### Example 3: Team Report

```bash
# Analyze all microservices
for service in auth api gateway; do
  python run.py --repo https://github.com/org/$service --output reports/$service
done

# Create index page linking to all dashboards
```

## Support

For issues:
1. Check this guide
2. Review error messages
3. Try with a public repo first
4. Check Python and Git versions

---

**Happy analyzing! 🎯**
