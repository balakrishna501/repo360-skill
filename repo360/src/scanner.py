"""
File Scanner
Discovers and categorizes source files
"""

from pathlib import Path
from collections import defaultdict

class FileScanner:
    """Scans repository for source files"""
    
    # File extensions to analyze
    EXTENSIONS = {
        'java': ['.java'],
        'python': ['.py'],
        'javascript': ['.js', '.jsx'],
        'typescript': ['.ts', '.tsx'],
        'go': ['.go'],
        'ruby': ['.rb'],
        'php': ['.php'],
        'csharp': ['.cs'],
        'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
        'rust': ['.rs']
    }
    
    # Directories to skip
    SKIP_DIRS = {
        'node_modules', 'vendor', 'target', 'build', 'dist',
        '.git', '.svn', '__pycache__', '.pytest_cache',
        'venv', 'env', '.venv', 'virtualenv',
        'bin', 'obj', 'packages', '.idea', '.vscode'
    }
    
    # Test file patterns
    TEST_PATTERNS = [
        'test_', '_test.', '.test.', '.spec.',
        '/tests/', '/test/', '__tests__'
    ]
    
    def __init__(self, skip_tests=False):
        self.skip_tests = skip_tests
    
    def scan(self, repo_path):
        """Scan repository and return list of source files"""
        
        repo_path = Path(repo_path)
        source_files = []
        
        for file_path in repo_path.rglob('*'):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip if in excluded directory
            if any(skip_dir in file_path.parts for skip_dir in self.SKIP_DIRS):
                continue
            
            # Check if it's a source file
            if not self._is_source_file(file_path):
                continue
            
            # Skip test files if requested
            if self.skip_tests and self._is_test_file(file_path):
                continue
            
            source_files.append(file_path)
        
        return sorted(source_files)
    
    def _is_source_file(self, file_path):
        """Check if file is a source code file"""
        
        suffix = file_path.suffix.lower()
        for language, extensions in self.EXTENSIONS.items():
            if suffix in extensions:
                return True
        return False
    
    def _is_test_file(self, file_path):
        """Check if file is a test file"""
        
        file_str = str(file_path).lower()
        return any(pattern in file_str for pattern in self.TEST_PATTERNS)
    
    def get_language(self, file_path):
        """Determine programming language of file"""
        
        suffix = file_path.suffix.lower()
        for language, extensions in self.EXTENSIONS.items():
            if suffix in extensions:
                return language
        return 'unknown'
    
    def get_language_stats(self, files):
        """Get statistics by programming language"""
        
        stats = defaultdict(lambda: {'files': 0, 'lines': 0})
        
        for file_path in files:
            language = self.get_language(file_path)
            stats[language]['files'] += 1
            
            # Count lines
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
                    stats[language]['lines'] += lines
            except:
                pass
        
        # Calculate percentages
        total_lines = sum(data['lines'] for data in stats.values())
        for language in stats:
            if total_lines > 0:
                stats[language]['percentage'] = round(
                    (stats[language]['lines'] / total_lines) * 100, 2
                )
            else:
                stats[language]['percentage'] = 0
        
        return dict(stats)
