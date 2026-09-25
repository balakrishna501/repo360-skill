"""
Python Code Analyzer - Performs REAL analysis using AST parsing
"""

import ast
import os
from pathlib import Path
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from radon.raw import analyze

class PythonAnalyzer:
    """Analyzes Python files using actual AST parsing and metrics"""
    
    def analyze_file(self, file_path, repo_path):
        """
        Perform deep analysis of a Python file
        
        Returns actual metrics, not assumptions:
        - Lines of code (actual count)
        - Cyclomatic complexity (calculated)
        - Maintainability index (calculated)
        - Functions and classes (parsed from AST)
        - Issues (detected from actual code)
        """
        result = {
            'file': str(file_path.relative_to(repo_path)),
            'language': 'Python',
            'type': 'source',
            'metrics': {},
            'functions': [],
            'classes': [],
            'issues': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Parse AST
            tree = ast.parse(code)
            
            # Raw metrics (actual line counts)
            raw_metrics = analyze(code)
            result['metrics']['loc'] = raw_metrics.loc  # Lines of code
            result['metrics']['lloc'] = raw_metrics.lloc  # Logical lines
            result['metrics']['sloc'] = raw_metrics.sloc  # Source lines
            result['metrics']['comments'] = raw_metrics.comments
            result['metrics']['multi'] = raw_metrics.multi
            result['metrics']['blank'] = raw_metrics.blank
            
            # Cyclomatic Complexity (actual calculation)
            complexity_results = cc_visit(code)
            complexities = []
            for item in complexity_results:
                func_info = {
                    'name': item.name,
                    'type': item.type,
                    'lineno': item.lineno,
                    'complexity': item.complexity,
                    'rank': item.rank
                }
                result['functions'].append(func_info)
                complexities.append(item.complexity)
                
                # Flag high complexity
                if item.complexity > 10:
                    result['issues'].append({
                        'type': 'high_complexity',
                        'severity': 'high' if item.complexity > 15 else 'medium',
                        'line': item.lineno,
                        'function': item.name,
                        'message': f'High cyclomatic complexity: {item.complexity}',
                        'complexity': item.complexity
                    })
            
            result['metrics']['complexity_average'] = (
                sum(complexities) / len(complexities) if complexities else 0
            )
            result['metrics']['complexity_max'] = max(complexities) if complexities else 0
            
            # Maintainability Index (actual calculation)
            mi_score = mi_visit(code, multi=True)
            result['metrics']['maintainability_index'] = round(mi_score, 2)
            
            # Halstead metrics (actual calculation)
            halstead = h_visit(code)
            if halstead:
                result['metrics']['halstead'] = {
                    'volume': round(halstead.total.volume, 2),
                    'difficulty': round(halstead.total.difficulty, 2),
                    'effort': round(halstead.total.effort, 2)
                }
            
            # Extract classes from AST
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    result['classes'].append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
            
            # Detect actual code issues
            self._detect_issues(tree, result)
            
        except SyntaxError as e:
            result['issues'].append({
                'type': 'syntax_error',
                'severity': 'critical',
                'line': e.lineno if hasattr(e, 'lineno') else 0,
                'message': str(e)
            })
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _detect_issues(self, tree, result):
        """Detect code quality issues from AST"""
        
        for node in ast.walk(tree):
            # Detect bare except clauses
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    result['issues'].append({
                        'type': 'bare_except',
                        'severity': 'medium',
                        'line': node.lineno,
                        'message': 'Bare except clause - catch specific exceptions'
                    })
            
            # Detect print statements (should use logging)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'print':
                    result['issues'].append({
                        'type': 'print_statement',
                        'severity': 'low',
                        'line': node.lineno,
                        'message': 'Use logging instead of print()'
                    })
            
            # Detect functions with too many arguments
            if isinstance(node, ast.FunctionDef):
                num_args = len(node.args.args)
                if num_args > 5:
                    result['issues'].append({
                        'type': 'too_many_parameters',
                        'severity': 'medium',
                        'line': node.lineno,
                        'function': node.name,
                        'message': f'Function has {num_args} parameters (max recommended: 5)'
                    })
                
                # Detect missing docstrings
                if not ast.get_docstring(node):
                    result['issues'].append({
                        'type': 'missing_docstring',
                        'severity': 'low',
                        'line': node.lineno,
                        'function': node.name,
                        'message': 'Function missing docstring'
                    })
