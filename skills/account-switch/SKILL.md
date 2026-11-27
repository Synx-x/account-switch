---
name: account-switch
description: Use when the user wants to switch Claude Code between saved claude.ai logins (Pro, Team, Max), run one session on another account, save a new login, or refresh the /model list for the active account.
---

# Account switching

`bin/ccsw` stores each login as a named profile and swaps them. Run it through the slash commands, or call `ccsw` directly. It is on the Bash tool's PATH while the plugin is enabled.

## Pick the command

| The user wants | Run |
|---|---|
| See what is live | `/account-switch:status` |
| Save the current login | `/account-switch:save <name>` |
| Change every session's account | `/account-switch:switch <name>` |
| Move only this conversation | `/account-switch:switch <name> --session` |
| Rebuild the `/model` list | `/account-switch:models` |

## Rules

- A running session cannot change its own login. `--session` prints a resume command for a second process. Tell the user to use one copy at a time.
- A new account needs a browser sign-in first. Tell the user to run `! claude auth login`, then save the profile. Do not try to sign in for them.
- Never print or paste a token. The commands print only email, plan and organization.
- On macOS the commands refuse, because the login lives in the Keychain.
