"""
Complexity Metrics Calculator
Calculates ACTUAL complexity metrics from analyzed files
"""

class ComplexityCalculator:
    """Calculates complexity metrics across all files"""
    
    def calculate(self, files):
        """
        Calculate aggregate complexity metrics from analyzed files
        
        Args:
            files: List of file analysis results
        
        Returns:
            Dictionary of complexity metrics (ACTUAL calculations, no assumptions)
        """
        complexities = []
        total_functions = 0
        high_complexity_count = 0
        very_high_complexity_count = 0
        
        for file_result in files:
            # Extract complexity from functions/methods
            functions = file_result.get('functions', []) + file_result.get('methods', [])
            
            for func in functions:
                complexity = func.get('complexity', 0)
                if complexity > 0:
                    complexities.append(complexity)
                    total_functions += 1
                    
                    if complexity > 15:
                        very_high_complexity_count += 1
                    elif complexity > 10:
                        high_complexity_count += 1
        
        if not complexities:
            return {
                'average_complexity': 0,
                'max_complexity': 0,
                'total_functions': 0,
                'high_complexity_count': 0,
                'very_high_complexity_count': 0
            }
        
        return {
            'average_complexity': round(sum(complexities) / len(complexities), 2),
            'max_complexity': max(complexities),
            'min_complexity': min(complexities),
            'total_functions': total_functions,
            'high_complexity_count': high_complexity_count,
            'very_high_complexity_count': very_high_complexity_count,
            'complexity_distribution': {
                'simple': len([c for c in complexities if c <= 5]),
                'moderate': len([c for c in complexities if 5 < c <= 10]),
                'complex': len([c for c in complexities if 10 < c <= 15]),
                'very_complex': len([c for c in complexities if c > 15])
            }
        }
