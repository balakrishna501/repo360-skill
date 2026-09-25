---
title: Custom Rules and Configuration
---

# Custom Rules and Configuration

Customize Repo360 analysis to match your organization's specific coding standards, patterns, and requirements.

## Configuration File

Create `.repo360/config.yml` in your repository root:

```yaml
# .repo360/config.yml
version: "1.0"

# Analysis scope
analysis:
  languages:
    - java
    - python
    - typescript
    - javascript
  
  # Paths to include
  include_patterns:
    - "src/**/*"
    - "lib/**/*"
  
  # Paths to exclude
  exclude_patterns:
    - "**/node_modules/**"
    - "**/target/**"
    - "**/build/**"
    - "**/__pycache__/**"
    - "**/dist/**"
    - "**/.git/**"
    - "**/vendor/**"

# Quality thresholds
quality:
  min_overall_score: 70
  max_complexity: 10
  max_function_length: 50
  max_class_length: 500
  max_file_length: 1000
  max_parameters: 5
  min_maintainability: 65
  max_duplication_percentage: 5

# Security configuration
security:
  enabled: true
  fail_on_critical: true
  fail_on_high: false
  
  # Secret detection patterns
  custom_secret_patterns:
    - name: "Internal API Key"
      pattern: "INTERNAL_API_[A-Za-z0-9]{32}"
      severity: critical
    - name: "Service Token"
      pattern: "svc_token_[a-f0-9]{40}"
      severity: high
  
  # Allowed dependency licenses
  allowed_licenses:
    - MIT
    - Apache-2.0
    - BSD-2-Clause
    - BSD-3-Clause
    - ISC
  
  # Forbidden dependencies
  forbidden_dependencies:
    - name: "lodash"
      reason: "Use native ES6+ features instead"
    - name: "request"
      reason: "Deprecated, use axios or node-fetch"

# Architecture rules
architecture:
  style: "layered"
  
  required_layers:
    - name: "presentation"
      patterns: ["**/controller/**", "**/api/**", "**/routes/**"]
    - name: "business"
      patterns: ["**/service/**", "**/business/**"]
    - name: "data"
      patterns: ["**/repository/**", "**/dao/**", "**/models/**"]
  
  # Forbidden dependency directions
  forbidden_dependencies:
    - from_layer: "data"
      to_layer: "presentation"
      severity: critical
    - from_layer: "data"
      to_layer: "business"
      severity: high
  
  # Circular dependency tolerance
  max_circular_dependencies: 0

# Testing requirements
testing:
  min_line_coverage: 80
  min_branch_coverage: 70
  min_function_coverage: 85
  
  require_tests_for:
    - pattern: "**/service/**"
      reason: "All business logic must be tested"
    - pattern: "**/controller/**"
      reason: "All API endpoints must be tested"
  
  critical_paths:
    - pattern: "**/*Payment*"
      min_coverage: 95
    - pattern: "**/*Auth*"
      min_coverage: 90
    - pattern: "**/*Security*"
      min_coverage: 90

# Custom rules
custom_rules:
  java:
    - id: "no-system-out"
      pattern: "System\\.out\\.print"
      message: "Use logging framework instead of System.out"
      severity: medium
    
    - id: "require-logger"
      pattern: "class .* \\{"
      requires: "private static final Logger"
      message: "All classes should have a logger"
      severity: low
  
  python:
    - id: "no-print-statements"
      pattern: "^\\s*print\\("
      message: "Use logging module instead of print()"
      severity: medium
      exclude_patterns:
        - "**/scripts/**"
        - "**/__main__.py"
    
    - id: "require-type-hints"
      pattern: "def \\w+\\([^)]*\\):"
      requires: "def \\w+\\([^)]*\\) -> "
      message: "Functions should have type hints"
      severity: low
  
  typescript:
    - id: "no-any-type"
      pattern: ":\\s*any\\b"
      message: "Avoid using 'any' type, use specific types"
      severity: medium
    
    - id: "prefer-const"
      pattern: "^\\s*let\\s+\\w+\\s*="
      message: "Use 'const' instead of 'let' when possible"
      severity: low

# Naming conventions
naming:
  java:
    classes: "^[A-Z][a-zA-Z0-9]*$"
    interfaces: "^I[A-Z][a-zA-Z0-9]*$"
    methods: "^[a-z][a-zA-Z0-9]*$"
    constants: "^[A-Z][A-Z0-9_]*$"
  
  python:
    classes: "^[A-Z][a-zA-Z0-9]*$"
    functions: "^[a-z][a-z0-9_]*$"
    constants: "^[A-Z][A-Z0-9_]*$"
  
  typescript:
    interfaces: "^I[A-Z][a-zA-Z0-9]*$"
    types: "^[A-Z][a-zA-Z0-9]*$"
    functions: "^[a-z][a-zA-Z0-9]*$"
    constants: "^[A-Z][A-Z0-9_]*$"

# Documentation requirements
documentation:
  require_file_headers: true
  require_class_docs: true
  require_function_docs_for_public: true
  min_comment_ratio: 10  # percentage

# Technical debt
technical_debt:
  hourly_rate: 100  # USD per hour
  debt_ratio_threshold: 5  # percentage
  
  # Custom effort estimates
  effort_estimates:
    high_complexity: 2  # hours
    code_smell: 0.5
    duplication: 0.25
    security_high: 4
    security_critical: 8

# Reporting
reporting:
  output_formats:
    - json
    - markdown
    - html
  
  include_file_details: true
  include_history: true
  
  # Comparison baseline
  baseline:
    branch: "main"
    compare_on_pr: true

# Integrations
integrations:
  # Slack notifications
  slack:
    enabled: false
    webhook_url: "${SLACK_WEBHOOK_URL}"
    notify_on:
      - critical_issues
      - score_drop
  
  # JIRA issue creation
  jira:
    enabled: false
    url: "${JIRA_URL}"
    project: "TECH-DEBT"
    create_issues_for:
      - critical
      - high
```

