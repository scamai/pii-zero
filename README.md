# PII Zero

**Local PII redaction for PDFs and document images, by [Scam AI](https://scam.ai).**

PII Zero helps developers inspect and redact personally identifiable information
in documents such as receipts, invoices, and insurance forms. It combines text
extraction, OCR, entity recognition, and visual detection with a command-line
interface and a local review UI.

[Setup](docs/setup.md) · [Limitations and data handling](docs/limitations.md) ·
[Development and benchmarks](docs/development.md) ·
[Report an issue](https://github.com/scamai/pii-zero/issues)

> **Status: experimental.** Review redacted outputs before sharing them. Detection
> can miss sensitive information, and a successful command is not proof that a
> document is safe to release.

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

Use a Python virtual environment. The package declares Python 3.10 or newer; the
included Dockerfile uses Python 3.11. Installation includes substantial ML
dependencies, and model provisioning requires network access.

```bash
git clone https://github.com/scamai/pii-zero.git
cd pii-zero
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m spacy download en_core_web_lg
pii-redact --help
```

Complete [model setup](docs/setup.md) before processing documents. OCR and other
components may download weights on first use. Start with synthetic documents to
confirm that the required detection paths are available in your environment.

The public project name is **PII Zero**. The Python package and command remain
`pii-redact`, and Python imports use `pii_redact`.

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

Report security vulnerabilities through the
[Scam AI security policy](https://github.com/scamai/.github/blob/main/SECURITY.md).
For other inquiries, contact [Scam AI](mailto:contact@scam.ai).

## Licensing

This repository does not currently include a project `LICENSE` file. Its public
visibility should not be presented as a published open-source license. Third-party
libraries, datasets, and model weights have their own licensing terms.
