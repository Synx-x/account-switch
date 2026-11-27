# Changelog

All notable changes to this project are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-27

### Added

- Save, list, switch and remove named claude.ai logins with `ccsw` or the `/account-switch:*` commands.
- Per-session isolation. `--session` prints the command that resumes the current conversation on another account. `--open` starts it in a herdr pane.
- `ccsw run <name>` and `ccsw launchers` start Claude Code on one account without touching the others.
- A session-start hook rebuilds the `/model` list from Anthropic's live models for the active account. Check `settings.json.ccsw-bak` if you want the previous list back.
- Optional `extra_models_url` and `extra_models_owners` settings append models from an OpenAI-style gateway.

[Unreleased]: https://github.com/Synx-x/account-switch/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Synx-x/account-switch/releases/tag/v0.1.0
