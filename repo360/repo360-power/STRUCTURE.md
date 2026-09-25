# Repo360 Power Structure

This document explains the complete folder structure and organization of the Repo360 Power.

## Directory Structure

```
repo360-power/
├── POWER.md                          # Main power documentation
├── power.json                        # Power configuration and metadata
├── README.md                         # User-facing overview
├── INSTALL.md                        # Installation guide
├── STRUCTURE.md                      # This file
├── LICENSE                           # License information
│
├── agents/                           # Specialized AI agents
│   ├── repo360-analyzer.md           # Main orchestrator agent
│   ├── repo360-quality-checker.md    # Code quality specialist
│   ├── repo360-security-scanner.md   # Security vulnerability specialist
│   └── repo360-architect.md          # Architecture analysis specialist
│
├── skills/                           # Reusable capabilities
│   ├── clone-repository.md           # Repository cloning
│   ├── analyze-java-code.md          # Java analysis
│   ├── analyze-python-code.md        # Python analysis
│   ├── analyze-react-code.md         # React/TypeScript analysis
│   ├── detect-security-issues.md     # Security scanning
│   ├── analyze-architecture.md       # Architecture evaluation
│   ├── measure-test-coverage.md      # Test coverage measurement
│   ├── calculate-technical-debt.md   # Technical debt calculation
│   └── generate-metrics-report.md    # Report generation
│
├── steering/                         # Workflow guides
│   ├── getting-started.md            # Quick start guide
│   ├── enterprise-setup.md           # Enterprise deployment
│   └── custom-rules.md               # Custom configuration
│
├── examples/                         # Example files
│   ├── config.example.yml            # Example configuration
│   ├── java-project/                 # Sample Java analysis
│   ├── python-project/               # Sample Python analysis
│   └── react-project/                # Sample React analysis
│
├── schemas/                          # JSON schemas
│   ├── metrics-summary.schema.json
│   ├── quality-metrics.schema.json
│   ├── security-metrics.schema.json
│   ├── architecture-metrics.schema.json
│   ├── test-metrics.schema.json
│   └── technical-debt.schema.json
│
└── docs/                            # Additional documentation
    ├── architecture.md              # System architecture
    ├── metrics-explained.md         # Metric definitions
    ├── scoring-algorithm.md         # Scoring methodology
    └── api-reference.md             # API documentation
```

## Component Descriptions

### Root Level Files

#### POWER.md
The main documentation file that describes:
- Power overview and capabilities
- Problem statement and solution
- Language support
- Usage examples
- Output structure
- Keywords for discovery

#### power.json
Configuration file that defines:
- Power metadata (name, version, description)
- Agent references
- Skill references
- Steering file references
- Keywords for power discovery

#### README.md
User-facing documentation:
- Quick start guide
- Feature overview
- Example usage
- Installation instructions
- Architecture diagram
- Use cases

#### INSTALL.md
Complete installation guide:
- Prerequisites
- Installation steps
- Configuration
- Troubleshooting
- Verification

### Agents Directory

Contains specialized AI agents, each with a specific focus:

#### repo360-analyzer.md
**Role**: Main orchestrator
- Coordinates entire analysis workflow
- Manages repository cloning
- Delegates to specialized agents
- Aggregates results
- Generates final reports

**Workflow**:
1. Clone repository
2. Discover structure
3. Delegate to specialists
4. Aggregate results
5. Generate reports

#### repo360-quality-checker.md
**Role**: Code quality specialist
- Complexity analysis
- Code smell detection
- Duplication identification
- Maintainability scoring
- Best practices verification

**Focus Areas**:
- Cyclomatic complexity
- Cognitive complexity
- Code duplication
- Naming conventions
- Code smells

#### repo360-security-scanner.md
**Role**: Security specialist
- Vulnerability detection
- Dependency scanning
- Secret detection
- Cryptography checks
- OWASP Top 10 coverage

**Focus Areas**:
- Injection vulnerabilities
- Authentication issues
- Cryptographic failures
- Hardcoded secrets
- Vulnerable dependencies

#### repo360-architect.md
**Role**: Architecture specialist
- Design pattern detection
- Dependency analysis
- SOLID principles
- Architectural metrics
- Structural quality

**Focus Areas**:
- Architecture patterns
- Component relationships
- Circular dependencies
- Coupling and cohesion
- Design patterns

### Skills Directory

Reusable capabilities that agents can use:

#### clone-repository.md
- Clone GitHub repositories
- Handle authentication
- Support branch selection
- Shallow clone for large repos
- Error handling

#### analyze-java-code.md
- Parse Java files (AST)
- Spring Boot detection
- Maven/Gradle analysis
- JUnit test detection
- Best practices checking

#### analyze-python-code.md
- Parse Python files (AST)
- Django/Flask/FastAPI detection
- Requirements analysis
- pytest/unittest detection
- PEP 8 compliance

#### analyze-react-code.md
- Parse React/TypeScript components
- Hook usage analysis
- State management patterns
- Accessibility checks
- Performance patterns

#### detect-security-issues.md
- Pattern-based vulnerability detection
- Regex secret scanning
- Dependency CVE checking
- OWASP mapping
- Risk scoring

#### analyze-architecture.md
- Dependency graph building
- Pattern detection
- Layer violation checking
- Metric calculation
- Anti-pattern identification

#### measure-test-coverage.md
- Coverage tool integration
- Coverage parsing
- Critical path identification
- Test quality assessment
- Gap analysis

