# Detect Security Issues Skill

## Purpose
Identify security vulnerabilities, insecure patterns, and compliance issues across the codebase.

## Detection Areas

### 1. Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (shell execution with user input)
- XSS (unescaped HTML rendering)
- Path traversal (file operations with user paths)

### 2. Authentication & Authorization
- Missing authentication checks
- Weak password policies
- Broken access control
- Session management issues
- JWT vulnerabilities

### 3. Cryptography
- Weak algorithms (MD5, SHA1, DES)
- Hardcoded encryption keys
- Insecure random number generation
- Missing TLS/SSL

### 4. Secrets Detection
- API keys, passwords, tokens
- Private keys and certificates
- Database credentials
- Cloud provider credentials (AWS, Azure, GCP)

### 5. Dependency Vulnerabilities
- Known CVEs in dependencies
- Outdated packages
- Vulnerable transitive dependencies

## Detection Patterns

### SQL Injection
```java
// Detect:
"SELECT * FROM users WHERE id = " + userId
String.format("DELETE FROM %s WHERE id = %s", table, id)
```

### Hardcoded Secrets
```python
# Detect:
password = "MySecret123!"
api_key = "sk_live_abc123..."
AWS_SECRET_KEY = "wJalrXUtnFEMI/..."
```

### XSS
```javascript
// Detect:
element.innerHTML = userInput
dangerouslySetInnerHTML={{__html: data}}
```

## Output
```json
{
  "security_score": 68,
  "critical_issues": 3,
  "high_issues": 12,
  "vulnerabilities": [
    {
      "id": "SEC-001",
      "type": "sql_injection",
      "severity": "critical",
      "cwe": "CWE-89",
      "file": "UserDao.java",
      "line": 42,
      "description": "...",
      "recommendation": "Use prepared statements"
    }
  ]
}
```
