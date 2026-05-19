# Contributing

## Getting started
1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-change`
4. Make your changes and test locally
5. Commit with a clear message
6. Push and open a pull request

## Commit message format
Use this pattern:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation updates
- `ci:` for pipeline changes
- `chore:` for maintenance tasks

Example: `docs: add troubleshooting guide for Kubernetes pods`

## Code standards
- Python: follow PEP 8
- Bash: use `set -e` at the top of all scripts
- Terraform: run `terraform fmt` before committing
- Docker: always pin image versions, never use `latest` in production
