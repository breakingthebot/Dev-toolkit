# Changelog

All notable changes to this project will be documented in this file.

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
