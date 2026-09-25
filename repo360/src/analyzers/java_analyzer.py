"""
Java Code Analyzer
Deep analysis of Java source files
"""

import re
import javalang
from pathlib import Path

class JavaAnalyzer:
    """Analyzes Java source code"""
    
    def __init__(self):
        self.issues = []
    
    def analyze_file(self, file_path, repo_root):
        """Analyze a single Java file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            result = {
                'file': str(file_path.relative_to(repo_root)),
                'language': 'java',
                'size': len(content),
                'lines': len(content.splitlines()),
                'issues': []
            }
            
            # Parse with javalang
            try:
                tree = javalang.parse.parse(content)
                result.update(self._analyze_ast(tree, content, file_path))
            except Exception as parse_error:
                result['parse_error'] = str(parse_error)
            
            # Pattern-based analysis
            result['issues'].extend(self._pattern_analysis(content, file_path))
            
            # Calculate complexity
            result['complexity'] = self._calculate_complexity(content)
            
            return result
            
        except Exception as e:
            return {
                'file': str(file_path.relative_to(repo_root)),
                'language': 'java',
                'error': str(e)
            }
    
    def _analyze_ast(self, tree, content, file_path):
        """Analyze Java AST"""
        
        classes = []
        methods = []
        imports = []
        
        # Extract classes
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_info = {
                'name': node.name,
                'line': node.position.line if node.position else 0,
                'methods': len([m for m in node.methods]) if hasattr(node, 'methods') else 0,
                'fields': len([f for f in node.fields]) if hasattr(node, 'fields') else 0
            }
            classes.append(class_info)
            
            # Check for god class
            if class_info['methods'] > 20 or class_info['fields'] > 15:
                self.issues.append({
                    'type': 'god_class',
                    'severity': 'high',
                    'file': str(file_path),
                    'line': class_info['line'],
                    'message': f"Class '{node.name}' has too many methods ({class_info['methods']}) or fields ({class_info['fields']})"
                })
        
        # Extract methods
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            method_info = {
                'name': node.name,
                'line': node.position.line if node.position else 0,
                'parameters': len(node.parameters) if node.parameters else 0
            }
            methods.append(method_info)
            
            # Check for long parameter list
            if method_info['parameters'] > 5:
                self.issues.append({
                    'type': 'long_parameter_list',
                    'severity': 'medium',
                    'file': str(file_path),
                    'line': method_info['line'],
                    'message': f"Method '{node.name}' has {method_info['parameters']} parameters (max: 5)"
                })
        
        # Extract imports
        for path, node in tree.filter(javalang.tree.Import):
            imports.append(node.path)
        
        return {
            'classes': classes,
            'methods': methods,
            'imports': imports,
            'class_count': len(classes),
            'method_count': len(methods),
            'import_count': len(imports)
        }
    
    def _pattern_analysis(self, content, file_path):
        """Pattern-based code analysis"""
        
        issues = []
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            # System.out.println usage
            if re.search(r'System\.out\.print', line):
                issues.append({
                    'type': 'system_out',
                    'severity': 'low',
                    'line': line_num,
                    'message': 'Use logging framework instead of System.out'
                })
            
            # Empty catch blocks
            if re.search(r'catch\s*\([^)]+\)\s*{\s*}', line):
                issues.append({
                    'type': 'empty_catch',
                    'severity': 'high',
                    'line': line_num,
                    'message': 'Empty catch block - handle or log exceptions'
                })
            
            # SQL concatenation (potential injection)
            if re.search(r'"SELECT.*\+|String\.format.*SELECT', line):
                issues.append({
                    'type': 'sql_injection_risk',
                    'severity': 'critical',
                    'line': line_num,
                    'message': 'Potential SQL injection - use PreparedStatement'
                })
            
            # Hardcoded passwords
            if re.search(r'password\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                issues.append({
                    'type': 'hardcoded_credential',
                    'severity': 'critical',
                    'line': line_num,
                    'message': 'Hardcoded credential detected'
                })
        
        return issues
    
    def _calculate_complexity(self, content):
        """Calculate cyclomatic complexity"""
        
        # Count decision points
        decision_keywords = [
            r'\bif\s*\(',
            r'\bfor\s*\(',
            r'\bwhile\s*\(',
            r'\bcase\s+',
            r'\bcatch\s*\(',
            r'\b&&\b',
            r'\|\|',
            r'\?'
        ]
        
        complexity = 1  # Start at 1
        for keyword in decision_keywords:
            complexity += len(re.findall(keyword, content))
        
        return complexity
