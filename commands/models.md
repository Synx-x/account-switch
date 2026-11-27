---
description: Rebuild the /model list from Anthropic's live models for the active account.
argument-hint: 
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/bin/ccsw:*)
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/bin/ccsw" models`

Report the output above in one line.
