# Repo360 - Deep Code Analysis Engine

A real, working code analysis tool that clones GitHub repositories and performs comprehensive deep scanning to generate actionable metrics.

## What This Tool Actually Does

1. **Clones** your GitHub repository
2. **Scans** every file line-by-line using real static analysis tools
3. **Analyzes** code quality, security, architecture, and technical debt
4. **Generates** JSON metrics and interactive HTML dashboard
5. **NO ASSUMPTIONS** - Everything is actually scanned and measured

## Architecture

```
repo360/
├── src/                       # Core analysis engine
│   ├── main.py               # Entry point
│   ├── cloner.py             # Git repository cloning
│   ├── scanner.py            # File discovery and parsing
│   ├── analyzers/            # Real analysis engines
│   │   ├── java_analyzer.py
│   │   ├── python_analyzer.py
│   │   ├── javascript_analyzer.py
│   │   └── security_analyzer.py
│   ├── metrics/              # Metrics calculation
│   │   ├── complexity.py
│   │   ├── quality.py
│   │   └── debt.py
│   └── reporters/            # Report generation
│       ├── json_reporter.py
│       └── html_reporter.py
├── output/                   # Generated reports
├── requirements.txt          # Python dependencies
└── run.py                    # Quick start script
```

## Installation

```bash
# Clone this tool
git clone https://github.com/yourusername/repo360
cd repo360

# Install dependencies
pip install -r requirements.txt

# Run analysis
python run.py --repo https://github.com/username/repository --branch main
```

## What You Get

After analysis:
- `output/metrics.json` - All raw metrics
- `output/dashboard.html` - Interactive dashboard for project managers
- `output/detailed-report.json` - File-by-file analysis
