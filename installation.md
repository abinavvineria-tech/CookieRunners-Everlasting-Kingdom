# Cookie Runner Studio — Hermes Agent Installation Guide

**Edition:** 2026  
**Agent display name:** EverBloom Nexus  
**Technical profile:** `everbloomnexus`  
**Primary device:** OnePlus Pad Go · Android 14  
**Primary environment:** Native Termux · Zsh  
**Hermes data directory:** `~/.hermes`

This guide covers all three parts of the Cookie Runner setup:

1. Install Hermes Agent in native Termux using the installer already used on this device.
2. Install or inspect Hermes Agent from its GitHub source repository.
3. Configure the Cookie Runner Studio environment, EverBloom Nexus profile, memory, skills, and Telegram.

> **Important:** The Termux installer in this guide is community-maintained. It is not the official Hermes project installer. Check its current README and release notes before using it. Do not run two installation methods over an existing installation without understanding how they manage Python packages, executables, and data.

---

## Part 1 — Native Termux installation

### 1.1 Device prerequisites

Open Termux and check the device environment:

```bash
uname -m
getprop ro.build.version.release
echo "$SHELL"
pkg update
pkg upgrade
pkg install -y git curl wget python
```

The expected Android ARM64 architecture is usually `aarch64`.

### 1.2 The community Termux installer

This is the command used for the existing installation:

```bash
curl -fsSL --retry 6 --retry-all-errors \
  https://raw.githubusercontent.com/adybag14-cyber/termux-hermes/main/install.sh | bash
```

**Safer review-first method for a new installation:**

```bash
mkdir -p ~/hermes-installer-review
cd ~/hermes-installer-review

curl -fsSL \
  https://raw.githubusercontent.com/adybag14-cyber/termux-hermes/main/install.sh \
  -o install.sh

less install.sh
```

Review the script and the repository's README before running it:

```bash
bash install.sh
```

Only run a script after deciding that you trust its source and understand the changes it makes.

### 1.3 Verify the installation

```bash
command -v hermes
hermes --version
hermes --help
hermes doctor
```

If a command is unavailable, consult `hermes --help` and the installer's documentation. Do not assume commands are identical across releases.

### 1.4 Back up the existing Hermes data

Do this before upgrades, profile changes, or migrations:

```bash
mkdir -p "$HOME/hermes-backups"

tar -czf "$HOME/hermes-backups/hermes-backup-$(date +%Y%m%d-%H%M%S).tar.gz" \
  -C "$HOME" .hermes
```

Keep the archive private. It may contain credentials, chat sessions, and personal data.

---

## Part 2 — GitHub source installation and maintenance

### 2.1 Official source repository

Hermes Agent's upstream source repository is:

- https://github.com/NousResearch/hermes-agent

The community Termux installer repository used on this device is:

- https://github.com/adybag14-cyber/termux-hermes

These are different repositories with different purposes. The upstream repository is the project source; the community repository provides a Termux-oriented installation route.

### 2.2 Inspect the upstream repository

Install Git if needed:

```bash
pkg install -y git
```

Clone the upstream repository into a separate inspection directory:

```bash
mkdir -p ~/src
cd ~/src

git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

git remote -v
git status
```

This clones the source code for inspection. **It does not automatically install or replace the Hermes executable already used by Termux.**

### 2.3 Read the upstream installation instructions

Before installing from source, read the repository's current documentation:

```bash
less README.md
```

Look for the current installation guide and follow the instructions specifically intended for your environment. If the upstream instructions do not support native Termux directly, do not force the Linux installation steps onto Android.

For a supported Linux environment, the project may document its own installer or package workflow. Use the exact current command from the upstream documentation rather than copying an old command into this guide.

### 2.4 Keep source checkout separate from the working installation

Recommended separation:

```text
~/src/hermes-agent/       # upstream source checkout
~/.hermes/                # user data and configuration
~/hermes-backups/         # private backups
```

Do not copy source files over `~/.hermes`. Do not run a second installer over the current working setup just to obtain a Git checkout.

### 2.5 Updating the source checkout

When you intentionally want to update the inspection copy:

```bash
cd ~/src/hermes-agent
git fetch --all --prune
git status
```

Review local changes and upstream release notes before deciding whether to update the checkout. Fetching changes is not the same as updating the installed Hermes application.

---

## Part 3 — Cookie Runner Studio configuration

### 3.1 Project identity

| Setting | Value |
|---|---|
| Studio | Cookie Runner Studio |
| Creative universe | CookieVerse Infinity |
| Agent display name | EverBloom Nexus |
| Existing technical profile | `everbloomnexus` |
| Primary environment | Native Termux |
| Additional environment | Ubuntu proot-distro |

Keep the agent's display name separate from the technical profile name. Do not rename the existing profile unless explicitly requested.

### 3.2 Inspect existing profiles first

```bash
hermes profile --help
hermes profile list
```

Use only the profile-management commands shown by the installed version's help output. If the version documents a profile inspection or selection command, use that documented syntax.

