"""
Quick test script to verify Repo360 works
Analyzes a small public repository
"""

import subprocess
import sys
from pathlib import Path

def test_repo360():
    """Test Repo360 on a small public repository"""
    
    print("=" * 80)
    print("REPO360 TEST - Analyzing Spring Pet Clinic")
    print("=" * 80)
    print()
    
    # Small, well-known Java repository
    test_repo = "https://github.com/spring-projects/spring-petclinic"
    
    try:
        # Run analysis
        result = subprocess.run(
            [
                sys.executable,
                "run.py",
                "--repo", test_repo,
                "--shallow",
                "--output", "test-output"
            ],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n" + "=" * 80)
            print("✓ TEST PASSED!")
            print("=" * 80)
            print()
            print("View results:")
            print("  - Dashboard: test-output/dashboard.html")
            print("  - Metrics:   test-output/metrics.json")
            print("  - Summary:   test-output/summary.json")
            print()
            
            # Check if dashboard was created
            dashboard = Path("test-output/dashboard.html")
            if dashboard.exists():
                print(f"✓ Dashboard created: {dashboard.absolute()}")
                print(f"  File size: {dashboard.stat().st_size / 1024:.1f} KB")
            else:
                print("✗ Dashboard not found!")
                return False
            
            return True
        else:
            print("\n" + "=" * 80)
            print("✗ TEST FAILED!")
            print("=" * 80)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_repo360()
    sys.exit(0 if success else 1)
