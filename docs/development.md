# Developing and evaluating PII Zero

The product name is **PII Zero**, maintained by **Scam AI**. Use `pii-zero` for the
GitHub repository, `pii-redact` for the existing Python distribution and command,
and `pii_redact` for imports. Domain names such as `scam.ai` retain their spelling.

## Repository layout

| Path | Purpose |
| --- | --- |
| `pii_redact/cli.py`, `pii_redact/ui.py` | Command-line and local review interfaces |
| `pii_redact/pipeline.py`, `pii_redact/classifier.py` | Document routing and processing |
| `pii_redact/layers/`, `pii_redact/ner/` | Extraction, OCR, visual detection, and entity recognition |
| `pii_redact/redact/` | Redaction primitives and supporting audit/vault components |
| `config/settings.yaml` | Default configuration |
| `scripts/` | Model setup helpers, training, and evaluation runners |
| `tests/` | Unit tests and document smoke tests |

Some supporting modules are not wired into the current pipeline. Follow the
call path from the CLI before documenting a component as a supported feature.

## Tests

After [setup](setup.md), install the development extra and run the fast suite:

```bash
python -m pip install -e ".[dev]"
python -m pytest -m fast
```

The suite uses mocked model paths for many fast tests. Collection may still inspect
optional libraries, so read the complete result, including skipped tests. Fast
tests do not establish model quality or a working end-to-end installation.

Run model-dependent checks separately in a provisioned environment:

```bash
python -m pytest tests/test_regex_patterns.py
python -m pytest tests/test_smoke_claim_form.py -v
```

The existing `pytest.ini` excludes regex tests from default collection to avoid a
documented native-library interaction. `tests/conftest.py` disables CUDA and runs
subprocess-marked cases in an isolated interpreter. Preserve those controls; do
not treat an unrun or dependency-skipped test as a pass.

## Benchmarks

The runners measure different parts of the system. Dataset downloads and model
initialization may need network access. Check each runner's `--help` and provision
its dependencies and datasets before execution.

```bash
# Text entity recognition, exact matching (the default for this runner).
python scripts/run_benchmark_nlp.py --dataset gretel --max-docs 100 --output ./gretel-exact.json

# The same sample with partial matching, reported separately.
python scripts/run_benchmark_nlp.py --dataset gretel --max-docs 100 --partial --output ./gretel-partial.json

# Receipt OCR + entity recognition; explicitly select exact matching.
python scripts/run_benchmark_sroie.py --dataset cord --max-docs 20 --exact --output ./cord-exact.json
```

Report the commit, dependency versions, model identifiers, hardware, dataset
version/split, sample count, matching policy, failures, and per-entity results with
every result. The receipt runner defaults to partial matching; the text runner
does not. Their scores are not directly interchangeable.

Partial overlap can count as a match while leaving some identifying text
uncovered. Evaluate residual content in actual redacted files in addition to
precision, recall, and F1. Historical README results remain available in Git
history; they are not current benchmark evidence.

## Contributing

Keep changes focused and explain the behavior they change. Include a synthetic
reproduction and relevant verification results. Do not commit personal documents,
model caches, vault keys, or sensitive audit files. Use the
[security reporting policy](https://github.com/scamai/.github/blob/main/SECURITY.md)
for vulnerabilities instead of a public issue.
