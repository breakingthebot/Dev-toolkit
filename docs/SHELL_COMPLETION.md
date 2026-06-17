<!--
docs/SHELL_COMPLETION.md
Documents shell completion setup for Dev Toolkit.
Connects to: README.md, src/dev_toolkit/cli.py
Created: 2026-06-17
-->

# Shell Completion

Dev Toolkit uses Click's built-in shell completion support. Install the package in the active environment before generating completion scripts:

```powershell
pip install -e ".[dev]"
```

## PowerShell

Generate the completion script:

```powershell
_DEV_TOOLKIT_COMPLETE=powershell_source dev-toolkit > dev-toolkit-complete.ps1
```

Load it for the current terminal session:

```powershell
. .\dev-toolkit-complete.ps1
```

To load completion automatically, add that dot-source command to your PowerShell profile.

## Bash

Generate the completion script:

```bash
_DEV_TOOLKIT_COMPLETE=bash_source dev-toolkit > ~/.dev-toolkit-complete.bash
```

Load it for the current terminal session:

```bash
source ~/.dev-toolkit-complete.bash
```

To load completion automatically, add the `source` command to `~/.bashrc`.

## Zsh

Generate the completion script:

```zsh
_DEV_TOOLKIT_COMPLETE=zsh_source dev-toolkit > ~/.dev-toolkit-complete.zsh
```

Load it for the current terminal session:

```zsh
source ~/.dev-toolkit-complete.zsh
```

To load completion automatically, add the `source` command to `~/.zshrc`.

## Verify Completion

After loading the script, type a partial command and press Tab:

```powershell
dev-toolkit j<Tab>
dev-toolkit hash <Tab>
```
