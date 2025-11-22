# GitHub Actions CI/CD Setup Guide

## Overview

This CI/CD pipeline automatically:

1. ✅ **Tests** your Python code with flake8 linting
2. 🔢 **Auto-increments** version tags (patch version)
3. 🐳 **Builds** Docker image
4. 📤 **Pushes** to Docker Hub with multiple tags
5. 🏷️ **Creates** Git release tags

## Required GitHub Secrets

You need to add these secrets to your GitHub repository:

### 1. Navigate to Repository Settings

- Go to: `https://github.com/Automation-Scripts-By-Default/Birthday-Agent/settings/secrets/actions`
- Click **"New repository secret"**

### 2. Add Docker Hub Credentials

#### DOCKER_HUB_USERNAME

- **Name**: `DOCKER_HUB_USERNAME`
- **Value**: `johndoe` (your Docker Hub username)

#### DOCKER_HUB_TOKEN

- **Name**: `DOCKER_HUB_TOKEN`
- **Value**: Your Docker Hub Access Token

**To create a Docker Hub Access Token:**

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to Account Settings → Security → [Access Tokens](https://hub.docker.com/settings/security)
3. Click **"New Access Token"**
4. Name it: `github-actions-birthday-agent`
5. Permissions: **Read, Write, Delete**
6. Copy the token (you won't see it again!)
7. Paste it as the secret value in GitHub

## Version Tagging Strategy

The pipeline uses **Semantic Versioning** (semver):

- Format: `vMAJOR.MINOR.PATCH` (e.g., v1.0.0, v1.0.1, v1.2.3)
- **Patch version** auto-increments on every push to main
- Starts at `v0.0.1` if no tags exist

### Version Bumping

**Automatic (current setup):**

- Every push to `main` → patch version +1
- `v1.0.0` → `v1.0.1` → `v1.0.2` ...

**Manual version bump** (for major/minor releases):

```bash
# For minor version bump (v1.0.5 → v1.1.0)
git tag -a v1.1.0 -m "Release v1.1.0 - New features"
git push origin v1.1.0

# For major version bump (v1.5.3 → v2.0.0)
git tag -a v2.0.0 -m "Release v2.0.0 - Breaking changes"
git push origin v2.0.0
```

## Docker Image Tags

Each build creates **4 tags**:

1. `lucasdadev/homelab:v1.0.5` - Specific version
2. `lucasdadev/homelab:latest` - Latest build
3. `lucasdadev/homelab:birthday-agent-v1.0.5` - Named version
4. `lucasdadev/homelab:birthday-agent-latest` - Named latest

### Pull Commands

```bash
# Pull specific version
docker pull lucasdadev/homelab:v1.0.5

# Pull latest
docker pull lucasdadev/homelab:latest

# Pull with project name
docker pull lucasdadev/homelab:birthday-agent-latest
```

## Workflow Triggers

### Automatic Triggers

- ✅ Push to `main` branch → Full pipeline (test, build, push, tag)
- ✅ Pull request → Tests only (no build/deploy)

### Manual Trigger

You can also trigger manually from GitHub Actions UI:

1. Go to Actions tab
2. Select "CI/CD - Test, Build & Deploy"
3. Click "Run workflow"

## Pipeline Jobs

### 1. Test Job

- Runs on every push and PR
- Lints Python code with flake8
- Validates syntax of Python files
- Must pass for pipeline to continue

### 2. Version Job

- Only runs on push to main (after tests pass)
- Reads latest git tag
- Increments patch version
- Outputs new version for next jobs

### 3. Build and Push Job

- Only runs on push to main (after version)
- Builds Docker image
- Pushes to Docker Hub with 4 tags
- Uses Docker layer caching for faster builds

### 4. Tag Release Job

- Only runs after successful build
- Creates git tag with new version
- Pushes tag to GitHub

### 5. Notify Job

- Runs at the end
- Creates build summary in Actions UI
- Shows version and Docker pull commands

## Monitoring Builds

### View Pipeline Status

- Go to: `https://github.com/Automation-Scripts-By-Default/Birthday-Agent/actions`
- Click on latest workflow run
- See all jobs and their status

### Check Docker Hub

- Visit: `https://hub.docker.com/r/lucasdadev/homelab/tags`
- See all pushed images and tags

## Troubleshooting

### Build fails with "Invalid credentials"

**Solution:** Verify Docker Hub secrets are correct

```bash
# In GitHub repo settings, check:
DOCKER_HUB_USERNAME = lucasdadev
DOCKER_HUB_TOKEN = <your-token>
```

### Version not incrementing

**Solution:** Check if git tags are pushed

```bash
# List all tags
git tag

# Fetch remote tags
git fetch --tags

# Delete wrong tags locally and remotely
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### Build succeeds but image not in Docker Hub

**Solution:** Check Docker Hub token permissions

- Token needs: **Read, Write, Delete**
- Create new token if needed

### Self-hosted runner not working

**Solution:** Ensure your runner is online

- Go to Settings → Actions → Runners
- Check if runner shows "Idle" or "Active"
- Restart runner if needed

## Using the Image on Your Server

### Pull and Run

```bash
# Pull latest image
docker pull lucasdadev/homelab:birthday-agent-latest

# Stop old container
docker stop birthday-agent
docker rm birthday-agent

# Run new container
docker run -d \
  --name birthday-agent \
  --env-file .env \
  --network homelab-network \
  --restart unless-stopped \
  lucasdadev/homelab:birthday-agent-latest
```

### Or use Docker Compose

Update your `docker-compose.yml`:

```yaml
services:
  birthday-agent:
    image: lucasdadev/homelab:birthday-agent-latest
    container_name: birthday-agent
    env_file:
      - .env
    networks:
      - homelab-network
    restart: unless-stopped
```

Then:

```bash
docker-compose pull
docker-compose up -d
```

## Best Practices

1. ✅ **Always test locally** before pushing to main
2. ✅ **Use pull requests** for code review
3. ✅ **Monitor Actions tab** for build status
4. ✅ **Tag major/minor releases manually** when needed
5. ✅ **Keep Docker Hub token secure** - never commit it
6. ✅ **Use specific version tags** in production
7. ✅ **Check Docker Hub regularly** for old unused images

## Example Workflow

```bash
# 1. Make changes locally
git checkout -b feature/new-feature
# ... make changes ...

# 2. Test locally
python main.py
docker build -t test .

# 3. Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 4. Create pull request
# - Tests run automatically
# - Review and merge to main

# 5. After merge to main
# - Tests run
# - Version bumps (e.g., v1.0.5 → v1.0.6)
# - Docker image builds and pushes
# - Git tag created
# - Ready to deploy!

# 6. Deploy on server
ssh user@server
docker pull lucasdadev/homelab:v1.0.6
docker-compose up -d
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub](https://hub.docker.com/r/lucasdadev/homelab)
- [Semantic Versioning](https://semver.org/)
