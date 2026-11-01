"""Tests for EverLink SSH security helpers."""

import pytest

from everlink.security import (
    ValidationError,
    validate_hostname,
    validate_port,
    validate_profile_name,
    validate_username,
    validate_identity_file,
    constant_time_compare,
    is_path_within,
)


def test_validate_port_valid():
    assert validate_port(22) == 22
    assert validate_port("22") == 22
    assert validate_port(1) == 1
    assert validate_port(65535) == 65535


def test_validate_port_invalid():
    with pytest.raises(ValidationError):
        validate_port(0)
    with pytest.raises(ValidationError):
        validate_port(65536)
    with pytest.raises(ValidationError):
        validate_port(-1)
    with pytest.raises(ValidationError):
        validate_port("not-a-port")


def test_validate_hostname_valid():
    assert validate_hostname("example.com") == "example.com"
    assert validate_hostname("192.168.1.1") == "192.168.1.1"
    assert validate_hostname("localhost") == "localhost"
    assert validate_hostname("::1") == "::1"
    assert validate_hostname("2001:db8::1") == "2001:db8::1"


def test_validate_hostname_invalid():
    with pytest.raises(ValidationError):
        validate_hostname("")
    with pytest.raises(ValidationError):
        validate_hostname("-bad.com")
    with pytest.raises(ValidationError):
        validate_hostname("bad-.com")
    with pytest.raises(ValidationError):
        validate_hostname("bad..com")
    with pytest.raises(ValidationError):
        validate_hostname("not valid")


def test_validate_profile_name_valid():
    assert validate_profile_name("myhost") == "myhost"
    assert validate_profile_name("Host 1") == "Host 1"
    assert validate_profile_name("a.b-c_d") == "a.b-c_d"


def test_validate_profile_name_invalid():
    with pytest.raises(ValidationError):
        validate_profile_name("")
    with pytest.raises(ValidationError):
        validate_profile_name("-bad")
    with pytest.raises(ValidationError):
        validate_profile_name("a" * 70)


def test_validate_username_valid():
    assert validate_username("root") == "root"
    assert validate_username("user.name") == "user.name"
    assert validate_username("user_name") == "user_name"


def test_validate_username_invalid():
    with pytest.raises(ValidationError):
        validate_username("")
    with pytest.raises(ValidationError):
        validate_username("bad user")
    with pytest.raises(ValidationError):
        validate_username("bad@user")


def test_validate_identity_file():
    assert validate_identity_file(None) is None
    assert validate_identity_file("") is None
    assert validate_identity_file("/home/user/.ssh/id_ed25519") == "/home/user/.ssh/id_ed25519"
    with pytest.raises(ValidationError):
        validate_identity_file("relative/path")


def test_constant_time_compare():
    assert constant_time_compare("abc", "abc") is True
    assert constant_time_compare("abc", "abd") is False


def test_is_path_within():
    base = Path_tmp = None  # noqa
    from pathlib import Path
    base = Path("/data")
    assert is_path_within(base, Path("/data/foo")) is True
    assert is_path_within(base, Path("/data/foo/bar")) is True
    assert is_path_within(base, Path("/etc/passwd")) is False
    assert is_path_within(base, Path("/data2/foo")) is False
