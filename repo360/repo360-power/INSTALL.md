# Repo360 Installation Guide

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended for large repositories)
- **Disk Space**: 2GB free space for analysis cache
- **Git**: Version 2.0 or higher

### Required Software

1. **Kiro IDE** (required)
   ```bash
   # Install Kiro
   curl -fsSL https://kiro.dev/install.sh | sh
   ```

2. **Git** (required)
   ```bash
   # Check if Git is installed
   git --version
   
   # Install Git if needed:
   # macOS: brew install git
   # Ubuntu: sudo apt-get install git
   # Windows: Download from git-scm.com
   ```

3. **Language-Specific Tools** (optional, for enhanced analysis)

   **For Java:**
   ```bash
   # Java Development Kit 11+
   java -version
   
   # Maven or Gradle
   mvn --version
   gradle --version
   ```

   **For Python:**
   ```bash
   # Python 3.8+
   python --version
   
   # pip
   pip --version
   ```

   **For Node.js/TypeScript:**
   ```bash
   # Node.js 16+
   node --version
   
   # npm
   npm --version
   ```

## Installation Steps

### Step 1: Install Repo360 Power

Open Kiro and run:

```bash
kiro> install repo360 power
```

Or from command line:

```bash
kiro power install repo360
```

### Step 2: Verify Installation

```bash
kiro> list powers

# Should show:
# - repo360 (v1.0.0) - Engineering Intelligence Layer
```

### Step 3: Activate the Power

```bash
kiro> activate repo360
```

## First-Time Setup

### Configure Git Credentials (for private repositories)

If you need to analyze private repositories:

```bash
# Using HTTPS (recommended)
git config --global credential.helper store

# Or using SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add the key to GitHub: Settings > SSH and GPG keys
```

### Set up GitHub Personal Access Token (optional)

For better rate limits and private repo access:

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`
4. Copy the token

Set as environment variable:

```bash
# Linux/macOS
export GITHUB_TOKEN="your_token_here"

# Windows (PowerShell)
$env:GITHUB_TOKEN="your_token_here"

# Windows (CMD)
set GITHUB_TOKEN=your_token_here
```

## Quick Test

Test the installation by analyzing a public repository:

```bash
kiro> analyze https://github.com/spring-projects/spring-petclinic

# Expected output:
# ✓ Cloning repository...
# ✓ Analyzing code structure...
# ✓ Running quality checks...
# ✓ Scanning for security issues...
# ✓ Analyzing architecture...
# ✓ Measuring test coverage...
# ✓ Calculating technical debt...
# ✓ Generating reports...
# 
# Analysis complete!
# Overall Score: 82/100
# View detailed metrics in: repo360-output/
```

## Configuration

### Basic Configuration

Create a configuration file in your home directory:

```bash
# Create config directory
mkdir -p ~/.repo360

# Copy example configuration
cp repo360-power/examples/config.example.yml ~/.repo360/config.yml

# Edit with your preferences
nano ~/.repo360/config.yml  # or your preferred editor
```

### Repository-Specific Configuration

For project-specific settings, create `.repo360/config.yml` in your repository:

```bash
cd your-repository

mkdir -p .repo360
cp ~/.repo360/config.yml .repo360/config.yml

# Customize for this repository
nano .repo360/config.yml
```

## Troubleshooting

### Issue: "Git not found"

**Solution:**
```bash
# Install Git
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# Windows
# Download from https://git-scm.com/download/win
```

### Issue: "Permission denied (publickey)"

**Solution:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output and add to GitHub: Settings > SSH and GPG keys
```

### Issue: "Repository clone failed"

**Solution:**
1. Check internet connection
2. Verify repository URL is correct
3. For private repos, ensure you have access
4. Try with HTTPS instead of SSH (or vice versa)

### Issue: "Analysis taking too long"

**Solution:**
```bash
# For large repositories, use shallow clone
kiro> analyze https://github.com/user/large-repo --shallow

# Or increase timeout
kiro> analyze https://github.com/user/large-repo --timeout 3600
```

### Issue: "Out of memory"

**Solution:**
```bash
# Increase Java heap size (if analyzing Java projects)
export JAVA_OPTS="-Xmx4g"

# Or analyze incrementally
kiro> analyze https://github.com/user/repo --incremental
```

## Updating

### Update Repo360 Power

```bash
# Check for updates
kiro power list --updates

# Update to latest version
kiro power update repo360

# Or update all powers
kiro power update --all
```

## Uninstallation

If you need to remove Repo360:

```bash
# Uninstall the power
kiro power uninstall repo360

# Remove configuration (optional)
rm -rf ~/.repo360

# Remove analysis cache (optional)
rm -rf ~/.kiro/cache/repo360
```

## Advanced Installation

### Enterprise Deployment

For deploying across an organization:

```bash
# 1. Install Kiro on all machines via script
curl -fsSL https://kiro.dev/install.sh | sh

# 2. Install Repo360 power
kiro power install repo360

# 3. Deploy organization config
# Create shared config repository
git clone https://github.com/yourorg/repo360-config
cp repo360-config/config.yml ~/.repo360/config.yml

# 4. Set up CI/CD integration
# See enterprise-setup.md for details
```

### Docker Installation

For containerized environments:

```dockerfile
# Dockerfile
FROM kiroai/kiro:latest

# Install Repo360
RUN kiro power install repo360

# Copy organization config
COPY config.yml /root/.repo360/config.yml

# Set working directory
WORKDIR /analysis

# Default command
CMD ["kiro", "analyze-repo", "."]
```

Build and run:

```bash
# Build image
docker build -t repo360-analyzer .

# Run analysis
docker run -v $(pwd):/analysis repo360-analyzer
```

### CI/CD Pipeline Installation

See [Enterprise Setup Guide](steering/enterprise-setup.md) for complete CI/CD integration examples for:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps
- CircleCI

## Verification

After installation, verify everything works:

```bash
# 1. Check Kiro is installed
kiro --version

# 2. Check Repo360 is installed
kiro power list | grep repo360

# 3. Run test analysis
kiro> analyze https://github.com/spring-projects/spring-petclinic

# 4. Check output
ls -la repo360-output/
# Should see:
# - metrics-summary.json
# - quality-metrics.json
# - security-metrics.json
# - architecture-metrics.json
# - test-metrics.json
# - technical-debt.json
```

## Getting Help

If you encounter issues:

1. **Check logs**:
   ```bash
   cat ~/.kiro/logs/repo360.log
   ```

2. **Run in debug mode**:
   ```bash
   kiro --debug analyze https://github.com/user/repo
   ```

3. **Check documentation**:
   - [Getting Started Guide](steering/getting-started.md)
   - [Enterprise Setup](steering/enterprise-setup.md)
   - [Custom Rules](steering/custom-rules.md)

4. **Community support**:
   - GitHub Issues
   - Kiro Community Forum
   - Slack Channel

## Next Steps

After installation:

1. **Read Getting Started**: [steering/getting-started.md](steering/getting-started.md)
2. **Try example analysis**: Analyze a sample repository
3. **Configure for your needs**: Customize configuration
4. **Integrate with CI/CD**: Set up automated analysis
5. **Share with team**: Deploy organization-wide

---

**Installation complete! You're ready to analyze repositories with Repo360.**
