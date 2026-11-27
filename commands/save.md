---
description: Save the current claude.ai login as a named profile.
argument-hint: NAME
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/bin/ccsw:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/bin/ccsw" save $ARGUMENTS`

Report the output above in one line.
