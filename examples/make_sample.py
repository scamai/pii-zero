"""Create a fictional contact sheet as a searchable PDF and a document image.

Run from the repository root after installing PII Zero:
    python examples/make_sample.py --output-dir demo/input
No models or network access are needed to generate these inputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("demo/input"))
    args = parser.parse_args()
    pdf_path = args.output_dir / "contact.pdf"
    image_path = args.output_dir / "contact.png"
    if pdf_path.exists() or image_path.exists():
        parser.error("sample files already exist; choose a new --output-dir")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        "SYNTHETIC CONTACT SHEET - NOT A REAL RECORD",
        "Name: Alex Example",
        "Email: alex@example.com",
        "Phone: +1 202-555-0100",
        "Purpose: test detection and review the saved redacted output.",
        "All contact details on this page are fictional demonstration data.",
    ]
    with fitz.open() as document:
        page = document.new_page(width=612, height=792)
        for index, line in enumerate(lines):
            page.insert_text((40, 70 + index * 32), line, fontsize=12)
        document.save(pdf_path)
        page.get_pixmap(dpi=150).save(image_path)
    print(f"Created {pdf_path} and {image_path}")
    print("Inspect for EMAIL_ADDRESS around alex@example.com; review every output.")


if __name__ == "__main__":
    main()
