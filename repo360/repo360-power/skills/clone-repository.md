# Clone Repository Skill

## Purpose
Clone a GitHub repository to a local directory for analysis, supporting specific branches and handling authentication when needed.

## Usage

```
Clone https://github.com/username/repository branch:main
```

## Parameters

- **repository_url** (required): Full GitHub repository URL
- **branch** (optional): Branch name to checkout (default: main/master)
- **depth** (optional): Shallow clone depth for large repos
- **target_dir** (optional): Custom directory name

## Process

### Step 1: Validate URL
```bash
# Check if URL is valid GitHub URL
# Formats supported:
# - https://github.com/user/repo
# - https://github.com/user/repo.git
# - git@github.com:user/repo.git
```

### Step 2: Prepare Directory
```bash
# Create analysis directory
mkdir -p repo360-analysis
cd repo360-analysis

# Generate unique directory name
repo_name=$(basename $repository_url .git)
timestamp=$(date +%Y%m%d_%H%M%S)
target_dir="${repo_name}_${timestamp}"
```

### Step 3: Clone Repository
```bash
# For public repositories
git clone $repository_url $target_dir

# For specific branch
git clone -b $branch $repository_url $target_dir

# For shallow clone (faster for large repos)
git clone --depth 1 -b $branch $repository_url $target_dir
```

### Step 4: Verify Clone
```bash
cd $target_dir

# Verify git repository
git status

# Get commit information
git log -1 --format="%H %an %ae %ai"

# Get branch information
git branch -v
```

### Step 5: Gather Metadata
```json
{
  "repository_url": "https://github.com/user/repo",
  "branch": "main",
  "commit_hash": "abc123...",
  "commit_author": "John Doe",
  "commit_date": "2024-01-15T10:30:00Z",
  "clone_path": "/path/to/repo360-analysis/repo_20240115_103000",
  "clone_timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Handling

### Repository Not Found
```
Error: Repository not found at https://github.com/user/repo
- Verify URL is correct
- Check if repository is private (may need authentication)
- Ensure you have access permissions
```

### Authentication Required
```
Error: Authentication required
- For private repos, configure Git credentials:
  git config --global credential.helper store
- Or use personal access token:
  git clone https://token@github.com/user/repo
```

### Branch Not Found
```
Error: Branch 'develop' not found
- Available branches: main, staging, feature-x
- Default branch: main
```

### Network Issues
```
Error: Failed to clone (network timeout)
- Check internet connection
- Retry with: git clone --depth 1 (faster)
- Check GitHub status
```

## Examples

### Example 1: Clone Main Branch
```bash
# Input
Clone https://github.com/spring-projects/spring-boot

# Output
✓ Cloning spring-boot from GitHub...
✓ Checked out branch: main
✓ Latest commit: abc123 by John Doe (2024-01-15)
✓ Clone path: /repo360-analysis/spring-boot_20240115_103000
```

### Example 2: Clone Specific Branch
```bash
# Input
Clone https://github.com/django/django branch:stable/4.2.x

# Output
✓ Cloning django from GitHub...
✓ Checked out branch: stable/4.2.x
✓ Latest commit: def456 by Jane Smith (2024-01-10)
✓ Clone path: /repo360-analysis/django_20240115_103000
```

### Example 3: Shallow Clone (Large Repo)
```bash
# Input
Clone https://github.com/torvalds/linux --depth 1

# Output
✓ Performing shallow clone (depth: 1)...
✓ Cloning linux from GitHub...
✓ Checked out branch: master
✓ Latest commit: 789abc (2024-01-15)
✓ Clone path: /repo360-analysis/linux_20240115_103000
Note: Shallow clone - history limited to 1 commit
```

## Output

Returns a JSON object with clone information:

```json
{
  "success": true,
  "repository": {
    "url": "https://github.com/user/repo",
    "name": "repo",
    "branch": "main",
    "commit": "abc123...",
    "author": "John Doe",
    "date": "2024-01-15T10:30:00Z"
  },
  "clone": {
    "path": "/full/path/to/repo360-analysis/repo_20240115_103000",
    "timestamp": "2024-01-15T10:30:00Z",
    "shallow": false
  }
}
```

## Best Practices

1. **Always use fresh clones** for analysis to ensure clean state
2. **Use shallow clones** for large repositories to save time and space
3. **Verify clone success** before proceeding with analysis
4. **Store metadata** about clone for reporting
5. **Clean up** old clones after analysis complete

## Integration

This skill is typically the first step in the analysis workflow:

```
1. Clone Repository (this skill)
2. Discover files and structure
3. Run language-specific analysis
4. Generate metrics
5. Clean up clone
```

## Performance Considerations

### Small Repository (<10 MB)
- Full clone: ~5 seconds
- Recommended: Full clone

### Medium Repository (10-100 MB)
- Full clone: ~30 seconds
- Recommended: Full clone or depth 10

### Large Repository (>100 MB)
- Full clone: >2 minutes
- Recommended: Shallow clone (depth 1)

### Very Large Repository (>1 GB)
- Full clone: >10 minutes
- Recommended: Shallow clone + sparse checkout if possible

## Security Considerations

1. **Never log credentials** in output
2. **Don't commit .git directory** in analysis output
3. **Handle private keys** securely
4. **Use tokens** instead of passwords
5. **Clean up clones** containing sensitive data

## Troubleshooting

### Problem: Clone is slow
**Solution**: Use `--depth 1` for shallow clone

### Problem: Out of disk space
**Solution**: Clean up old clones in repo360-analysis directory

### Problem: SSL certificate error
**Solution**: Update Git or temporarily use `GIT_SSL_NO_VERIFY=true`

### Problem: Rate limited by GitHub
**Solution**: Authenticate with personal access token
