"""
Security Analyzer - Deep security scanning
"""

import re
from pathlib import Path
from collections import defaultdict

class SecurityAnalyzer:
    """Scans for security vulnerabilities and secrets"""
    
    # Secret patterns
    SECRET_PATTERNS = {
        'aws_access_key': r'AKIA[0-9A-Z]{16}',
        'aws_secret_key': r'[0-9a-zA-Z/+=]{40}',
        'github_token': r'gh[ps]_[a-zA-Z0-9]{36}',
        'slack_token': r'xox[baprs]-[0-9a-zA-Z-]{10,}',
        'private_key': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
        'generic_api_key': r'[aA][pP][iI][_]?[kK][eE][yY][\s]*[=:][\s]*["\']([a-zA-Z0-9_\-]{20,})["\']',
        'generic_secret': r'[sS][eE][cC][rR][eE][tT][\s]*[=:][\s]*["\']([a-zA-Z0-9_\-]{20,})["\']',
        'password': r'[pP][aA][sS][sS][wW][oO][rR][dD][\s]*[=:][\s]*["\']([^"\']+)["\']'
    }
    
    def __init__(self):
        self.results = {
            'vulnerabilities': [],
            'secrets': [],
            'critical_count': 0,
            'high_count': 0,
            'medium_count': 0,
            'low_count': 0
        }
    
    def scan_all(self, files, repo_path):
        """Scan all files for security issues"""
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                rel_path = str(file_path.relative_to(repo_path))
                
                # Scan for secrets
                self._scan_secrets(content, rel_path)
                
                # Scan for vulnerabilities
                self._scan_vulnerabilities(content, rel_path, file_path.suffix)
                
            except Exception as e:
                pass
        
        return self.results
    
    def _scan_secrets(self, content, file_path):
        """Scan for hardcoded secrets"""
        
        lines = content.splitlines()
        
        for secret_type, pattern in self.SECRET_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                matches = re.finditer(pattern, line)
                for match in matches:
                    self.results['secrets'].append({
                        'type': secret_type,
                        'file': file_path,
                        'line': line_num,
                        'severity': 'critical',
                        'message': f'Potential {secret_type.replace("_", " ")} detected'
                    })
                    self.results['critical_count'] += 1
    
    def _scan_vulnerabilities(self, content, file_path, file_ext):
        """Scan for security vulnerabilities"""
        
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            # SQL Injection patterns
            if re.search(r'execute\s*\([^)]*[+%]|SELECT.*\+|INSERT.*\+', line, re.IGNORECASE):
                self.results['vulnerabilities'].append({
                    'type': 'sql_injection',
                    'cwe': 'CWE-89',
                    'file': file_path,
                    'line': line_num,
                    'severity': 'critical',
                    'message': 'Potential SQL injection vulnerability',
                    'recommendation': 'Use parameterized queries or prepared statements'
                })
                self.results['critical_count'] += 1
            
            # Command Injection
            if re.search(r'exec\s*\(|system\s*\(|popen\s*\(|subprocess\.call.*shell\s*=\s*True', line):
                self.results['vulnerabilities'].append({
                    'type': 'command_injection',
                    'cwe': 'CWE-78',
                    'file': file_path,
                    'line': line_num,
                    'severity': 'critical',
                    'message': 'Potential command injection vulnerability',
                    'recommendation': 'Avoid shell execution or sanitize inputs'
                })
                self.results['critical_count'] += 1
            
            # XSS (for JavaScript/HTML files)
            if file_ext in ['.js', '.jsx', '.ts', '.tsx', '.html']:
                if re.search(r'innerHTML\s*=|dangerouslySetInnerHTML|document\.write\(', line):
                    self.results['vulnerabilities'].append({
                        'type': 'xss',
                        'cwe': 'CWE-79',
                        'file': file_path,
                        'line': line_num,
                        'severity': 'high',
                        'message': 'Potential XSS vulnerability',
                        'recommendation': 'Sanitize user input before rendering'
                    })
                    self.results['high_count'] += 1
            
            # Insecure deserialization
            if re.search(r'pickle\.loads|yaml\.load\(|eval\(|__import__', line):
                self.results['vulnerabilities'].append({
                    'type': 'insecure_deserialization',
                    'cwe': 'CWE-502',
                    'file': file_path,
                    'line': line_num,
                    'severity': 'high',
                    'message': 'Insecure deserialization detected',
                    'recommendation': 'Use safe alternatives like json.loads() or yaml.safe_load()'
                })
                self.results['high_count'] += 1
            
            # Weak crypto
            if re.search(r'\b(md5|sha1|des)\b', line, re.IGNORECASE):
                self.results['vulnerabilities'].append({
                    'type': 'weak_crypto',
                    'cwe': 'CWE-327',
                    'file': file_path,
                    'line': line_num,
                    'severity': 'medium',
                    'message': 'Weak cryptographic algorithm detected',
                    'recommendation': 'Use SHA-256 or stronger algorithms'
                })
                self.results['medium_count'] += 1
            
            # Debug mode
            if re.search(r'DEBUG\s*=\s*True|app\.debug\s*=\s*True', line, re.IGNORECASE):
                self.results['vulnerabilities'].append({
                    'type': 'debug_mode',
                    'file': file_path,
                    'line': line_num,
                    'severity': 'medium',
                    'message': 'Debug mode enabled',
                    'recommendation': 'Disable debug mode in production'
                })
                self.results['medium_count'] += 1
