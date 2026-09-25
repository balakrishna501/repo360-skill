"""
JSON Reporter - Generates JSON output files
"""

import json
from pathlib import Path

class JSONReporter:
    """Generates JSON reports from analysis results"""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
    
    def generate(self, results):
        """Generate all JSON report files"""
        
        # Main metrics file
        metrics_file = self.output_dir / 'metrics.json'
        with open(metrics_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Summary file
        summary = self._create_summary(results)
        summary_file = self.output_dir / 'summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Detailed issues file
        issues = self._extract_issues(results)
        issues_file = self.output_dir / 'issues.json'
        with open(issues_file, 'w') as f:
            json.dump(issues, f, indent=2)
        
        print(f"  ✓ Generated {metrics_file}")
        print(f"  ✓ Generated {summary_file}")
        print(f"  ✓ Generated {issues_file}")
    
    def _create_summary(self, results):
        """Create executive summary"""
        return {
            'repository': results['repository'],
            'analyzed_at': results['repository']['analyzed_at'],
            'statistics': results.get('statistics', {}),
            'scores': results.get('scores', {}),
            'metrics': {
                'complexity': results.get('metrics', {}).get('complexity', {}),
                'quality': results.get('metrics', {}).get('quality', {}),
                'technical_debt': results.get('metrics', {}).get('technical_debt', {})
            },
            'security': {
                'critical': results.get('security', {}).get('critical_count', 0),
                'high': results.get('security', {}).get('high_count', 0),
                'medium': results.get('security', {}).get('medium_count', 0),
                'low': results.get('security', {}).get('low_count', 0)
            }
        }
    
    def _extract_issues(self, results):
        """Extract all issues from results"""
        all_issues = []
        
        # Code quality issues
        for file_result in results.get('files', []):
            for issue in file_result.get('issues', []):
                all_issues.append({
                    'file': file_result['file'],
                    'type': issue.get('type'),
                    'severity': issue.get('severity'),
                    'line': issue.get('line', issue.get('lineno', 0)),
                    'message': issue.get('message'),
                    'category': 'quality'
                })
        
        # Security issues
        for vuln in results.get('security', {}).get('vulnerabilities', []):
            all_issues.append({
                'file': vuln.get('file'),
                'type': vuln.get('type'),
                'severity': vuln.get('severity'),
                'line': vuln.get('line'),
                'message': vuln.get('message'),
                'category': 'security',
                'cwe': vuln.get('cwe')
            })
        
        for secret in results.get('security', {}).get('secrets', []):
            all_issues.append({
                'file': secret.get('file'),
                'type': secret.get('type'),
                'severity': 'critical',
                'line': secret.get('line'),
                'message': secret.get('message'),
                'category': 'security'
            })
        
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        all_issues.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 4))
        
        return {
            'total_issues': len(all_issues),
            'by_severity': {
                'critical': len([i for i in all_issues if i['severity'] == 'critical']),
                'high': len([i for i in all_issues if i['severity'] == 'high']),
                'medium': len([i for i in all_issues if i['severity'] == 'medium']),
                'low': len([i for i in all_issues if i['severity'] == 'low'])
            },
            'issues': all_issues
        }
