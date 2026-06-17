# Dev Toolkit

A Click-based Python CLI for common developer utilities.

## Stack

- Python 3.12
- Click
- pytest
- No database

## Setup

```powershell
py -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Environment Variables

No environment variables are required.

See `.env.example` for the empty template used by this project.

## Running Locally

```powershell
dev-toolkit --version
dev-toolkit uuid
dev-toolkit password --length 24
dev-toolkit base64 encode "hello"
dev-toolkit base64 decode "aGVsbG8="
dev-toolkit base64 encode --input-file plain.txt --output-file encoded.txt
dev-toolkit base64 decode --input-file encoded.txt --output-file plain.txt
dev-toolkit hash text sha256 "hello"
dev-toolkit hash file sha512 plain.txt
dev-toolkit hash verify sha256 "<expected-digest>" plain.txt
dev-toolkit json format '{\"b\":2,\"a\":1}'
dev-toolkit json minify '{ \"b\": 2, \"a\": 1 }'
dev-toolkit json validate --input-file data.json
dev-toolkit timestamp 1718064000
dev-toolkit timestamp --to-unix "2024-06-11T00:00:00+00:00"
dev-toolkit timestamp --to-unix --milliseconds "2001-09-09T01:46:40Z"
```

## Shell Completion

Shell completion is available through Click for PowerShell, Bash, and Zsh.

See [docs/SHELL_COMPLETION.md](docs/SHELL_COMPLETION.md) for setup commands.

## Help Examples

Every major command group includes examples in its help output:

```powershell
dev-toolkit --help
dev-toolkit base64 --help
dev-toolkit hash --help
dev-toolkit json --help
dev-toolkit timestamp --help
```

## Testing

```powershell
venv\Scripts\python.exe -m pytest
```

## Deployed

Not deployed. This is a local command-line tool.

## Architecture Notes

This is a small terminal toolkit that groups common developer utilities behind predictable commands while keeping each utility isolated in its own module so it is easy to test and extend. The Click layer in `src/dev_toolkit/cli.py` handles command parsing, file option handling, shell-completion-compatible command metadata, practical help examples, and user-facing errors. The actual work lives in service modules under `src/dev_toolkit/services/`, which keeps encoding, hashing, JSON parsing, password generation, bidirectional timestamp conversion, and UUID generation independently testable.

## Notes

- The CLI entry point is `dev-toolkit`.
- Password generation uses Python's `secrets` module.
- Base64 commands accept direct text or file input with optional file output.
- Hash commands support SHA-256 and SHA-512 for direct text, files, and checksum verification.
- JSON commands support formatting, minification, validation, file input, and file output.
- Timestamp conversion accepts Unix timestamps in seconds or milliseconds, returns UTC ISO 8601 output, and can convert ISO 8601 datetimes back to Unix seconds or milliseconds.
- Shell completion setup is documented for PowerShell, Bash, and Zsh.
