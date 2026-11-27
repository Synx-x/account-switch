# Contributing

The most confusing part of this repo is that `bin/ccsw` edits real login files. Every test runs it against a throwaway `HOME` for that reason. Never point a test at your own home directory.

## Setup

```bash
git clone https://github.com/Synx-x/account-switch
cd account-switch
python3 -m pip install pytest
```

## Verify

```bash
python3 -m pytest tests
claude plugin validate .
```

All 14 tests pass. A lower number means a test did not run. The validator prints one warning about a missing icon, which is expected.

## Run

```bash
claude --plugin-dir . -p "/account-switch:status"
```

Set `CCSW_HOME` to a scratch directory first, so the run does not write to your real profile store.

## Branching

- Branch from `main`.
- One concern per branch.
- Write commit subjects in the imperative, such as "Reject names with a slash".

## Before opening a pull request

- [ ] Tests pass locally
- [ ] A changelog entry is added under `## [Unreleased]`, if the change is user-visible
- [ ] No secrets, local paths, or build output in the diff
- [ ] The description says what breaks, if anything does

## Reporting a bug

Include the version, the command you ran, and what you expected instead. Remove any token from pasted output. A reproduction that fails in one paste is worth ten paragraphs of description.
