# Setting up PII Zero

Start with the [README installation steps](../README.md#get-started). Run commands
from the repository root so the default configuration and relative model paths
resolve consistently.

## Dependencies and models

Review the [third-party notices](../THIRD_PARTY_NOTICES.md) before provisioning
weights, especially Surya's version-specific model terms. Record the dependency
versions and model revisions you install; the project's AGPL license does not
license third-party weights.

| Component | Setup and behavior |
| --- | --- |
| Python dependencies | Install with `python -m pip install -e .`; ML frameworks are part of the base dependency set |
| spaCy English model | Install with `python -m spacy download en_core_web_lg`; smaller installed models or a blank pipeline can be used as fallbacks, with reduced detection coverage |
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
