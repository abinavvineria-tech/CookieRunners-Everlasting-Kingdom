"""Tests for EverLink SSH database layer."""

import os
import tempfile

import pytest

from everlink import database as db


@pytest.fixture
def conn():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    connection = db.get_connection(path)
    db.init_db(path)
    yield connection
    connection.close()
    os.unlink(path)


def test_add_and_get_host(conn):
    hid = db.add_host(conn, "web", "example.com", "alice", 2222, "/home/alice/.ssh/id")
    row = db.get_host(conn, "web")
    assert row is not None
    assert row["hostname"] == "example.com"
    assert row["username"] == "alice"
    assert row["port"] == 2222
    assert row["identity_file"] == "/home/alice/.ssh/id"


def test_list_hosts(conn):
    db.add_host(conn, "b", "b.example.com", "u", 22)
    db.add_host(conn, "a", "a.example.com", "u", 22)
    hosts = db.list_hosts(conn)
    names = [h["name"] for h in hosts]
    assert names == ["a", "b"]


def test_list_hosts_search(conn):
    db.add_host(conn, "alpha", "alpha.example.com", "u", 22)
    db.add_host(conn, "beta", "beta.example.com", "u", 22)
    hosts = db.list_hosts(conn, search="alpha")
    assert len(hosts) == 1
    assert hosts[0]["name"] == "alpha"


def test_update_host(conn):
    hid = db.add_host(conn, "web", "example.com", "alice", 22)
    db.update_host(conn, hid, port=2222, username="bob")
    row = db.get_host_by_id(conn, hid)
    assert row["port"] == 2222
    assert row["username"] == "bob"


def test_delete_host(conn):
    hid = db.add_host(conn, "web", "example.com", "alice", 22)
    db.delete_host(conn, hid)
    assert db.get_host(conn, "web") is None


def test_record_and_recent_attempts(conn):
    db.record_attempt(conn, "web", "alice@example.com:22", "ok", "connected")
    attempts = db.recent_attempts(conn, limit=5)
    assert len(attempts) == 1
    assert attempts[0]["status"] == "ok"


def test_add_and_list_keys(conn):
    db.add_key(conn, "mykey", "/home/user/.ssh/mykey.pub", "SHA256:xxx")
    keys = db.list_keys_db(conn)
    assert len(keys) == 1
    assert keys[0]["name"] == "mykey"


def test_unique_name_constraint(conn):
    db.add_host(conn, "web", "example.com", "alice", 22)
    with pytest.raises(Exception):
        db.add_host(conn, "web", "other.com", "bob", 22)