## Language-Specific Rules

### Java Custom Rules

```yaml
# .repo360/rules/java-custom.yml
rules:
  - id: "spring-service-naming"
    pattern: "@Service\\s+public\\s+class\\s+(\\w+)"
    requires: "Service$"
    message: "Service classes should end with 'Service'"
    severity: low
  
  - id: "no-field-injection"
    pattern: "@Autowired\\s+private"
    message: "Use constructor injection instead of field injection"
    severity: medium
  
  - id: "transactional-on-service"
    class_annotation: "@Service"
    method_pattern: "public.*save|update|delete"
    requires: "@Transactional"
    message: "Data-modifying service methods should be @Transactional"
    severity: high
```

### Python Custom Rules

```yaml
# .repo360/rules/python-custom.yml
rules:
  - id: "django-view-docstring"
    pattern: "class.*View\\(.*\\):"
    requires: '""".*"""'
    message: "Django views should have docstrings"
    severity: low
  
  - id: "no-bare-except"
    pattern: "except:\\s*$"
    message: "Catch specific exceptions, not bare except"
    severity: high
  
  - id: "use-pathlib"
    pattern: "import os\\.path"
    message: "Use pathlib instead of os.path"
    severity: low
```

### TypeScript Custom Rules

```yaml
# .repo360/rules/typescript-custom.yml
rules:
  - id: "react-component-naming"
    pattern: "export (default )?function (\\w+)"
    file_pattern: "src/components/**/*.tsx"
    requires: "^[A-Z]"
    message: "React components should start with capital letter"
    severity: medium
  
  - id: "no-anonymous-export"
    pattern: "export default \\("
    message: "Avoid anonymous default exports"
    severity: low
  
  - id: "use-strict-equality"
    pattern: "[^=!]==[^=]"
    message: "Use === instead of =="
    severity: medium
```

## Pattern-Based Rules

### Detect Anti-Patterns

```yaml
anti_patterns:
  - name: "god-class"
    conditions:
      - methods > 20
      - lines > 500
      - dependencies > 10
    severity: critical
    message: "Class is too large and has too many responsibilities"
  
  - name: "anemic-model"
    conditions:
      - type: "entity"
      - methods < 2
      - fields > 5
    severity: medium
    message: "Domain model lacks behavior"
  
  - name: "feature-envy"
    conditions:
      - external_method_calls > internal_method_calls
    severity: medium
    message: "Method uses another class more than its own"
```

### Enforce Design Patterns

```yaml
required_patterns:
  - name: "repository-pattern"
    when:
      file_pattern: "**/repository/**"
    requires:
      - interface_exists: true
      - methods_match: "find.*|save.*|delete.*"
    severity: medium
  
  - name: "factory-pattern"
    when:
      class_name: ".*Factory"
    requires:
      - method_exists: "create.*"
      - returns_interface: true
    severity: low
```

## Environment-Specific Configuration

### Development Environment

```yaml
# .repo360/config.dev.yml
quality:
  min_overall_score: 60  # Relaxed for dev
  max_complexity: 15

testing:
  min_line_coverage: 60
  
custom_rules:
  # Disable strict rules in dev
  java:
    - id: "no-system-out"
      enabled: false
```

### Production Environment

```yaml
# .repo360/config.prod.yml
quality:
  min_overall_score: 85  # Strict for prod
  max_complexity: 8

security:
  fail_on_critical: true
  fail_on_high: true

testing:
  min_line_coverage: 90
```

## Load Configuration

```bash
# Use specific config
kiro analyze-repo . --config .repo360/config.prod.yml

# Use environment-specific config
kiro analyze-repo . --env production
```

## Rule Testing

Test your custom rules before deploying:

```bash
# Test rule on sample code
kiro test-rule --rule-file .repo360/rules/java-custom.yml \
              --test-file samples/TestClass.java \
              --expect-issues 2
```

## Best Practices

1. **Start Conservative**: Begin with lenient thresholds, tighten gradually
2. **Document Rules**: Add clear messages explaining why rules exist
3. **Test Rules**: Verify rules work as expected before enforcing
4. **Version Control**: Keep configuration in Git
5. **Environment-Specific**: Different configs for dev/staging/prod
6. **Team Consensus**: Agree on rules as a team
7. **Regular Review**: Update rules based on learnings

## Sharing Rules

### Organization Template

Create a shared template repository:

```
org-repo360-config/
├── config.yml                 # Base config
├── rules/
│   ├── java-rules.yml
│   ├── python-rules.yml
│   └── typescript-rules.yml
└── README.md
```

Teams can then import:

```yaml
# .repo360/config.yml
extends: "https://github.com/myorg/repo360-config/config.yml"

# Override specific values
quality:
  min_overall_score: 75  # Team-specific threshold
```
