# Analyze Java Code Skill

## Purpose
Perform comprehensive analysis of Java code including quality, complexity, design patterns, Spring framework usage, and best practices compliance.

## Capabilities

### 1. Static Code Analysis
- Parse Java files using AST
- Calculate complexity metrics
- Detect code smells
- Identify duplications
- Check naming conventions

### 2. Framework Detection
- Spring Boot / Spring Framework
- Jakarta EE / Java EE
- Hibernate / JPA
- Maven / Gradle projects
- JUnit / TestNG tests

### 3. Quality Checks
- **SOLID Principles**: Check adherence to SRP, OCP, LSP, ISP, DIP
- **Effective Java**: Apply best practices from Joshua Bloch's guidelines
- **Code Complexity**: Cyclomatic and cognitive complexity
- **Exception Handling**: Try-catch patterns, proper exception usage
- **Resource Management**: Try-with-resources, connection handling
- **Concurrency**: Thread safety, synchronization patterns

### 4. Design Patterns
Detect common Java patterns:
- Singleton, Factory, Builder
- Dependency Injection
- Repository pattern
- Service layer pattern
- DTO pattern
- Strategy, Observer, Decorator

### 5. Metrics Collected

```json
{
  "file": "src/main/java/com/example/UserService.java",
  "package": "com.example",
  "class_name": "UserService",
  "type": "class",
  "lines": 234,
  "methods": 12,
  "complexity": 28,
  "maintainability_index": 65,
  "dependencies": ["UserRepository", "EmailService", "AuditLogger"],
  "annotations": ["@Service", "@Transactional"],
  "issues": [
    {
      "type": "high_complexity",
      "line": 45,
      "method": "processUser",
      "severity": "high",
      "message": "Method complexity is 15 (threshold: 10)"
    }
  ]
}
```

## Process

### Step 1: Discovery
```bash
# Find all Java files
find . -name "*.java" -type f

# Identify build system
if [ -f "pom.xml" ]; then
  echo "Maven project"
elif [ -f "build.gradle" ]; then
  echo "Gradle project"
fi

# Check for Spring Boot
grep -r "@SpringBootApplication" src/
```

### Step 2: Parse and Analyze
For each Java file:
1. Parse into AST
2. Extract classes, methods, fields
3. Calculate metrics
4. Check patterns
5. Identify issues

### Step 3: Framework-Specific Analysis
```java
// Spring Boot checks
- @Service, @Component, @Repository usage
- @Autowired vs constructor injection
- @Transactional boundaries
- REST controller design (@RestController, @RequestMapping)
- Exception handling (@ControllerAdvice, @ExceptionHandler)

// JPA/Hibernate checks
- Entity design
- Relationship mappings
- Query optimization
- N+1 query problems
- Transaction management
```

### Step 4: Quality Assessment
- Check for proper exception handling
- Verify resource management (try-with-resources)
- Assess thread safety
- Review stream API usage
- Check null safety patterns

## Common Issues Detected

### High Complexity
```java
// Example: Method with cyclomatic complexity > 10
public void processOrder(Order order) {
    if (order.isValid()) {
        if (order.hasItems()) {
            if (order.getTotal() > 0) {
                // ... many nested conditions
            }
        }
    }
}
```

**Recommendation**: Extract methods, use early returns, apply strategy pattern

### Exception Handling
```java
// Bad: Empty catch block
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure
}
```

**Recommendation**: Log errors, handle specifically, propagate when needed

### Resource Management
```java
// Bad: Manual resource closing
InputStream is = new FileInputStream("file.txt");
// ... use stream
is.close(); // May not execute if exception occurs
```

**Recommendation**: Use try-with-resources

```java
// Good
try (InputStream is = new FileInputStream("file.txt")) {
    // ... use stream
} // Automatically closed
```

## Tools Integration

### Checkstyle
```bash
# Run Checkstyle for code style
java -jar checkstyle.jar -c /sun_checks.xml src/
```

### PMD
```bash
# Run PMD for code quality
pmd check -d src/ -R rulesets/java/quickstart.xml
```

### SpotBugs
```bash
# Run SpotBugs for bug patterns
spotbugs -textui -effort:max target/classes
```

## Output Structure

```json
{
  "language": "java",
  "framework": "spring-boot",
  "build_system": "maven",
  "total_files": 156,
  "total_classes": 178,
  "total_methods": 892,
  "total_lines": 23456,
  "quality_score": 75,
  "issues_summary": {
    "critical": 2,
    "high": 12,
    "medium": 34,
    "low": 56
  },
  "files": [
    {
      "path": "src/main/java/com/example/service/UserService.java",
      "metrics": { "..." },
      "issues": [ "..." ]
    }
  ]
}
```

## Best Practices Checked

1. **Immutability**: Prefer immutable objects
2. **Composition over Inheritance**: Check class hierarchies
3. **Interface-based Design**: Use interfaces for abstractions
4. **Dependency Injection**: Constructor injection preferred
5. **Null Safety**: Use Optional, Objects.requireNonNull
6. **Stream API**: Effective use of Java streams
7. **Exception Handling**: Specific exceptions, proper catching
8. **Resource Management**: AutoCloseable, try-with-resources
9. **Thread Safety**: Proper synchronization, immutability
10. **Testing**: JUnit 5, proper assertions, coverage
