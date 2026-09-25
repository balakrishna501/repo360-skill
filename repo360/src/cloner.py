"""
Repository Cloner
Handles git clone operations
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class RepositoryCloner:
    """Clones GitHub repositories for analysis"""
    
    def __init__(self, work_dir='work'):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    def clone(self, repo_url, branch='main', shallow=False):
        """Clone repository to work directory"""
        
        # Extract repo name from URL
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        target_dir = self.work_dir / f"{repo_name}_{timestamp}"
        
        # Build git clone command
        cmd = ['git', 'clone']
        
        if shallow:
            cmd.extend(['--depth', '1'])
        
        cmd.extend(['-b', branch, repo_url, str(target_dir)])
        
        # Execute clone
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  ✓ Cloned to: {target_dir}")
            return target_dir
        except subprocess.CalledProcessError as e:
            # Try alternative branch names
            if branch == 'main':
                print(f"  Branch 'main' not found, trying 'master'...")
                cmd[-2] = 'master'
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"  ✓ Cloned to: {target_dir}")
                return target_dir
            else:
                raise Exception(f"Failed to clone repository: {e.stderr}")
    
    def get_commit_info(self, repo_path):
        """Get current commit information"""
        
        try:
            # Get commit hash
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            commit_hash = result.stdout.strip()
            
            # Get commit author and date
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%an|%ae|%ai'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            author, email, date = result.stdout.strip().split('|')
            
            return {
                'hash': commit_hash,
                'author': author,
                'email': email,
                'date': date
            }
        except Exception as e:
            return {'error': str(e)}
