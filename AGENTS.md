# AGENTS.md

Canonical project guide. Every AI tool reads this file. Every other tool file in the repo is a short bridge that imports it. Edit conventions here, never in a bridge.

## What this is

account-switch is a Claude Code plugin. It saves several claude.ai logins as named profiles and swaps between them, for every session or for one session. Its one script, `bin/ccsw`, moves refresh tokens around. A bug there can lock a user out of an account or leak a credential.

## Repo map

| Path | Holds |
|---|---|
| `bin/ccsw` | The whole tool. Standard library only. |
| `commands/` | Slash commands that call `bin/ccsw`. |
| `hooks/hooks.json` | The session-start hook that syncs the `/model` list. |
| `skills/account-switch/` | The skill that tells Claude when to use the commands. |
| `tests/` | Tests that run `bin/ccsw` against a throwaway `HOME`. |
| `.claude-plugin/` | The plugin manifest and the one-plugin marketplace file. |
| `.agents/rules/` | Conventions, read on demand. |

## Stack

| Layer | Choice |
|---|---|
| Language | Python 3.9 or newer, standard library only |
| Test | pytest |
| CI | GitHub Actions |

## Build and run

```bash
python3 -m pytest tests
claude plugin validate .
claude --plugin-dir . -p "/account-switch:status"
```

## Environment

Every variable is documented in `.env.example`. None is required and none holds a secret.

## Branching

Branch from `main`. One concern per branch. Write commit subjects in the imperative.

## Golden rules

1. **Never print or log a token.** A pasted terminal log would leak a working credential. See `.agents/rules/credentials.md`.
2. **Write credential files only through `atomic_write`.** A crash mid-write would corrupt a login. See `.agents/rules/credentials.md`.
3. **Never overwrite an isolated directory's `.credentials.json`.** Claude Code rotates the token in place, and an overwrite revives a dead token. See `.agents/rules/isolation.md`.
4. **Validate every profile name with `NAME_RE`.** An unchecked name becomes a path and escapes the store. See `.agents/rules/isolation.md`.
5. **Tests use a throwaway `HOME`.** A test against the real home swaps your real login. See `.agents/rules/credentials.md`.

## Rules index

| Working on… | Read |
|---|---|
| Reading or writing a login | `.agents/rules/credentials.md` |
| Isolated config directories | `.agents/rules/isolation.md` |
| Cutting a release | `.agents/workflows/release.md` |

## Coding style

Keep `bin/ccsw` one file with no third-party imports. Fail with `die()` and a message that names the fix.

## Adding things

- **A new command:** add a function in `bin/ccsw`, route it in `main`, add `commands/NAME.md`, and add a test.
- **A new setting:** add it to `userConfig` in `.claude-plugin/plugin.json`, read it with `opt()`, and list it in `.env.example`.

## Tooling

Claude Code reads `CLAUDE.md` and Gemini CLI reads `GEMINI.md`. Both import this file.
