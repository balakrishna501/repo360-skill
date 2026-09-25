#!/usr/bin/env python3
"""
Repo360 - Deep Code Analysis Engine
Entry point for repository analysis
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import Repo360Analyzer

def main():
    parser = argparse.ArgumentParser(
        description='Repo360 - Deep Code Analysis for GitHub Repositories'
    )
    parser.add_argument(
        '--repo',
        required=True,
        help='GitHub repository URL (e.g., https://github.com/user/repo)'
    )
    parser.add_argument(
        '--branch',
        default='main',
        help='Branch to analyze (default: main)'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for reports (default: output)'
    )
    parser.add_argument(
        '--shallow',
        action='store_true',
        help='Perform shallow clone for faster analysis'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip test file analysis'
    )
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = Repo360Analyzer(
        repo_url=args.repo,
        branch=args.branch,
        output_dir=args.output,
        shallow=args.shallow,
        skip_tests=args.skip_tests
    )
    
    # Run analysis
    print("=" * 80)
    print("Repo360 - Deep Code Analysis Engine")
    print("=" * 80)
    print(f"Repository: {args.repo}")
    print(f"Branch: {args.branch}")
    print(f"Output: {args.output}")
    print("=" * 80)
    
    try:
        analyzer.run()
        print("\n✓ Analysis complete!")
        print(f"✓ View dashboard: {args.output}/dashboard.html")
        print(f"✓ View metrics: {args.output}/metrics.json")
    except Exception as e:
        print(f"\n✗ Analysis failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
