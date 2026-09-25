# Generate Metrics Report Skill

## Purpose
Aggregate all analysis results and generate comprehensive JSON reports and human-readable summaries.

## Report Types

### 1. metrics-summary.json
High-level overview of all metrics

### 2. quality-metrics.json
Detailed code quality analysis

### 3. security-metrics.json
Security vulnerabilities and risks

### 4. architecture-metrics.json
Architectural analysis and design

### 5. test-metrics.json
Test coverage and quality

### 6. technical-debt.json
Technical debt quantification

### 7. Executive Summary (Markdown)
Human-readable summary for stakeholders

## Generation Process

### Step 1: Collect All Analysis Data
- Quality analysis results
- Security scan results
- Architecture evaluation
- Test coverage data
- Technical debt calculations

### Step 2: Aggregate Metrics
- Calculate overall scores
- Summarize issues by severity
- Identify top hotspots
- Prioritize recommendations

### Step 3: Generate JSON Reports
- Write individual metric files
- Ensure valid JSON structure
- Include timestamps and metadata

### Step 4: Create Summary Report
- Executive summary
- Key findings
- Critical issues
- Recommendations
- Comparison to benchmarks

## Output Structure

### Directory Layout
```
repo360-output/
├── metrics-summary.json          # Overall summary
├── quality-metrics.json          # Code quality details
├── security-metrics.json         # Security findings
├── architecture-metrics.json     # Architecture analysis
├── test-metrics.json            # Test coverage
├── technical-debt.json          # Debt analysis
├── file-details/                # Per-file metrics
│   ├── src_main_UserService.json
│   └── ...
└── reports/
    ├── executive-summary.md     # High-level summary
    ├── detailed-findings.md     # Complete findings
    └── recommendations.md       # Actionable recommendations
```

### Executive Summary Template
```markdown
# Repo360 Analysis Report

**Repository**: github.com/company/project
**Branch**: main
**Analyzed**: 2024-01-15 10:30:00 UTC

## Overview
- **Overall Score**: 78/100 (Good)
- **Total Files**: 234
- **Total Lines**: 45,678
- **Primary Language**: Java (Spring Boot)

## Health Scores
- Quality: 82/100 ✅
- Security: 68/100 ⚠️
- Architecture: 75/100 ✅
- Test Coverage: 72% ⚠️
- Technical Debt: 234 hours ($23,400)

## Critical Issues (3)
1. SQL Injection in UserDao.java:42
2. Hardcoded AWS credentials in Config.java:15
3. High complexity in PaymentProcessor.processPayment (CC: 24)

## Top Recommendations
1. Fix critical security vulnerabilities (4 hours)
2. Refactor high-complexity methods (12 hours)
3. Increase test coverage on payment logic (8 hours)

## Comparison to Industry Standards
- Quality Score: Above average (industry avg: 70)
- Security Score: Below average (industry avg: 75)
- Test Coverage: Average (industry avg: 75%)
```

## Report Validation

Before finalizing:
1. Validate all JSON syntax
2. Ensure all required fields present
3. Check metric calculations
4. Verify file references
5. Confirm recommendations are actionable

## Distribution

### For Developers
- Detailed JSON metrics
- File-level issues
- Specific code locations
- Fix examples

### For Team Leads
- Summary dashboard data
- Priority recommendations
- Effort estimates
- Trend analysis

### For Executives
- Executive summary (Markdown)
- High-level scores
- Business impact
- ROI of improvements

## Export Formats

### JSON (default)
Machine-readable, API-friendly

### Markdown
Human-readable summaries

### HTML (optional)
Interactive dashboards

### CSV (optional)
Spreadsheet analysis

### PDF (optional)
Formal reports

## Success Criteria

✅ All JSON files valid
✅ All metrics calculated correctly
✅ Issues prioritized appropriately
✅ Recommendations actionable
✅ Reports generated in output directory
✅ No sensitive data exposed
