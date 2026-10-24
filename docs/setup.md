[English](setup.md)

← Back to [README](../README.md)

# Setting up PII Zero

Start with the [README installation steps](../README.md#get-started). Run commands
from the repository root so the default configuration and relative model paths
resolve consistently.

## Contents

- [Prerequisites](#prerequisites)
- [Dependencies and models](#dependencies-and-models)
- [Preflight checks](#preflight-checks)
- [Try the sample](#try-the-sample)
- [Review the output](#review-the-output)
- [Optional models](#optional-models)
- [Restricted-network operation](#restricted-network-operation)
- [Troubleshooting](#troubleshooting)
- [Containers](#containers)

## Prerequisites

| Requirement | What to prepare |
| --- | --- |
| Python | The package declares 3.10+. The README uses Python 3.11, as does the Dockerfile. Use a virtual environment; a complete OS/hardware support matrix has not been established. |
| Shell | README commands use a POSIX shell. On Windows, adapt virtual-environment activation to your shell; the container files do not establish a tested Windows installation. |
| Dependencies | The base install includes PyTorch, OCR, NLP, and image-processing libraries. There is no lightweight CLI-only extra. |
| Models and storage | Allow storage for both dependencies and the models used by your document path. Downloads may use library caches outside `./models`; no measured minimum disk or RAM requirement is published. |
| Network | Provision dependencies and model weights before attempting restricted-network execution. A source checkout alone contains neither. |
| QR/barcodes | Install the system ZBar library as well as `pyzbar`; follow [pyzbar's platform instructions](https://github.com/NaturalHistoryMuseum/pyzbar#installation). |
| GPU | The optional VLM has its own compatibility requirements. No hardware configuration or throughput is guaranteed by this preview; leave optional models off for the first evaluation. |

## Dependencies and models

Review the [third-party notices](../THIRD_PARTY_NOTICES.md) before provisioning
weights, especially Surya's version-specific model terms. Record the dependency
versions and model revisions you install; the project's AGPL license does not
license third-party weights.

| Component | Setup and behavior |
| --- | --- |
| Python dependencies | Install with `python -m pip install -e .`; ML frameworks are part of the base dependency set |
| spaCy English model | The README's native-PDF example uses `python -m spacy download en_core_web_sm`. You can install `en_core_web_lg` for the larger English model. Model choice changes detection coverage; an absent model is not a working fallback. |
| Surya OCR | Used by the current image OCR pipeline; predictor initialization can fetch weights on first use |
| Docling | Used for layout-aware PDF text extraction, with a PyMuPDF fallback; provision any models needed by your document path |
| QR/barcodes | The `pyzbar` package also needs the system ZBar shared library |
| Visual detectors | Availability depends on installed packages and model files; missing components can be skipped |

The legacy `scripts/download_models.py` helper attempts several downloads, but it
still targets PaddleOCR and does not provision the active Surya path or Qwen3-VL.
`pii-redact doctor` also checks older dependencies. Neither is a complete readiness
check for the current pipeline.

Use synthetic examples that exercise your intended input types to initialize and
verify each path. Confirm warnings, detected regions, and saved outputs before
using sensitive documents. A dependency import or a zero-detection result alone
does not demonstrate a working detector.

## Preflight checks

After the README install steps, keep the virtual environment active and run:

```bash
pii-redact --help
python -m pip check
python -m spacy validate
python -c "import spacy; spacy.load('en_core_web_sm'); print('English model loads')"
```

Substitute `en_core_web_lg` if that is the model you installed.
These check command discovery, declared dependency consistency, and the English
NLP model. They do not validate OCR, visual detectors, PDF coordinates, or output
redaction. Resolve errors before continuing. The legacy `pii-redact doctor` is
supplementary; neither its success nor `download-models` completes this checklist.

## Try the sample

For the smallest evaluation, first run the
[native-PDF example](../README.md#try-a-fictional-document). It checks saved text
and produces the README's before/after images without exercising OCR or visual
detectors. Then evaluate the full CLI route below.

Generate the fictional contact sheet from the repository root:

```bash
python examples/make_sample.py --output-dir demo/input
mkdir -p demo/output
pii-redact inspect demo/input/contact.pdf --format table
pii-redact redact demo/input/contact.pdf --output demo/output/contact_redacted.pdf
```

The PDF contains native text; its rendered PNG exercises a different route. Once
you have reviewed the PDF result, run:

```bash
pii-redact inspect demo/input/contact.png --format table
pii-redact redact demo/input/contact.png --output demo/output/contact_redacted.png
```

This can initialize Surya and other detectors on first use. Keep all warnings;
if a required detector fails, stop treating that run as evidence of coverage.
The synthetic email is `alex@example.com`, the name is `Alex Example`, and the
phone is `+1 202-555-0100`. Look for detections at the corresponding regions;
name and phone recognition can differ between models. A missed expected field
is a useful reproduction, not a reason to lower your acceptance criteria.

## Review the output

1. Check that the output exists and opens, with the same expected pages and
   readable non-sensitive content. A structured PDF with no detections may have
   no output copy at all.
2. Compare input and output visually. Confirm that the complete email is covered,
   with no shifted boxes or readable characters at the edges. Review the name
   and phone too.
3. For the PDF, also search/copy the text. This small residual-text check catches
   the sample email surviving in an extractable text layer:

   ```bash
   python - <<'PY'
   from pathlib import Path
   import fitz
   path = Path('demo/output/contact_redacted.pdf')
   if not path.is_file():
       raise SystemExit('Missing redacted PDF')
   with fitz.open(path) as document:
       text = '\n'.join(page.get_text() for page in document)
   if 'alex@example.com' in text.lower():
       raise SystemExit('Sample email remains in the PDF text layer')
   print('Sample email absent from extracted text; visual and other checks still required')
   PY
   ```

4. Check the matching audit JSON in `audit_logs/`. Confirm the input filename,
   page count, detection types, and `source_counts`; inspection also writes a
   record. Audit files do not certify completeness and a failed audit write may
   not fail the processing command.

The text check covers one known string in one layer. It does not validate image
OCR, metadata, attachments, every page, or every sensitive field. Follow
[detection and output review limitations](limitations.md#detection-and-output-review)
when evaluating your intended document type.

## Optional models

### GLiNER

GLiNER is already declared in the base dependencies, but its recognizer is opt-in:

```bash
PII_USE_GLINER=1 pii-redact inspect ./sample.png --format table
```

The recognizer can load additional weights. Test its effect on your evaluation
documents before enabling it in a workflow.

### Qwen3-VL

The local UI exposes an experimental vision-language model option:

```bash
pii-redact ui --vlm
```

The model identifier is configured under `models.vlm_model_id` in
[settings.yaml](../config/settings.yaml). The default is
`Qwen/Qwen3-VL-8B-Instruct-FP8`. Provision compatible weights and dependencies for
your hardware before enabling it. This repository does not establish a minimum
GPU specification or a guaranteed processing rate. The `redact` CLI command does
not accept `--vlm`.

## Restricted-network operation

Model execution is local, but dependency installation, initial model loading, and
library telemetry are separate network considerations. To prepare an isolated
environment:

1. Install dependencies and provision the models for every enabled path.
2. Exercise those paths with synthetic inputs and inspect warnings and outputs.
3. Preserve the required model files and caches in the runtime environment.
4. Apply network restrictions and repeat the same checks with network access
   denied. Account for local UI access if you use the browser interface.

Hugging Face offline environment variables only affect cooperating libraries;
they do not replace network isolation. A missing detector must not be interpreted
as a document containing no PII.

## Troubleshooting

| Symptom | Check next |
| --- | --- |
| `pii-redact: command not found` | Activate the environment where you ran `python -m pip install -e .`; check `python -m pip show pii-redact`. |
| The English model cannot load | Run `python -m spacy download en_core_web_lg` in that same environment, then repeat preflight. A blank NLP fallback has different coverage. |
| A model download fails on first use | Check connectivity, permissions, disk space, and the model's terms. Provision caches for the same user/environment that runs the CLI. |
| ZBar cannot be found | Install its native shared library for your platform; installing the Python wrapper alone is insufficient. |
| No detections or no output | Read detector warnings, check the classified document type, and repeat with the known sample. Do not interpret an empty list as proof that the document has no PII. |
| PDF boxes are shifted | Stop sharing that output and retain a synthetic reproduction; coordinate conversion is a documented limitation. |
| A custom config seems ignored | Some layers use module-level defaults. See [configuration limitations](limitations.md#configuration) before relying on overrides. |

If the problem remains, follow [the reporting guide](../CONTRIBUTING.md#report-a-reproducible-problem).

## Containers

The included [Dockerfile](../Dockerfile) and
[Compose configuration](../docker-compose.yml) are development scaffolding. They
have not been validated as a complete installation path for the current pipeline:

- The image's download step uses the legacy helper and tolerates download failures.
- The worker disables networking, which makes missing model caches a runtime issue.
- The UI service command and container binding need integration work before its
  published port can be used as a supported startup path.

Use the source installation above for evaluation. Container deployment and model
packaging need separate validation before use with sensitive documents.
