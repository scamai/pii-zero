<!-- English only -->

[Back to README](../README.md)

# Reproduce the README example

## Contents

- [What is shown](#what-is-shown)
- [Run it](#run-it)
- [Review the evidence](#review-the-evidence)
- [Scope and limitations](#scope-and-limitations)

## What is shown

The two README images are PNG renders of the input and saved output of
[`examples/native_pdf_demo.py`](../examples/native_pdf_demo.py). The PDF contains
only fictional contact details and a public purpose line. Neither image is a
mockup or a manually painted redaction. PyMuPDF renders each PDF after the real
text detection and redaction functions run.

The committed example used Python 3.11, spaCy 3.8.16 with `en_core_web_sm` 3.8.0,
Presidio Analyzer 2.2.364, and PyMuPDF 2.0. The optional InsuranceNER model was
absent, with its warning visible. All returned detections were from Presidio.

## Run it

Follow [source installation](../README.md#get-started), activate the virtual
environment, and install a spaCy English model if one is not already available:

```bash
python -m spacy download en_core_web_sm
python examples/native_pdf_demo.py --output-dir demo/native-pdf
```

The script refuses an unprovisioned spaCy model and enabled optional transformer
or GLiNER modes. It uses the repository's model selection order; an existing
configured or larger English model may be selected before the small one.
The output records which model was actually used. To repeat, choose a new output
directory; it refuses to overwrite existing files.

## Review the evidence

Open `before.pdf` and `after.pdf`. Inspect the solid-filled regions, then search
or copy text from the saved output. The script requires email and phone
detections, checks that their known text fragments are absent, checks that the
purpose line remains, and checks that the original PDF's hash is unchanged.
`evidence.json` records dependency versions, observed detector sources, entity
counts, checks, and file hashes. The two PNGs are generated from those PDFs.

To refresh the README assets after reviewing a new run, copy `before.png` to
`docs/assets/native-pdf-before.png` and `after.png` to
`docs/assets/native-pdf-after.png`. Update the version record above with the
actual evidence. The images inherit this repository's license; no third-party
artwork is embedded.

## Scope and limitations

The path is native PDF extraction → real text detection → PDF redaction → saved
output inspection. This deliberately bypasses OCR, visual detectors, CLI
routing, and audit writing. It does not measure detection completeness, model
accuracy, scan/photo coverage, restricted-network operation, or compliance.

The checks concern the known email and phone in this fixture. They are not a
general detector for sensitive information left in arbitrary documents.
Review every output and run the separate [full CLI sample](../README.md#try-a-fictional-document)
and [output checks](setup.md#review-the-output) for the workflow you intend to use.
