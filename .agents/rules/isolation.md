# Isolation

An isolated directory `~/.claude-<name>` has its own login and symlinks the rest to the main config directory.

- Create `.credentials.json` there once. Never overwrite it, because Claude Code rotates the token in place.
- Skip the entries in `ISOLATE_SKIP`. They are login state and per-process runtime files.
- Pass every profile name through `NAME_RE` before it becomes a path.
- `remove` deletes the isolated directory with `shutil.rmtree`. It unlinks symlinks and does not follow them, so the main config directory survives.
- `use` prefers the isolated directory's token over the saved profile's token. The isolated copy is the fresher one.
