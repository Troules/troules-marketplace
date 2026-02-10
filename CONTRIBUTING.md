# Contributing to SNCF Train Schedule Plugin

Thank you for your interest in contributing to this Claude Code plugin! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the issue tracker
2. If not, create a new issue with:
   - Clear description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Claude version, OS, etc.)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git fork <repository-url>
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Update documentation as needed
   - Test your changes

4. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe what your changes do
   - Reference any related issues
   - Include examples if applicable

## Development Guidelines

### Plugin Structure

The plugin follows this directory layout:

- **`.claude-plugin/plugin.json`**: Plugin manifest (name, description, author)
- **`skills/sncf-train-schedule/SKILL.md`**: Core skill instructions (keep under 2,000 words)
- **`skills/sncf-train-schedule/references/`**: Detailed API documentation
- **`skills/sncf-train-schedule/examples/`**: Usage examples
- **`skills/sncf-train-schedule/scripts/`**: Helper scripts
- **`hooks/`**: Event hooks (token validation, security checks)
- **`tests/`**: Test scripts

### Testing Your Changes

Before submitting:

1. Run structure tests (no token needed):
   ```bash
   bash tests/test-plugin-structure.sh
   ```

2. Run API tests (requires token):
   ```bash
   export NAVITIA_API_TOKEN='your-token'
   bash tests/test-api-integration.sh
   ```

3. Test the plugin with Claude Code:
   ```bash
   claude --plugin-dir .
   # Then ask: "Show me trains from Paris to Lyon"
   ```

4. Check that documentation is clear and accurate

### Documentation Standards

- Use clear, concise language
- Include code examples with expected output
- Document all API endpoints and parameters
- Keep examples up-to-date
- Use proper markdown formatting

### Code Style

- Use consistent indentation (2 spaces)
- Keep lines under 100 characters when possible
- Use meaningful variable names
- Add comments for complex logic
- Follow markdown best practices

## Areas for Contribution

### Features
- [ ] Add support for more journey filters (wheelchair access, bike transport)
- [ ] Implement fare information retrieval
- [ ] Add multi-language support
- [ ] Create journey comparison tool
- [ ] Add disruption notifications

### Documentation
- [ ] Add more usage examples
- [ ] Translate documentation to French
- [ ] Expand troubleshooting guide

### Improvements
- [ ] Optimize API call efficiency
- [ ] Improve error handling
- [ ] Better datetime parsing
- [ ] Enhance output formatting

### Testing
- [ ] Add more integration tests
- [ ] Create test fixtures
- [ ] Create mock API for testing

## API Guidelines

When working with the Navitia API:

- **Respect rate limits**: Don't make excessive requests
- **Handle errors**: Always check for and handle API errors
- **Real-time data**: Prefer `data_freshness=realtime` for current info
- **Privacy**: Never log or expose API tokens

## Versioning and Releases

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 2.1.0)
  - **MAJOR**: Incompatible API changes (e.g., remove a feature, change API format)
  - **MINOR**: New features, backward compatible (e.g., add new endpoint support)
  - **PATCH**: Bug fixes, backward compatible (e.g., fix error handling)

### Creating a Release

Releases are **automated** via GitHub Actions when CHANGELOG.md is updated on the main branch.

**Steps to create a new release:**

1. **Decide the version number** based on your changes:
   - Breaking changes → bump MAJOR (2.1.0 → 3.0.0)
   - New features → bump MINOR (2.1.0 → 2.2.0)
   - Bug fixes → bump PATCH (2.1.0 → 2.1.1)

2. **Update CHANGELOG.md** with a new version section at the top:
   ```markdown
   ## 2026-02-11 - v2.2.0: Short Feature Title

   ### New Features
   - Feature description with details
   - Another feature

   ### Bug Fixes
   - Fix description

   ### Files Modified
   - List of changed files (optional)
   ```

3. **Create a PR** with your changes (including CHANGELOG update)

4. **Merge the PR** to main branch

5. **Automated workflow runs**:
   - ✅ Extracts version from CHANGELOG.md
   - ✅ Updates `.claude-plugin/plugin.json` version field
   - ✅ Creates git tag (e.g., `v2.2.0`)
   - ✅ Creates GitHub release with extracted notes
   - ✅ Commits plugin.json update back to main

**What you need to do manually:**
- ✍️ Write detailed CHANGELOG entries
- ✍️ Choose appropriate version number
- ✍️ Craft clear release narratives

**What's automated:**
- ✅ Git tag creation
- ✅ GitHub release creation
- ✅ plugin.json version updates
- ✅ Release notes extraction

### Version Consistency

The plugin version is tracked in two places:
- **CHANGELOG.md**: Source of truth (manual updates)
- **`.claude-plugin/plugin.json`**: Auto-updated by workflow

Tests verify these stay in sync.

### Conventional Commits

Use conventional commit format for clarity:
- `feat: add journey filtering` → MINOR version
- `fix: handle API timeout` → PATCH version
- `feat!: remove deprecated API` → MAJOR version (note the `!`)

## Pull Request Review Process

1. **Automated checks**: PRs must pass CI tests
2. **Code review**: At least one maintainer will review your code
3. **Testing**: Changes will be tested in a real environment
4. **Documentation**: Ensure all docs are updated
5. **Merge**: Once approved, your PR will be merged

## Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Give credit where credit is due
- Focus on what is best for the community

## Questions?

If you have questions about contributing:

- Open an issue for discussion
- Check existing documentation
- Review the Navitia API docs at https://doc.navitia.io/

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
