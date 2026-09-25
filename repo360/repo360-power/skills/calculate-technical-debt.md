# Calculate Technical Debt Skill

## Purpose
Quantify technical debt by identifying code smells, outdated dependencies, complexity issues, and estimating remediation effort.

## Debt Categories

### 1. Code Smells (40%)
- Long methods/functions
- Large classes (God objects)
- Duplicate code
- Dead code
- Magic numbers/strings
- Complex conditionals

### 2. Complexity (25%)
- High cyclomatic complexity
- Deep nesting
- Long parameter lists
- Cognitive complexity

### 3. Outdated Dependencies (20%)
- Unmaintained packages
- Security vulnerabilities
- Version lag behind latest stable

### 4. Documentation (10%)
- Missing documentation
- Outdated comments
- Lack of architectural docs

### 5. Test Debt (5%)
- Low test coverage
- Flaky tests
- Missing integration tests

## Debt Calculation

### Formula
```
Total Debt (hours) = 
  Code Smell Count × 0.5 hours +
  Complexity Issues × 1 hour +
  Duplicate Blocks × 0.25 hours +
  Outdated Deps × 2 hours +
  Coverage Gap % × 50 hours
```

### Cost Calculation
```
Total Cost = Total Hours × Hourly Rate ($100/hour default)
```

### Debt Score (0-100)
```
Debt Score = 100 - (Total Debt Hours / Ideal Hours × 100)
Where Ideal Hours = Total LOC / 1000
```

## Hotspot Identification

Files with highest debt:
1. Large files with multiple issues
2. High-complexity, low-coverage files
3. Files with many code smells
4. Security-vulnerable files

## Priority Calculation

### Critical Priority
- Security vulnerabilities
- High complexity in critical paths
- Untested payment/auth logic

### High Priority
- God objects
- Circular dependencies
- Major duplication

### Medium Priority
- Moderate complexity
- Minor duplication
- Missing documentation

### Low Priority
- Code style issues
- Minor refactoring opportunities
- Documentation improvements

## Output
```json
{
  "debt_score": 72,
  "total_debt_hours": 234,
  "total_debt_cost": 23400,
  "breakdown": {
    "code_smells": {"count": 156, "hours": 78},
    "complexity": {"count": 45, "hours": 45},
    "duplication": {"count": 32, "hours": 8},
    "outdated_deps": {"count": 12, "hours": 24},
    "test_debt": {"hours": 79}
  },
  "hotspots": [
    {
      "file": "ApplicationService.java",
      "debt_hours": 12,
      "issues": ["god_object", "high_complexity", "low_coverage"],
      "priority": "critical"
    }
  ],
  "recommendations": [
    {
      "priority": "critical",
      "category": "complexity",
      "description": "Refactor ApplicationService.processPayment (complexity: 24)",
      "effort_hours": 4,
      "impact": "high"
    }
  ]
}
```

## Remediation Strategies

### Quick Wins (Low effort, High impact)
- Remove dead code
- Extract magic numbers to constants
- Add missing documentation

### High Impact (Medium effort, High impact)
- Break up god objects
- Resolve circular dependencies
- Update critical vulnerable deps

### Long-term (High effort, High impact)
- Architectural refactoring
- Comprehensive test coverage
- Major version upgrades

## Tracking Over Time

Compare debt metrics across commits/branches:
- Debt trend (increasing/decreasing)
- New debt introduced
- Debt paid down
- ROI of refactoring efforts
