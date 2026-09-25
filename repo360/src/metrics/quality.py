"""
Quality Metrics Calculator
"""

class QualityCalculator:
    """Calculates code quality metrics from analyzed files"""
    
    def calculate(self, files):
        """Calculate aggregate quality metrics"""
        
        total_issues = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        maintainability_scores = []
        total_loc = 0
        total_comments = 0
        
        for file_result in files:
            # Count issues by severity
            for issue in file_result.get('issues', []):
                severity = issue.get('severity', 'low')
                if severity in total_issues:
                    total_issues[severity] += 1
            
            # Collect maintainability scores
            metrics = file_result.get('metrics', {})
            if 'maintainability_index' in metrics:
                maintainability_scores.append(metrics['maintainability_index'])
            
            # Count lines
            total_loc += metrics.get('loc', metrics.get('code_lines', 0))
            total_comments += metrics.get('comments', metrics.get('comment_lines', 0))
        
        avg_maintainability = (
            sum(maintainability_scores) / len(maintainability_scores)
            if maintainability_scores else 0
        )
        
        comment_ratio = (
            (total_comments / total_loc * 100) if total_loc > 0 else 0
        )
        
        return {
            'maintainability_average': round(avg_maintainability, 2),
            'total_loc': total_loc,
            'total_comments': total_comments,
            'comment_ratio': round(comment_ratio, 2),
            'issues_by_severity': total_issues,
            'total_issues': sum(total_issues.values())
        }
