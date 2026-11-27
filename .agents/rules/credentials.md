# Credentials

A profile holds a refresh token. Treat it like `.credentials.json`.

- Write every credential file through `atomic_write` in `bin/ccsw`. It writes a temp file, sets the mode, then renames.
- Create profile files with mode 600 and the store directory with mode 700.
- Print only the email, plan and organization. Never print `accessToken` or `refreshToken`.
- Keep the old `settings.json` as `settings.json.ccsw-bak` before the first model-list rewrite.
- Run tests with a throwaway `HOME`, as `tests/test_ccsw.py` does. A test must never read the real login.
