"""
JavaScript/TypeScript Analyzer - Performs REAL analysis
"""

import esprima
import lizard
from pathlib import Path

class JavaScriptAnalyzer:
    """Analyzes JavaScript/TypeScript files using actual parsing"""
    
    def analyze_file(self, file_path, repo_path):
        """
        Perform deep analysis of a JavaScript/TypeScript file
        Returns ACTUAL metrics from parsing
        """
        result = {
            'file': str(file_path.relative_to(repo_path)),
            'language': 'JavaScript' if file_path.suffix in ['.js', '.jsx'] else 'TypeScript',
            'type': 'source',
            'metrics': {},
            'functions': [],
            'issues': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Count actual lines
            lines = code.split('\n')
            result['metrics']['total_lines'] = len(lines)
            result['metrics']['code_lines'] = len([l for l in lines if l.strip() and not l.strip().startswith('//')])
            
            # Parse JavaScript (works for JSX too, TypeScript needs preprocessing)
            if file_path.suffix in ['.js', '.jsx']:
                try:
                    ast = esprima.parseScript(code, {'loc': True, 'tolerant': True})
                    self._analyze_ast(ast, result)
                except:
                    # Try as module
                    try:
                        ast = esprima.parseModule(code, {'loc': True, 'tolerant': True})
                        self._analyze_ast(ast, result)
                    except Exception as e:
                        result['issues'].append({
                            'type': 'parse_error',
                            'severity': 'high',
                            'message': f'Failed to parse JavaScript: {str(e)}'
                        })
            
            # Use Lizard for complexity
            lizard_result = lizard.analyze_file.analyze_source_code(str(file_path), code)
            
            complexities = []
            for func in lizard_result.function_list:
                func_info = {
                    'name': func.name,
                    'complexity': func.cyclomatic_complexity,
                    'lines': func.nloc,
                    'parameters': func.parameter_count
                }
                result['functions'].append(func_info)
                complexities.append(func.cyclomatic_complexity)
                
                # Flag high complexity
                if func.cyclomatic_complexity > 10:
                    result['issues'].append({
                        'type': 'high_complexity',
                        'severity': 'high' if func.cyclomatic_complexity > 15 else 'medium',
                        'function': func.name,
                        'complexity': func.cyclomatic_complexity,
                        'message': f'High cyclomatic complexity: {func.cyclomatic_complexity}'
                    })
            
            result['metrics']['complexity_average'] = (
                sum(complexities) / len(complexities) if complexities else 0
            )
            result['metrics']['complexity_max'] = max(complexities) if complexities else 0
            
            # Detect actual issues in code
            self._detect_issues(code, lines, result)
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_ast(self, ast, result):
        """Analyze JavaScript AST"""
        
        def walk(node):
            if isinstance(node, dict):
                node_type = node.get('type', '')
                
                # Detect console.log
                if node_type == 'CallExpression':
                    callee = node.get('callee', {})
                    if (callee.get('type') == 'MemberExpression' and
                        callee.get('object', {}).get('name') == 'console'):
                        result['issues'].append({
                            'type': 'console_log',
                            'severity': 'low',
                            'line': node.get('loc', {}).get('start', {}).get('line', 0),
                            'message': 'Remove console.log in production code'
                        })
                
                # Detect var usage (should use let/const)
                if node_type == 'VariableDeclaration' and node.get('kind') == 'var':
                    result['issues'].append({
                        'type': 'var_usage',
                        'severity': 'low',
                        'line': node.get('loc', {}).get('start', {}).get('line', 0),
                        'message': 'Use let or const instead of var'
                    })
                
                # Recursively walk child nodes
                for value in node.values():
                    if isinstance(value, (dict, list)):
                        walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        
        walk(ast)
    
    def _detect_issues(self, code, lines, result):
        """Detect code issues by analyzing actual code"""
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Detect dangerouslySetInnerHTML
            if 'dangerouslySetInnerHTML' in stripped:
                result['issues'].append({
                    'type': 'dangerous_html',
                    'severity': 'high',
                    'line': i,
                    'message': 'XSS risk: dangerouslySetInnerHTML - sanitize HTML content'
                })
            
            # Detect == instead of ===
            if '==' in stripped and '===' not in stripped and '!=' in stripped and '!==' not in stripped:
                if not stripped.startswith('//'):
                    result['issues'].append({
                        'type': 'loose_equality',
                        'severity': 'low',
                        'line': i,
                        'message': 'Use === instead of == for strict equality'
                    })
            
            # Detect eval usage
            if 'eval(' in stripped and not stripped.startswith('//'):
                result['issues'].append({
                    'type': 'eval_usage',
                    'severity': 'critical',
                    'line': i,
                    'message': 'eval() is dangerous and should be avoided'
                })
