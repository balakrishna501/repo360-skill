# Measure Test Coverage Skill

## Purpose
Analyze test quality and coverage across unit, integration, and end-to-end tests.

## Capabilities

### 1. Coverage Metrics
- **Line Coverage**: Percentage of executed lines
- **Branch Coverage**: Percentage of executed branches
- **Function Coverage**: Percentage of called functions
- **Statement Coverage**: Percentage of executed statements

### 2. Test Types Distribution
- Unit tests (isolated component testing)
- Integration tests (component interaction)
- End-to-end tests (full user flows)
- Snapshot tests
- Performance tests

### 3. Test Quality Assessment
- Assertions per test
- Test complexity
- Mock usage patterns
- Test maintainability
- Test execution time

### 4. Critical Path Analysis
Identify untested critical code:
- Payment processing
- Authentication/authorization
- Data persistence
- External API calls
- Security-sensitive functions

## Language-Specific Tools

### Java
```bash
# JUnit + JaCoCo
mvn test jacoco:report

# Coverage output
target/site/jacoco/jacoco.xml
```

### Python
```bash
# pytest + coverage.py
pytest --cov=app --cov-report=json

# Coverage output
coverage.json
```

### JavaScript/TypeScript
```bash
# Jest
jest --coverage --coverageReporters=json

# Coverage output
coverage/coverage-final.json
```

## Coverage Analysis

### Good Coverage (>80%)
- Indicates well-tested codebase
- Reduces bug risk
- Enables confident refactoring

### Poor Coverage (<60%)
- High bug risk
- Difficult maintenance
- Risky refactoring

### Critical Uncovered Code
Priority areas requiring tests:
1. Payment/financial logic
2. Authentication/authorization
3. Data validation
4. Security functions
5. Core business logic

## Output
```json
{
  "coverage_score": 78,
  "line_coverage": 82,
  "branch_coverage": 75,
  "function_coverage": 88,
  "test_distribution": {
    "unit": 234,
    "integration": 67,
    "e2e": 23
  },
  "uncovered_critical": [
    {
      "file": "PaymentProcessor.java",
      "function": "processPayment",
      "criticality": "high",
      "reason": "Handles financial transactions"
    }
  ]
}
```

## Best Practices

1. Aim for 80%+ coverage on business logic
2. 100% coverage on critical paths
3. Focus on branch coverage, not just line coverage
4. Write meaningful assertions
5. Avoid testing implementation details
6. Keep tests maintainable and readable
