# CLI Reference — EverLink SSH

Usage: `everlink [COMMAND] [OPTIONS]`

Run `everlink` with no arguments to see the help screen.

---

## Global options

- `--version` — print the installed version and exit.

---

## Commands

### `everlink` (no command)

Display a friendly help screen with the tagline.

### `everlink version`

Print the installed version.

```text
EverLink SSH v1.0.0
```

### `everlink doctor`

Inspect Python, OpenSSH, permissions, dependencies, and config paths. Use this
to verify the environment before connecting.

### `everlink add NAME --host HOST --user USER [--port PORT] [--identity-file PATH]`

Save a host profile. Profile names must start with a letter or digit and contain
only letters, digits, spaces, underscores, dots, and hyphens. Port must be
1–65535. Identity file must be an absolute path.

```bash
everlink add web --host example.com --user alice --port 2222
everlink add home --host 192.168.1.50 --user bob
```

### `everlink list [--search TERM]`

List saved host profiles, optionally filtered by a search term matched against
name, hostname, or username.

```bash
everlink list
everlink list --search web
```

### `everlink connect TARGET`

Launch an OpenSSH session. `TARGET` is either a saved profile name or a direct
`USER@HOST` string.

```bash
everlink connect web
everlink connect alice@example.com:2222
everlink connect web --port 2222          # port override (direct connect)
everlink connect web --identity-file /path/to/key
```

The real OpenSSH client is used. Passphrase and host-key confirmation prompts
appear in your terminal. Host-key verification is left at `ask`.

### `everlink remove NAME [--yes]`

Remove a saved profile after confirmation. Pass `--yes` to skip the prompt for
scripting.

```bash
everlink remove web
everlink remove web --yes
```

### `everlink test NAME [--timeout SECONDS]`

Run a connection diagnostic: TCP reachability check followed by an SSH session
test (`ssh ... exit`). Timeout defaults to 3 seconds.

```bash
everlink test web
everlink test web --timeout 5
```

### `everlink keygen [--type TYPE] [--path PATH] [--comment COMMENT] [--passphrase PASSPHRASE]`

Create an SSH key using `ssh-keygen`. Defaults to `ed25519` at
`~/.ssh/id_ed25519`.

```bash
everlink keygen --type ed25519 --comment "everlink key"
everlink keygen --path ~/.ssh/my_key --passphrase "secret"
```

### `everlink keys [--ssh-dir DIR]`

List available public keys (public information only — private keys are never
read or displayed).

```bash
everlink keys
everlink keys --ssh-dir ~/.ssh
```

### `everlink gui [--host HOST] [--port PORT]`

Start the Flask GUI on localhost.

```bash
everlink gui
everlink gui --port 5050
```

The server binds to `127.0.0.1` by default. Debug mode is disabled.

---

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error / connection failed |
| 2 | Invalid arguments / validation error |
| 3 | OpenSSH not available |

---

## Non-interactive scripting

Use `--yes` with `remove` to skip confirmation prompts. All validation errors
print to stderr and return non-zero exit codes, suitable for scripts.
