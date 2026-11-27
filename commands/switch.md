---
description: Switch to a saved Claude login. Add --session to leave the live login alone and get the command that resumes this conversation on that account (--open splits a herdr pane).
argument-hint: <name> [--session [--open]]
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/bin/ccsw:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/bin/ccsw" use $ARGUMENTS`

Report the output above in one line. After a plain switch, say a running session picks the new login up on its next request. If it says no profile, tell the user to run `! claude auth login` for that account, then `/account-switch:save <name>`.
