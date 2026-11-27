# Security

## Reporting a vulnerability

Do not open a public issue for a vulnerability. Report it privately through GitHub's [private advisory form](https://github.com/Synx-x/account-switch/security/advisories/new).

Include the version, the steps to reproduce, and what an attacker gains. Expect an acknowledgement within a few days. Credit is given in the release notes unless you ask otherwise.

## Scope

In scope:

- Any path where `bin/ccsw` prints, logs or transmits a token.
- Any path where a profile name writes or deletes outside the store or an isolated directory.
- Any path that leaves a credential file readable by other users.

Out of scope:

- Another process running as the same user reading `~/.config/account-switch`. Profiles are as exposed as `.credentials.json` itself.
- The Anthropic API behaviour that `bin/ccsw` calls.

## Deploy checklist

Before you share a machine with this plugin installed:

- [ ] `~/.config/account-switch` is mode 700 and its profile files are mode 600
- [ ] Each `~/.claude-<name>` directory is mode 700
- [ ] Backups of your home directory exclude both locations, or encrypt them
- [ ] You removed profiles of accounts you no longer use with `ccsw remove`

## Known limitations

- Profiles hold refresh tokens in plain files. A reader of those files can act as you until you sign out of that account.
- The plugin does not touch the macOS Keychain. It refuses to run there.
- `remove` deletes the saved copy. It does not revoke the token. Sign out of the account at claude.ai to revoke it.