Do not assume a profile directory layout or manually move profile folders.

### 3.3 Profile identity instructions

Use the following as the proposed identity for the existing profile, adapting it to the configuration format supported by the installed Hermes version:

```text
Agent display name: EverBloom Nexus
Organization: Cookie Runner Studio
Universe: CookieVerse Infinity

Personality:
- Friendly, creative, and helpful.
- Technically knowledgeable and careful.
- Organized and transparent about limitations.
- Supportive of Cookie Run fan projects.
- Ask before destructive actions or major configuration changes.

Technical profile name:
everbloomnexus
```

If the profile uses a `SOUL.md` instruction file, review the existing file before editing it. Back it up first and preserve unrelated instructions.

### 3.4 Suggested project workspace

Create a separate project directory without moving Hermes data:

```bash
mkdir -p ~/CookieRunnerStudio/{docs,projects,skills,backups}
```

Suggested organization:

```text
~/CookieRunnerStudio/
├── docs/
│   └── installation.md
├── projects/
│   ├── CookieVerse-Infinity/
│   ├── Everlasting-Ancients/
│   ├── PureLily-Forever-Together/
│   └── Cookie-Runners-United/
├── skills/
└── backups/
```

Keep credentials and private agent data outside public Git repositories.

### 3.5 Memory configuration

Inspect the existing setup before changing providers:

- Hermes native memory
- Mem0
- Supermemory

For each integration, record one status:

- Configured and tested
- Configured but not tested
- Not configured
- Unavailable or failing

Do not assume these integrations are enabled merely because their packages or names appear in a configuration. Never print API keys, tokens, or private memory contents in diagnostic output.

### 3.6 Skills

Inspect the skills available to the installed Hermes version and the existing profile before adding new ones.

Suggested Cookie Runner Studio skill areas:

- Cookie Run project documentation
- Project planning and release notes
- Termux and Android development
- Git and GitHub workflows
- Dashboard development
- Telegram bot maintenance

Use the skill installation mechanism documented by the installed Hermes version. Review third-party skill code before enabling it.

### 3.7 Telegram

Configure Telegram through the supported Hermes setup workflow for the installed version.

Verify:

- The bot is associated with the intended profile.
- The gateway starts and stays connected.
- Logs do not expose secrets.
- Android battery and background restrictions are understood.

Never share bot tokens, `.env` files, or screenshots containing credentials.

### 3.8 Zsh and tmux

Check installed tools:

```bash
echo "$SHELL"
command -v zsh
command -v tmux
command -v git
```

Optional tools for the development environment:

- Zinit for Zsh plugin management
- tmux for persistent terminal sessions
- Agenmux, after confirming compatibility with the installed tmux version
- OpenCode for coding workflows
- Ubuntu proot-distro for Linux tools

Back up shell configuration before editing:

```bash
cp ~/.zshrc ~/.zshrc.backup 2>/dev/null || true
cp ~/.tmux.conf ~/.tmux.conf.backup 2>/dev/null || true
```

Preferred tmux prefix: `Ctrl+W`. Apply the Cookie Runner theme only after verifying the existing configuration.

---

## Part 4 — First-run audit

Run a read-only audit before making changes:

```bash
printf '%s\n' '=== Device ==='
uname -m
getprop ro.build.version.release
printf '%s\n' '=== Hermes executable ==='
command -v hermes
hermes --version
printf '%s\n' '=== Hermes help ==='
hermes --help
printf '%s\n' '=== Profile help ==='
hermes profile --help
printf '%s\n' '=== Profiles ==='
hermes profile list
printf '%s\n' '=== Diagnostics ==='
hermes doctor
```

Some commands or options may vary by release. If a command is unsupported, record the error and consult the installed version's help and the relevant repository documentation.

Before sharing output, remove private paths if desired and redact all tokens, keys, account identifiers, and personal data.

---

## Part 5 — Maintenance and recovery rules

Before every significant change:

1. Read the current installer README and release notes.
2. Check the installed Hermes version and executable path.
3. Create a private backup of `~/.hermes`.
4. Confirm that the proposed method supports native Termux.
5. Keep upstream source checkouts separate from the working installation.
6. Explain the proposed changes.
7. Obtain approval before deleting, overwriting, migrating, or resetting data.
8. Test the profile, memory, Telegram, and dashboard after the change.

Never blindly pipe an unfamiliar remote script into a shell. Never expose secrets in GitHub commits.

---

## Official and community references

- Upstream Hermes Agent: https://github.com/NousResearch/hermes-agent
- Upstream documentation: https://hermes-agent.nousresearch.com/docs
- Community Termux installer: https://github.com/adybag14-cyber/termux-hermes

---

**Cookie Runner Studio principle:** Preserve the existing Hermes installation first; inspect and customize it second.  
**Project mission:** Build a reliable, maintainable Hermes environment for EverBloom Nexus and CookieVerse Infinity.
