#!/usr/bin/env python3
"""Run a small, local, searchable-PDF redaction demonstration.

This example deliberately exercises the native PDF text path.  It does not
download OCR or optional models, and it refuses to replace an existing output.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from pathlib import Path

import fitz
import spacy

from pii_redact.config import settings
from pii_redact.layers.text_layer import TextLayer
from pii_redact.models import DocumentType
from pii_redact.redact.engine import RedactionEngine
from pii_redact.ner.presidio_setup import _resolve_spacy_model


EMAIL = "alex@example.com"
PHONE = "+1 202-555-0100"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _render(pdf: Path, png: Path) -> None:
    with fitz.open(pdf) as document:
        if document.page_count != 1:
            raise RuntimeError("the demonstration PDF must contain exactly one page")
        pixmap = document[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        pixmap.save(png)


def _make_input(path: Path) -> None:
    with fitz.open() as document:
        page = document.new_page(width=360, height=220)
        page.insert_text((28, 42), "Fictional contact sheet", fontsize=18)
        page.insert_text((28, 82), "Name: Alex Example", fontsize=13)
        page.insert_text((28, 112), f"Email: {EMAIL}", fontsize=13)
        page.insert_text((28, 142), f"Phone: {PHONE}", fontsize=13)
        page.insert_text((28, 190), "Purpose: demonstrate local review before sharing.", fontsize=13)
        document.save(path)


def _text(path: Path) -> str:
    with fitz.open(path) as document:
        return "\n".join(page.get_text() for page in document)


def run(output_dir: Path) -> None:
    output_dir = output_dir.resolve()
    model_name = _resolve_spacy_model()
    if model_name == "blank:en":
        raise RuntimeError(
            "A trained spaCy model is required for this demo; install en_core_web_sm "
            "with `python -m spacy download en_core_web_sm` and retry."
        )
    truthy = {"1", "true", "yes"}
    if any(os.environ.get(name, "").lower() in truthy for name in ("PII_USE_TRANSFORMERS", "PII_USE_GLINER")):
        raise RuntimeError("optional transformer/GLiNER modes are not part of this demo")

    model_version = spacy.load(model_name).meta.get("version", "unknown")
    # Claim a fresh directory atomically, including when two demos start together.
    output_dir.mkdir(parents=True, exist_ok=False)
    paths = {name: output_dir / name for name in (
        "before.pdf", "after.pdf", "before.png", "after.png", "evidence.json"
    )}

    _make_input(paths["before.pdf"])
    before_hash = _sha256(paths["before.pdf"])
    _render(paths["before.pdf"], paths["before.png"])
    boxes = TextLayer().process(paths["before.pdf"], DocumentType.PDF_STRUCTURED)
    entity_types = {box.entity_type for box in boxes}
    required = {"EMAIL_ADDRESS", "PHONE_NUMBER"}
    if not required <= entity_types:
        raise RuntimeError(f"native detection missed required entities: {sorted(required - entity_types)}")

    RedactionEngine(settings).process_pdf(paths["before.pdf"], boxes, paths["after.pdf"])
    after_text = _text(paths["after.pdf"])
    residual_fragments = ("alex", "example.com", "202", "555", "0100")
    if any(fragment in after_text.lower() for fragment in residual_fragments):
        raise RuntimeError("redacted PDF still contains detected contact data")
    if "Purpose: demonstrate local review before sharing." not in after_text:
        raise RuntimeError("redaction removed the nonsensitive purpose line")
    if _sha256(paths["before.pdf"]) != before_hash:
        raise RuntimeError("input PDF changed during processing")
    _render(paths["after.pdf"], paths["after.png"])

    source_counts: dict[str, int] = {}
    for box in boxes:
        source_counts[box.source] = source_counts.get(box.source, 0) + 1
    evidence = {
        "format": "searchable PDF native text path",
        "python": platform.python_version(),
        "versions": {
            "pymupdf": fitz.VersionBind,
            "spacy": importlib.metadata.version("spacy"),
            "presidio_analyzer": importlib.metadata.version("presidio-analyzer"),
        },
        "spacy_model": Path(model_name).name if "/" in model_name else model_name,
        "spacy_model_version": model_version,
        "entities": sorted(entity_types),
        "source_counts": source_counts,
        "detected_count": len(boxes),
        "input_sha256": before_hash,
        "output_sha256": _sha256(paths["after.pdf"]),
        "before_png_sha256": _sha256(paths["before.png"]),
        "after_png_sha256": _sha256(paths["after.png"]),
        "checks": {
            "input_unchanged": True,
            "email_removed": True,
            "phone_removed": True,
            "purpose_retained": True,
        },
    }
    paths["evidence.json"].write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"Created native PDF demo in {output_dir}")
    print(f"Detected: {', '.join(sorted(required))}; wrote before/after PDFs and PNGs.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("demo/native-pdf"))
    args = parser.parse_args()
    try:
        run(args.output_dir)
    except (FileExistsError, OSError, RuntimeError) as error:
        print(f"native_pdf_demo.py: error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
