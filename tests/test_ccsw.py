"""ccsw against a throwaway HOME. Nothing here touches a real login or the network."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

CCSW = Path(__file__).resolve().parent.parent / "bin" / "ccsw"


def acct(email, org="claude_team"):
    return {"accountUuid": f"uuid-{email}", "emailAddress": email, "organizationType": org,
            "organizationName": f"{email} org"}


@pytest.fixture
def home(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text('{"keep": 1}')
    (tmp_path / ".claude" / "commands").mkdir()
    login(tmp_path, "a@x.io", "tok-a")
    return tmp_path


def login(home, email, token, org="claude_team"):
    (home / ".claude" / ".credentials.json").write_text(
        json.dumps({"claudeAiOauth": {"accessToken": token, "refreshToken": "r-" + token}, "other": 1}))
    cj = home / ".claude.json"
    data = json.loads(cj.read_text()) if cj.exists() else {"numStartups": 3}
    data["oauthAccount"] = acct(email, org)
    cj.write_text(json.dumps(data))


def ccsw(home, *args, **env):
    e = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "CCSW", "XDG_"))}
    e.update(HOME=str(home), CCSW_AUTO_SYNC_MODELS="false", **env)
    return subprocess.run([sys.executable, str(CCSW), *args], env=e, capture_output=True, text=True)


def live_token(home):
    return json.loads((home / ".claude" / ".credentials.json").read_text())["claudeAiOauth"]["accessToken"]


def test_save_use_round_trip_keeps_other_keys(home):
    assert ccsw(home, "save", "one").returncode == 0
    login(home, "b@x.io", "tok-b")
    assert ccsw(home, "save", "two").returncode == 0
    assert ccsw(home, "use", "one").returncode == 0
    assert live_token(home) == "tok-a"
    creds = json.loads((home / ".claude" / ".credentials.json").read_text())
    assert creds["other"] == 1
    assert json.loads((home / ".claude.json").read_text())["numStartups"] == 3
    assert ccsw(home, "use", "two").returncode == 0
    assert live_token(home) == "tok-b"


def test_profiles_are_private(home):
    ccsw(home, "save", "one")
    prof = home / ".config" / "account-switch" / "profiles" / "one.json"
    assert prof.stat().st_mode & 0o777 == 0o600
    assert (prof.parent.parent.stat().st_mode & 0o777) == 0o700


@pytest.mark.parametrize("bad", ["../x", "A", "a b", "-x", "x" * 30, ""])
def test_bad_names_rejected_without_writing(home, bad):
    r = ccsw(home, "save", bad)
    assert r.returncode != 0
    assert not (home / ".config" / "account-switch" / "profiles").exists()


def test_use_unknown_profile_fails_and_leaves_login(home):
    r = ccsw(home, "use", "nope")
    assert r.returncode != 0 and "no profile" in r.stderr
    assert live_token(home) == "tok-a"


def test_use_stores_rotated_token_back_before_swapping(home):
    ccsw(home, "save", "one")
    login(home, "b@x.io", "tok-b")
    ccsw(home, "save", "two")
    ccsw(home, "use", "one")
    login(home, "a@x.io", "tok-a-rotated")  # Claude Code rotated the token while "one" was live
    ccsw(home, "use", "two")
    ccsw(home, "use", "one")
    assert live_token(home) == "tok-a-rotated"


def test_isolate_builds_separate_login_and_links_the_rest(home):
    ccsw(home, "save", "one")
    login(home, "b@x.io", "tok-b")
    ccsw(home, "save", "two")
    r = ccsw(home, "use", "one", "--session", CLAUDE_CODE_SESSION_ID="sid-123")
    assert r.returncode == 0, r.stderr
    assert "sid-123" in r.stdout and "CLAUDE_CONFIG_DIR=" in r.stdout
    iso = home / ".claude-one"
    assert json.loads((iso / ".credentials.json").read_text())["claudeAiOauth"]["accessToken"] == "tok-a"
    assert json.loads((iso / ".claude.json").read_text())["oauthAccount"]["emailAddress"] == "a@x.io"
    assert (iso / "settings.json").is_symlink() and (iso / "commands").is_symlink()
    assert not (iso / ".credentials.json").is_symlink()
    assert live_token(home) == "tok-b"  # --session never touches the live login


def test_isolated_token_wins_on_later_global_use(home):
    ccsw(home, "save", "one")
    login(home, "b@x.io", "tok-b")
    ccsw(home, "save", "two")
    ccsw(home, "use", "one", "--session")
    iso_creds = home / ".claude-one" / ".credentials.json"
    iso_creds.write_text(json.dumps({"claudeAiOauth": {"accessToken": "tok-a-iso", "refreshToken": "r"}}))
    ccsw(home, "use", "one")
    assert live_token(home) == "tok-a-iso"


def test_remove_deletes_profile_and_isolated_dir_not_targets(home):
    ccsw(home, "save", "one")
    ccsw(home, "use", "one", "--session")
    assert ccsw(home, "remove", "one").returncode == 0
    assert not (home / ".claude-one").exists()
    assert (home / ".claude" / "settings.json").exists()  # symlink targets survive
    assert ccsw(home, "list").stdout.strip() == "none"


def test_models_label_uses_profile_name_and_keeps_extra_rows(home, monkeypatch):
    # offline: the Anthropic call fails, so existing rows must be kept and nothing corrupted
    settings = home / ".claude" / "settings.json"
    settings.write_text(json.dumps({"keep": 1, "modelPicker": {"options": [
        {"model": "m1", "label": "M1", "description": "x"},
        {"model": "gpt-x", "label": "Mine", "description": "y", "extra": True}], "replaceBuiltInOptions": True}}))
    ccsw(home, "save", "one")
    r = ccsw(home, "models", HTTPS_PROXY="http://127.0.0.1:1", ALL_PROXY="http://127.0.0.1:1")
    data = json.loads(settings.read_text())
    assert data["keep"] == 1
    assert {o["model"] for o in data["modelPicker"]["options"]} >= {"gpt-x"}
    assert r.returncode == 0
