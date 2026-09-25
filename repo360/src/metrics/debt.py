"""
Technical Debt Calculator
"""

class TechnicalDebtCalculator:
    """Calculates technical debt from metrics"""
    
    HOURLY_RATE = 100  # USD per hour
    
    def calculate(self, files, complexity_metrics, quality_metrics, security_metrics):
        """Calculate technical debt in hours and cost"""
        
        debt_hours = 0
        
        # Debt from complexity
        high_complexity = complexity_metrics.get('high_complexity_count', 0)
        very_high_complexity = complexity_metrics.get('very_high_complexity_count', 0)
        debt_hours += high_complexity * 2  # 2 hours per high complexity function
        debt_hours += very_high_complexity * 4  # 4 hours per very high complexity
        
        # Debt from quality issues
        issues = quality_metrics.get('issues_by_severity', {})
        debt_hours += issues.get('critical', 0) * 4
        debt_hours += issues.get('high', 0) * 2
        debt_hours += issues.get('medium', 0) * 1
        debt_hours += issues.get('low', 0) * 0.5
        
        # Debt from security issues
        debt_hours += security_metrics.get('critical_count', 0) * 8
        debt_hours += security_metrics.get('high_count', 0) * 4
        debt_hours += security_metrics.get('medium_count', 0) * 2
        
        # Calculate cost
        debt_cost = debt_hours * self.HOURLY_RATE
        
        # Calculate debt ratio
        total_loc = quality_metrics.get('total_loc', 1)
        debt_ratio = (debt_hours / (total_loc / 1000)) if total_loc > 0 else 0
        
        return {
            'total_hours': round(debt_hours, 1),
            'total_cost_usd': round(debt_cost, 2),
            'debt_ratio': round(debt_ratio, 2),
            'breakdown': {
                'complexity': high_complexity + very_high_complexity,
                'quality_issues': sum(issues.values()),
                'security_issues': (
                    security_metrics.get('critical_count', 0) +
                    security_metrics.get('high_count', 0) +
                    security_metrics.get('medium_count', 0)
                )
            }
        }
