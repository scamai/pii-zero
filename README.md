# PII Zero

**Find and redact personal information in PDFs and document images.**

PII Zero, by [Scam AI](https://scam.ai), helps developers review receipts,
invoices, and forms before sharing them. Inspect detected regions, write a
separate redacted copy, and review the result with a local CLI or browser UI.
Text extraction, OCR, entity recognition, and visual detection run locally;
installation and initial model loading can require network access.

[Try a sample](#try-a-fictional-document) · [Setup](docs/setup.md) ·
[Limitations and data handling](docs/limitations.md) ·
[Development and benchmarks](docs/development.md) ·
[License: AGPL-3.0-only](LICENSE) ·
[Report an issue](https://github.com/scamai/pii-zero/issues)

> **Status: experimental.** Review redacted outputs before sharing them. Detection
> can miss sensitive information, and a successful command is not proof that a
> document is safe to release.

<details>
<summary>Contents</summary>

- [Choose a workflow](#choose-a-workflow)
- [Capabilities](#capabilities)
- [Get started](#get-started)
- [Try a fictional document](#try-a-fictional-document)
- [Usage](#usage)
- [Configuration and data handling](#configuration-and-data-handling)
- [Development](#development)
- [Support and contributions](#support-and-contributions)
- [Licensing](#licensing)

</details>

## Choose a workflow

| Your goal | Start here |
| --- | --- |
| Evaluate it without uploading a real document | [Generate and review a fictional contact sheet](#try-a-fictional-document) |
| Review detections before writing an output | `pii-redact inspect FILE --format table` |
| Produce a redacted copy or process a folder | `pii-redact redact FILE_OR_DIR --output OUTPUT` |
| Inspect documents in a browser | `pii-redact ui --port 7860` — local Gradio interface |
| Prepare an environment with network access restricted | [Provision models, then test under restrictions](docs/setup.md#restricted-network-operation) |

The supported evaluation path is a source installation. Container files are
[development scaffolding](docs/setup.md#containers), and recoverable vault
redaction is [not connected to the current pipeline](docs/limitations.md#vault-and-restore).

## Capabilities

| Area | Current implementation |
| --- | --- |
| Inputs | PDF, JPEG, PNG, TIFF, and BMP files; a directory of supported files for batch processing |
| Text detection | Native PDF text extraction or Surya OCR, followed by Presidio, spaCy, and custom recognizers |
| Visual detection | Face, QR/barcode, and heuristic region detection; coverage depends on the document route and available dependencies |
| Redaction | Solid-filled image regions and PyMuPDF redaction operations for PDFs |
| Review | Detection inspection through the CLI and a Gradio UI bound to localhost |
| Audit records | Per-document JSON with detection locations, types, sources, and processing time; detected text is omitted by default |

The repository focuses on document images and PDFs. It does not provide an audio
or video redaction workflow. Optional GLiNER and Qwen3-VL integrations are described
in the [setup guide](docs/setup.md#optional-models).

## Get started

Use a Python virtual environment. The package declares Python 3.10 or newer;
Python 3.11 is a starting point consistent with the included Dockerfile, not a
verified platform matrix. The commands below use a POSIX shell. Installation
includes substantial ML dependencies; read [prerequisites](docs/setup.md#prerequisites)
and [model setup](docs/setup.md#dependencies-and-models) first.

```bash
git clone https://github.com/scamai/pii-zero.git
cd pii-zero
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m spacy download en_core_web_lg
pii-redact --help
```

The help command confirms that the CLI is installed. It does **not** load every
detector. Complete [preflight checks](docs/setup.md#preflight-checks), then try
the sample below. First-use OCR and layout processing can fetch model weights.

The public project name is **PII Zero**. The Python package and command remain
`pii-redact`, and Python imports use `pii_redact`.

## Try a fictional document

**1. Create inputs with known fields.** The example generator uses PyMuPDF from
the installed dependencies. It creates a searchable PDF and a portrait PNG,
without downloading models or using personal documents.

```bash
python examples/make_sample.py --output-dir demo/input
mkdir -p demo/output
```

Both files contain a fictional name, `alex@example.com`, and a reserved example
phone number. The generator refuses to overwrite existing sample files.

**2. Inspect the PDF, then redact it.** Initial processing can load or download
models. Keep warnings visible.

```bash
pii-redact inspect demo/input/contact.pdf --format table
pii-redact redact demo/input/contact.pdf --output demo/output/contact_redacted.pdf
```

**3. Review the saved result.** Look for an `EMAIL_ADDRESS` detection at the
email's location, then open the output and check that the field is covered.
Search or copy text from the PDF as well as looking at the page. Check that an
audit JSON was written under `audit_logs/` and inspect its `source_counts` and
`entity_counts`. Missing output, missing expected fields, or detector warnings
mean this evaluation is incomplete; an empty detection list is not a pass.

Use the [output review steps](docs/setup.md#review-the-output) for a repeatable
check. Then repeat with `demo/input/contact.png` to exercise OCR separately:
success on a searchable PDF does not establish scan or photo coverage. Exact
detection counts can vary with your model and dependency versions.

## Usage

Run these commands from the repository root after setup.

```bash
# Inspect detections without writing a redacted copy.
pii-redact inspect ./sample.png --format table

# Write a separate redacted image or PDF.
pii-redact redact ./sample.png --output ./sample_redacted.png
pii-redact redact ./sample.pdf --output ./sample_redacted.pdf

# Process supported files directly inside a directory (not recursively).
pii-redact redact ./inbox --output ./redacted

# Open the local review UI at http://127.0.0.1:7860.
pii-redact ui --port 7860
```

Keep input and output paths separate. Inspection still writes an audit record.
Check the output file and
warnings as well as the detection summary. Some missing components or failures
can produce empty detections; structured PDFs with no detections may produce no
output copy.

## Configuration and data handling

[config/settings.yaml](config/settings.yaml) defines model paths, redaction,
audit, and pipeline settings. `--config` is available on `redact`, `inspect`, and
`ui`. See the [configuration caveat](docs/limitations.md#configuration) before
relying on per-command overrides.

- **Processing:** models run locally. Installation and first-use model loading
  can access the network; provision and test all required weights before
  restricting network access.
- **Audit records:** written to `./audit_logs` by default. `audit.include_text`
  defaults to `false`, but filenames and detection metadata can still be
  sensitive.
- **Review UI:** binds to `127.0.0.1` with Gradio sharing disabled. Uploaded files,
  previews, and temporary outputs still require local retention controls.
- **Recovery:** the CLI exposes vault/restore options, but they are not connected
  to a working redaction-and-recovery workflow. Keep originals separately; do
  not rely on those options to recover redacted content.

Local processing and audit records can support a privacy workflow. This project
does not establish regulatory compliance or certify that all PII has been removed.
Read the [current limitations](docs/limitations.md) before use with sensitive data.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -m fast
```

See [development and benchmarks](docs/development.md) for test isolation,
evaluation commands, and how to report reproducible results. Historical benchmark
numbers in Git history are not guarantees of redaction quality on new documents.

## Support and contributions

Use [GitHub Issues](https://github.com/scamai/pii-zero/issues) for reproducible bugs
and feature requests. Include your commit, Python version, command, and a synthetic
example. Keep personal information and real customer documents out of public
issues and pull requests.

You can help by trying setup on a new environment, improving an error message,
or sharing a minimal synthetic example of missed or excessive redaction.
[CONTRIBUTING.md](CONTRIBUTING.md) explains the first-contribution path and
what evidence to include. The [development guide](docs/development.md) covers
tests and reproducible benchmarks.

Report security vulnerabilities through the
[Scam AI security policy](https://github.com/scamai/.github/blob/main/SECURITY.md).
For other inquiries, contact [Scam AI](mailto:contact@scam.ai).

## Licensing

PII Zero's original code and documentation are licensed under the
[GNU Affero General Public License v3.0 only](LICENSE) (`AGPL-3.0-only`).
Copyright © 2026 Reality Inc. (Scam AI) and contributors. The software is provided
without warranty; see [NOTICE](NOTICE) and the license for details.

Commercial use is permitted under the license. Redistribution carries source
and notice obligations; modified versions offered over a network must offer
their Corresponding Source to the users interacting with them. See the
[licensing guide](docs/licensing.md) for distribution and deployment guidance.

Dependencies, model weights, and datasets retain their own licenses. In
particular, some OCR weights have additional commercial-use conditions. Review
the [third-party notices](THIRD_PARTY_NOTICES.md) for the versions and models you
use; this project's AGPL license does not replace those terms.
