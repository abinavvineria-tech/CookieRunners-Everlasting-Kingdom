"""Everlasting Bloom Studio — Hermes Agent integration adapter.

Wraps the real `hermes` CLI (hermes-agent 0.19.0) so the frontend can query
genuine Hermes capabilities without simulating them. Only subcommands in the
configured allowlist are invoked; no arbitrary shell execution is exposed.

Agent operational data stays under ~/.hermes and is queried live — never
duplicated into this project's data/ directory.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional

from flask import current_app


@dataclass
class HermesResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    command: str


class HermesAdapter:
    """Thin wrapper around the `hermes` CLI for WebUI integration."""

    def __init__(self, cli: Optional[str] = None, profile: Optional[str] = None,
                 home: Optional[str] = None):
        self.cli = cli or current_app.config.get("HERMES_CLI", "hermes")
        self.profile = profile or current_app.config.get("HERMES_PROFILE", "lilymogra-studio")
        self.home = home or current_app.config.get("HERMES_HOME")
        self.allowed = set(current_app.config.get("HERMES_ALLOWED_COMMANDS", []))

    def is_available(self) -> bool:
        return shutil.which(self.cli) is not None

    def run(self, subcommand: str, *args: str, timeout: int = 30) -> HermesResult:
        if subcommand not in self.allowed:
            return HermesResult(
                ok=False, returncode=1, stdout="",
                stderr=f"command not allowed: {subcommand}", command=subcommand,
            )
        cmd = [self.cli]
        if self.profile:
            cmd += ["--profile", self.profile]
        cmd += [subcommand, *args]

        env = None
        if self.home:
            env = dict(os.environ)
            env["HERMES_HOME"] = self.home

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout, env=env
            )
            return HermesResult(
                ok=(result.returncode == 0),
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                command=" ".join(cmd),
            )
        except FileNotFoundError:
            return HermesResult(
                ok=False, returncode=127, stdout="",
                stderr="hermes CLI not found on PATH", command=" ".join(cmd),
            )
        except subprocess.TimeoutExpired:
            return HermesResult(
                ok=False, returncode=124, stdout="",
                stderr=f"timed out after {timeout}s", command=" ".join(cmd),
            )
        except Exception as exc:  # pragma: no cover - defensive
            return HermesResult(
                ok=False, returncode=1, stdout="", stderr=f"invocation error: {exc}",
                command=" ".join(cmd),
            )

    def status(self) -> HermesResult:
        return self.run("status")

    def doctor(self) -> HermesResult:
        return self.run("doctor")

    def skills(self) -> HermesResult:
        return self.run("skills")

    def memory(self) -> HermesResult:
        return self.run("memory")

    def sessions(self) -> HermesResult:
        return self.run("sessions")

    def logs(self) -> HermesResult:
        return self.run("logs")

    def config_view(self) -> HermesResult:
        return self.run("config", "view")

    def profile_list(self) -> HermesResult:
        return self.run("profile", "list")

    def security(self) -> HermesResult:
        return self.run("security")


def get_adapter() -> HermesAdapter:
    return HermesAdapter()