#### calculate-technical-debt.md
- Debt quantification
- Hotspot identification
- Effort estimation
- Cost calculation
- Priority recommendation

#### generate-metrics-report.md
- JSON report generation
- Markdown summary creation
- Data aggregation
- Score calculation
- Recommendation generation

### Steering Directory

Workflow guides for users:

#### getting-started.md
**Audience**: New users
- Quick start instructions
- Basic usage examples
- Understanding results
- Common first steps
- Tips for best results

#### enterprise-setup.md
**Audience**: Teams and organizations
- Organization-wide standards
- CI/CD integration (GitHub Actions, GitLab, Jenkins)
- Quality gates
- Multi-repository management
- Compliance reporting

#### custom-rules.md
**Audience**: Advanced users
- Configuration options
- Custom rule creation
- Language-specific rules
- Pattern-based rules
- Environment-specific configs

## Analysis Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    User Request                          │
│     "Analyze https://github.com/user/repo"              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              repo360-analyzer Agent                      │
│  (Main orchestrator - coordinates entire process)       │
└────────────────────┬────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Quality  │  │ Security │  │ Architect│
│ Checker  │  │ Scanner  │  │  Agent   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │    Uses Skills:          │
     │    - clone-repository    │
     │    - analyze-*-code      │
     │    - detect-security     │
     │    - analyze-architecture│
     │    - measure-coverage    │
     │    - calculate-debt      │
     │    - generate-reports    │
     │             │             │
     └─────────────┼─────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Aggregate Results   │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Generate Reports    │
        │  - JSON metrics      │
        │  - Markdown summary  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   repo360-output/    │
        │   - metrics-*.json   │
        │   - reports/*.md     │
        └──────────────────────┘
```

## Output Structure

When analysis completes, Repo360 creates:

```
repo360-output/
├── metrics-summary.json              # High-level overview
│   ├── repository info
│   ├── overall scores
│   ├── issue counts
│   └── language breakdown
│
├── quality-metrics.json              # Code quality details
│   ├── complexity metrics
│   ├── duplication analysis
│   ├── code smells
│   └── file-by-file details
│
├── security-metrics.json             # Security findings
│   ├── vulnerabilities
│   ├── dependency risks
│   ├── secrets found
│   └── compliance status
│
├── architecture-metrics.json         # Architecture analysis
│   ├── design patterns
│   ├── dependencies
│   ├── SOLID compliance
│   └── structural metrics
│
├── test-metrics.json                 # Test coverage
│   ├── coverage percentages
│   ├── test distribution
│   ├── uncovered critical paths
│   └── test quality
│
├── technical-debt.json               # Debt analysis
│   ├── total debt (hours/cost)
│   ├── debt breakdown
│   ├── hotspots
│   └── recommendations
│
├── file-details/                     # Per-file metrics
│   ├── [hash-1].json
│   ├── [hash-2].json
│   └── ...
│
└── reports/                          # Human-readable
    ├── executive-summary.md          # High-level overview
    ├── detailed-findings.md          # Complete analysis
    └── recommendations.md            # Action items
```

## Extension Points

Repo360 is designed to be extensible:

### Adding New Languages

1. Create new skill: `skills/analyze-{language}-code.md`
2. Define language-specific patterns
3. Integrate with existing tools
4. Update `power.json` to reference new skill

### Adding New Metrics

1. Define metric in appropriate agent
2. Add calculation logic
3. Update schema files
4. Include in report generation

### Adding New Rules

1. Create rule definition in config
2. Implement detection logic
3. Add to appropriate skill
4. Test and validate

### Custom Integrations

1. Define integration in config
2. Implement webhook/API calls
3. Add to reporting flow
4. Document usage

## Design Principles

### 1. Modularity
- Agents are independent specialists
- Skills are reusable capabilities
- Clean separation of concerns

### 2. Extensibility
- Easy to add new languages
- Simple to add new metrics
- Configurable for different needs

### 3. Accuracy
- Multiple analysis techniques
- Cross-validation of findings
- Industry-standard tools

### 4. Actionability
- Every issue includes fix suggestion
- Effort estimates provided
- Prioritization guidance

### 5. Performance
- Parallel analysis where possible
- Incremental analysis support
- Caching for speed

## Technology Stack

### Analysis Tools
- **Java**: Checkstyle, PMD, SpotBugs, JaCoCo
- **Python**: Pylint, Flake8, Bandit, Coverage.py
- **JavaScript/TypeScript**: ESLint, TSLint, Istanbul
- **Multi-language**: SonarQube patterns, Lizard

### Parsing & AST
- Language-specific parsers
- Abstract syntax tree analysis
- Token-based pattern matching

### Reporting
- JSON for machine readability
- Markdown for human readability
- Configurable output formats

## Maintenance

### Updating Agents
Agents are defined in Markdown with clear sections:
- Identity (role and purpose)
- Capabilities (what they can do)
- Process (how they work)
- Output (what they produce)

### Updating Skills
Skills are self-contained capabilities:
- Purpose statement
- Input parameters
- Process steps
- Output format
- Error handling

### Updating Configuration
Configuration is hierarchical:
- Global defaults (power level)
- User config (~/.repo360/config.yml)
- Repo config (.repo360/config.yml)
- Override precedence

## Support and Contributions

- **Documentation**: All files are well-commented
- **Examples**: Sample configs and projects
- **Testing**: Validate against known repos
- **Community**: Share patterns and rules

---

This structure enables powerful, accurate, and actionable repository analysis for enterprise software development.
