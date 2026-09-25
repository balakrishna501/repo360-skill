"""
Repo360 Main Analysis Engine
Orchestrates the entire analysis workflow
"""

import os
import json
from pathlib import Path
from datetime import datetime
from cloner import RepositoryCloner
from scanner import FileScanner
from analyzers.java_analyzer import JavaAnalyzer
from analyzers.python_analyzer import PythonAnalyzer
from analyzers.javascript_analyzer import JavaScriptAnalyzer
from analyzers.security_analyzer import SecurityAnalyzer
from metrics.complexity import ComplexityCalculator
from metrics.quality import QualityCalculator
from metrics.debt import TechnicalDebtCalculator
from reporters.json_reporter import JSONReporter
from reporters.html_reporter import HTMLDashboardGenerator

class Repo360Analyzer:
    """Main analyzer that coordinates all analysis activities"""
    
    def __init__(self, repo_url, branch='main', output_dir='output', 
                 shallow=False, skip_tests=False):
        self.repo_url = repo_url
        self.branch = branch
        self.output_dir = Path(output_dir)
        self.shallow = shallow
        self.skip_tests = skip_tests
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.cloner = RepositoryCloner()
        self.scanner = FileScanner(skip_tests=skip_tests)
        self.results = {
            'repository': {
                'url': repo_url,
                'branch': branch,
                'analyzed_at': datetime.now().isoformat()
            },
            'files': [],
            'metrics': {},
            'issues': []
        }
    
    def run(self):
        """Execute full analysis workflow"""
        
        # Step 1: Clone repository
        print("\n[1/7] Cloning repository...")
        repo_path = self.cloner.clone(
            self.repo_url, 
            self.branch, 
            shallow=self.shallow
        )
        self.results['repository']['path'] = str(repo_path)
        self.results['repository']['commit'] = self.cloner.get_commit_info(repo_path)
        
        # Step 2: Scan files
        print("\n[2/7] Scanning files...")
        files = self.scanner.scan(repo_path)
        print(f"  Found {len(files)} source files")
        self.results['statistics'] = {
            'total_files': len(files),
            'languages': self.scanner.get_language_stats(files)
        }
        
        # Step 3: Analyze by language
        print("\n[3/7] Analyzing code quality...")
        self._analyze_files(files, repo_path)
        
        # Step 4: Security analysis
        print("\n[4/7] Scanning for security issues...")
        security_analyzer = SecurityAnalyzer()
        security_results = security_analyzer.scan_all(files, repo_path)
        self.results['security'] = security_results
        
        # Step 5: Calculate metrics
        print("\n[5/7] Calculating metrics...")
        self._calculate_metrics()
        
        # Step 6: Generate JSON reports
        print("\n[6/7] Generating JSON reports...")
        json_reporter = JSONReporter(self.output_dir)
        json_reporter.generate(self.results)
        
        # Step 7: Generate HTML dashboard
        print("\n[7/7] Generating HTML dashboard...")
        html_generator = HTMLDashboardGenerator(self.output_dir)
        html_generator.generate(self.results)
        
        print(f"\n✓ Analysis complete")
        print(f"  - Dashboard: {self.output_dir / 'dashboard.html'}")
        print(f"  - Metrics: {self.output_dir / 'metrics.json'}")
    
    def _analyze_files(self, files, repo_path):
        """Analyze files by language"""
        
        java_files = [f for f in files if f.suffix == '.java']
        python_files = [f for f in files if f.suffix == '.py']
        js_files = [f for f in files if f.suffix in ['.js', '.jsx', '.ts', '.tsx']]
        
        all_file_results = []
        
        # Java analysis
        if java_files:
            print(f"  Analyzing {len(java_files)} Java files...")
            java_analyzer = JavaAnalyzer()
            for java_file in java_files:
                result = java_analyzer.analyze_file(java_file, repo_path)
                all_file_results.append(result)
        
        # Python analysis
        if python_files:
            print(f"  Analyzing {len(python_files)} Python files...")
            python_analyzer = PythonAnalyzer()
            for py_file in python_files:
                result = python_analyzer.analyze_file(py_file, repo_path)
                all_file_results.append(result)
        
        # JavaScript/TypeScript analysis
        if js_files:
            print(f"  Analyzing {len(js_files)} JavaScript/TypeScript files...")
            js_analyzer = JavaScriptAnalyzer()
            for js_file in js_files:
                result = js_analyzer.analyze_file(js_file, repo_path)
                all_file_results.append(result)
        
        self.results['files'] = all_file_results
    
    def _calculate_metrics(self):
        """Calculate aggregate metrics"""
        
        # Complexity metrics
        complexity_calc = ComplexityCalculator()
        complexity_metrics = complexity_calc.calculate(self.results['files'])
        
        # Quality metrics
        quality_calc = QualityCalculator()
        quality_metrics = quality_calc.calculate(self.results['files'])
        
        # Technical debt
        debt_calc = TechnicalDebtCalculator()
        debt_metrics = debt_calc.calculate(
            self.results['files'],
            complexity_metrics,
            quality_metrics,
            self.results.get('security', {})
        )
        
        self.results['metrics'] = {
            'complexity': complexity_metrics,
            'quality': quality_metrics,
            'technical_debt': debt_metrics
        }
        
        # Calculate overall scores
        self.results['scores'] = self._calculate_scores(
            complexity_metrics,
            quality_metrics,
            debt_metrics,
            self.results.get('security', {})
        )
    
    def _calculate_scores(self, complexity, quality, debt, security):
        """Calculate overall health scores"""
        
        # Quality score (0-100)
        quality_score = min(100, quality.get('maintainability_average', 50))
        
        # Security score (100 minus penalties)
        security_score = 100
        security_score -= security.get('critical_count', 0) * 20
        security_score -= security.get('high_count', 0) * 10
        security_score -= security.get('medium_count', 0) * 5
        security_score = max(0, security_score)
        
        # Complexity score
        avg_complexity = complexity.get('average_complexity', 0)
        complexity_score = max(0, 100 - (avg_complexity * 5))
        
        # Overall score (weighted average)
        overall_score = (
            quality_score * 0.35 +
            security_score * 0.35 +
            complexity_score * 0.30
        )
        
        return {
            'overall': round(overall_score, 2),
            'quality': round(quality_score, 2),
            'security': round(security_score, 2),
            'complexity': round(complexity_score, 2)
        }
