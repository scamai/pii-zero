# PII Zero: limitations and data handling

PII Zero is an experimental document-redaction codebase. Its components and
evaluation scripts are useful for development, but detection quality must be
measured on the documents and entity types relevant to a specific workflow.

## Detection and output review

- OCR, named-entity recognition, and visual heuristics can miss PII or redact
  unrelated content. English-oriented recognizers and financial examples do not
  establish coverage for every language or document type.
- Document classification selects different processing paths. For example, the
  photo path runs visual detection without the text OCR path.
- Some component failures are logged and converted into empty detections. Review
  warnings, verify that expected detectors ran, and inspect the output file.
- The structured-PDF path may not create an output when it finds no boxes.
- The implementation accepts TIFF files but does not establish complete coverage
  of every frame in a multipage TIFF.
- PDF OCR/visual boxes and native-text boxes originate in different coordinate
  spaces. Validate alignment and text removal on representative PDFs before
  relying on their redaction output.
- The configured generic YOLOv8 weights are not evidence of a validated
  license-plate detector. Heuristic handwriting detection is also not a guarantee
  that all handwritten PII is covered.
- Metadata removal is route-dependent. Do not assume every output format has all
  metadata, attachments, or hidden content removed.

Keep originals and redacted outputs in separate locations. Review detections and
saved artifacts before releasing a document. A passing unit test or an aggregate
F1 score does not prove that a particular document contains no residual PII.

## Audit records, inspection, and temporary files

Each processed document writes a JSON audit record to `audit.log_dir`, including
inspection and single-file dry runs. Records include the input filename, document
type, page information, detection boxes, entity/source counts, and processing time.

`audit.include_text: false` omits detected text from those JSON detection records.
JSON inspection also omits detected text by default. Filenames, console/debug
logs, inspection metadata, and UI temporary files can still be sensitive. Apply
access controls and retention rules to these files.

The audit files are ordinary local JSON files. They are not a tamper-evident or
immutable audit store, and an audit-write failure does not necessarily stop
document processing.

## Vault and restore

Vault modules and CLI/UI options exist, but the current pipeline does not store
original regions in a vault during redaction. The CLI also imports a vault class
from a module that does not expose that class. Consequently, `--vault` and
`restore` are not a supported end-to-end recovery workflow.

Do not use these options as a backup strategy. Retain source documents separately
according to your own access and retention requirements.

## Configuration

`--config` loads a configuration file for the pipeline, but some processing layers
still read a module-level default settings object. Per-command overrides therefore
do not consistently control every model or redaction setting. Verify the behavior
of a setting in the processing path you use before relying on it.

Directory processing is non-recursive. The batch path currently does not propagate
`redact --dry-run`, so use `inspect FILE` for inspection rather than assuming a
directory dry run will avoid output files.

## Privacy and licensing

Local execution describes where models process documents. It does not establish
zero network egress, a complete data-retention policy, or regulatory compliance.
See [restricted-network setup](setup.md#restricted-network-operation).

The repository currently has no project `LICENSE` file. Model weights, datasets,
and dependencies have separate terms; this documentation does not assign a new
license to the project or those components.
