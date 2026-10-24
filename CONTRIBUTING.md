# Contributing to PII Zero

Help make document redaction easier to evaluate. Useful contributions include
clearer setup instructions, synthetic failure examples, tests for missed or
over-redacted regions, and focused improvements to the CLI or review UI.

## Start with a small contribution

1. Follow [setup](docs/setup.md) and try the fictional contact sheet before using
   your own documents.
2. Check [existing issues](https://github.com/scamai/pii-zero/issues). For a new
   detector, format, or workflow, describe the use case before a large change.
3. Fork the repository and work on a branch. Keep one behavior and its tests in
   each pull request.
4. Run the checks in [the development guide](docs/development.md#tests). State
   the exact command, platform, dependency versions, failures, and skips. Fast
   tests do not establish model quality or a complete installation.
5. Explain what changed and how you checked the saved output. For documentation,
   verify commands, relative links, and any generated example files.

## Report a reproducible problem

Include the commit, OS, Python version, command, model identifiers, expected
result, actual result, and relevant warnings. Prefer a tiny synthetic PDF or image
with known fields. A false negative and a false positive are both useful reports.

Keep personal documents, real customer data, vault keys, model caches, and raw
sensitive audit records out of issues and pull requests. Filenames and diagnostic
metadata can identify people even when detected text is omitted. Report security
vulnerabilities through the
[security policy](https://github.com/scamai/.github/blob/main/SECURITY.md).

## Changes and licensing

Use descriptive Conventional Commit messages, such as
`docs: clarify model setup` or `fix: preserve PDF page coordinates`. Document
changes to a command, supported format, model requirement, or retention behavior.
Keep benchmarks reproducible with the metadata listed in
[Development and benchmarks](docs/development.md#benchmarks).

Contributions to the project's original code and documentation are accepted under
[AGPL-3.0-only](LICENSE). Retain notices and identify the source and license of
third-party material. Submitting a contribution does not transfer its copyright
to Scam AI. See [third-party notices](THIRD_PARTY_NOTICES.md) for dependency and
model terms.
