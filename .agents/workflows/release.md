# Release

1. Run `python3 -m pytest tests` and `claude plugin validate .`. Both must pass.
2. Move the `## [Unreleased]` entries under a new version heading in `CHANGELOG.md`.
3. Set the same version in `.claude-plugin/plugin.json`.
4. Commit, then tag `v<version>` and push the tag.
5. Open the repository page and confirm the README renders.
