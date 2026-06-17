# Changelog

All notable changes to this project will be documented in this file.

## [0.8.0] - 2026-06-17

### Added

- Add `dev-toolkit file size` for file byte counts.
- Add `dev-toolkit file size --human` for readable size units.
- Add `dev-toolkit file lines` for UTF-8 text line counts.
- Add `dev-toolkit file stats` for byte, line, word, and character counts.
- Add file service and CLI tests.

## [0.7.0] - 2026-06-17

### Added

- Add `DEV_TOOLKIT_PASSWORD_LENGTH` for default password command length.
- Add `DEV_TOOLKIT_JSON_INDENT` for default JSON formatting indentation.
- Add validated environment default helpers and tests.
- Document optional environment defaults in README and `.env.example`.

## [0.6.0] - 2026-06-17

### Added

- Add shell completion setup documentation for PowerShell, Bash, and Zsh.
- Add examples to top-level CLI help and major command group help output.
- Add CLI help tests for documented examples.

## [0.5.0] - 2026-06-17

### Added

- Add `dev-toolkit timestamp --to-unix` for ISO 8601 datetime to Unix timestamp conversion.
- Add `dev-toolkit timestamp --to-unix --milliseconds` for Unix millisecond output.
- Add timestamp service and CLI tests for reverse conversion, timezone offsets, and `Z` suffix input.

## [0.4.0] - 2026-06-12

### Added

- Add `dev-toolkit json format` for pretty-printing JSON.
- Add `dev-toolkit json minify` for compact JSON output.
- Add `dev-toolkit json validate` for JSON syntax validation.
- Add file input and output support for JSON formatting and minification.
- Add JSON service and CLI tests.

## [0.3.0] - 2026-06-12

### Added

- Add `dev-toolkit hash text` for SHA-256 and SHA-512 text hashing.
- Add `dev-toolkit hash file` for SHA-256 and SHA-512 file hashing.
- Add `dev-toolkit hash verify` for checksum verification.
- Add hash service and CLI tests.

## [0.2.0] - 2026-06-12

### Added

- Add file input and output options for `dev-toolkit base64 encode`.
- Add file input and output options for `dev-toolkit base64 decode`.
- Add byte-oriented base64 service helpers for file-safe encoding and decoding.
- Add CLI tests for file-based base64 workflows and missing input validation.

## [0.1.0] - 2026-06-12

### Added

- Add packaged Click CLI with `dev-toolkit` entry point.
- Add UUID generation command.
- Add secure password generation command with configurable length and optional symbols.
- Add base64 encode and decode commands.
- Add Unix timestamp conversion command.
- Add pytest coverage for services and CLI wiring.
- Add README, MIT license, environment template, and project metadata.
