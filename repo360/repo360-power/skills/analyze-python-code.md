# Analyze Python Code Skill

## Purpose
Comprehensive analysis of Python code including quality, complexity, framework patterns, and Pythonic best practices.

## Capabilities

### 1. Framework Detection
- Django (models, views, URLs, middleware)
- Flask (blueprints, routes, extensions)
- FastAPI (routers, dependencies, async)
- Requirements analysis (requirements.txt, Pipfile, pyproject.toml)

### 2. Code Quality Checks
- **PEP 8**: Style guide compliance
- **PEP 257**: Docstring conventions
- **Type Hints**: Type annotation coverage
- **Pythonic Idioms**: List comprehensions, generators, context managers
- **Code Complexity**: Cyclomatic complexity, nesting depth
- **Import Organization**: Standard, third-party, local imports

### 3. Common Issues Detected

#### Mutable Default Arguments
```python
# Bad
def append_to(element, target=[]):
    target.append(element)
    return target
```

#### Bare Except
```python
# Bad
try:
    risky_operation()
except:
    pass
```

#### Missing Type Hints
```python
# Bad
def calculate(x, y):
    return x + y

# Good
def calculate(x: int, y: int) -> int:
    return x + y
```

### 4. Metrics Collected

```json
{
  "file": "app/services/user_service.py",
  "module": "app.services.user_service",
  "lines": 245,
  "functions": 15,
  "classes": 3,
  "complexity": 18,
  "maintainability_index": 72,
  "type_hint_coverage": 65,
  "docstring_coverage": 80,
  "pep8_violations": 5,
  "issues": [
    {
      "type": "missing_type_hints",
      "line": 42,
      "function": "process_user",
      "severity": "medium",
      "message": "Function missing return type annotation"
    }
  ]
}
```

## Process

### Step 1: Discovery
```bash
# Find Python files
find . -name "*.py" -type f

# Detect framework
if [ -f "manage.py" ]; then
  echo "Django project"
elif grep -q "Flask" requirements.txt; then
  echo "Flask project"
elif grep -q "fastapi" requirements.txt; then
  echo "FastAPI project"
fi

# Find dependencies
ls requirements.txt Pipfile pyproject.toml setup.py 2>/dev/null
```

### Step 2: Static Analysis
```bash
# Pylint
pylint app/ --output-format=json

# Flake8
flake8 app/ --format=json

# Radon (complexity)
radon cc app/ -j

# Mypy (type checking)
mypy app/ --json-report
```

### Step 3: Parse Each File
```python
import ast

# Parse Python file
with open(file_path) as f:
    tree = ast.parse(f.read())

# Extract functions, classes
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        # Analyze function
    elif isinstance(node, ast.ClassDef):
        # Analyze class
```

## Framework-Specific Analysis

### Django
```python
# Check Models
- Proper field types
- Meta class usage
- __str__ method
- Indexes and constraints
- Migration files

# Check Views
- Class-based vs function views
- Permission checks
- Input validation
- Query optimization (select_related, prefetch_related)

# Check URLs
- URL patterns organization
- Namespace usage

# Check Settings
- DEBUG mode
- SECRET_KEY security
- ALLOWED_HOSTS
- Security middleware
```

### Flask
```python
# Check Blueprints
- Blueprint organization
- URL prefix usage

# Check Routes
- Route methods (GET, POST, etc.)
- Request validation
- Error handling

# Check Extensions
- Flask-SQLAlchemy usage
- Flask-Login configuration
- CORS setup
```

### FastAPI
```python
# Check Routers
- Router organization
- Dependency injection
- Async usage

# Check Models
- Pydantic models
- Validation rules
- Response models

# Check Dependencies
- Proper dependency injection
- Database session management
```

## Pythonic Patterns

### List Comprehensions
```python
# Check for proper usage
# Good
squares = [x**2 for x in range(10)]

# Avoid overly complex comprehensions
# Bad
result = [x for sublist in matrix for x in sublist if x > 0 and x % 2 == 0]
```

### Context Managers
```python
# Check for proper resource management
# Good
with open('file.txt') as f:
    content = f.read()

# Detect missing context managers
# Bad
f = open('file.txt')
content = f.read()
# f.close() might not be called
```

### Generators
```python
# Check for memory-efficient patterns
# Good (for large data)
def process_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield process(line)
```

## Quality Metrics

### Maintainability Index
```
MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
Where:
  HV = Halstead Volume
  CC = Cyclomatic Complexity
  LOC = Lines of Code
```

### Type Hint Coverage
```
Coverage = (Functions with type hints / Total functions) * 100
```

### Docstring Coverage
```
Coverage = (Functions with docstrings / Total functions) * 100
```

## Common Security Issues

### SQL Injection
```python
# Bad
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Good
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Command Injection
```python
# Bad
os.system(f"ls {user_input}")

# Good
subprocess.run(["ls", user_input], check=True)
```

### Unsafe Deserialization
```python
# Bad
import pickle
data = pickle.loads(user_data)

# Better
import json
data = json.loads(user_data)
```

## Output Structure

```json
{
  "language": "python",
  "framework": "django",
  "python_version": "3.11",
  "total_files": 89,
  "total_lines": 12456,
  "total_functions": 234,
  "total_classes": 67,
  "quality_score": 78,
  "pep8_compliance": 92,
  "type_hint_coverage": 65,
  "docstring_coverage": 82,
  "average_complexity": 4.2,
  "files": [
    {
      "path": "app/services/user_service.py",
      "metrics": {},
      "issues": []
    }
  ]
}
```

## Tools Used

1. **Pylint**: Comprehensive linting
2. **Flake8**: Style guide enforcement
3. **Radon**: Complexity metrics
4. **Mypy**: Static type checking
5. **Bandit**: Security issue detection
6. **Black**: Code formatting check
7. **isort**: Import sorting check

## Best Practices

1. **PEP 8 Compliance**: Follow style guide
2. **Type Hints**: Use type annotations
3. **Docstrings**: Document all public APIs
4. **Virtual Environments**: Use venv/virtualenv
5. **Requirements**: Pin dependency versions
6. **Testing**: Use pytest, maintain coverage
7. **Async**: Use async/await for I/O-bound operations
8. **Error Handling**: Specific exception catching
9. **Context Managers**: For resource management
10. **List Comprehensions**: For simple transformations
