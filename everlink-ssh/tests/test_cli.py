"""Tests for EverLink SSH CLI parsing and behavior."""

from unittest.mock import patch

import pytest

from everlink.cli import build_parser, main


def test_help_output(capsys):
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--help"])
    assert exc.value.code == 0


def test_version_flag(capsys):
    assert main(["--version"]) == 0


def test_no_args_prints_help(capsys):
    code = main([])
    assert code == 0


def test_add_invalid_port():
    code = main(["add", "web", "--host", "example.com", "--user", "alice", "--port", "99999"])
    assert code == 2


def test_add_invalid_hostname():
    code = main(["add", "web", "--host", "bad host", "--user", "alice"])
    assert code == 2


def test_add_valid(monkeypatch, tmp_path):
    # Point DB at a temp location via env override
    monkeypatch.setenv("EVERLINK_APP_DIR", str(tmp_path))
    code = main(["add", "web", "--host", "example.com", "--user", "alice", "--port", "2222"])
    assert code == 0


def test_connect_missing_profile():
    code = main(["connect", "nosuchprofile"])
    assert code == 2


@patch("everlink.cli.ssh_available", return_value=False)
def test_connect_when_ssh_missing(mock_avail, monkeypatch, tmp_path):
    monkeypatch.setenv("EVERLINK_APP_DIR", str(tmp_path))
    code = main(["add", "web", "--host", "example.com", "--user", "alice"])
    assert code == 0
    code = main(["connect", "web"])
    assert code == 3
