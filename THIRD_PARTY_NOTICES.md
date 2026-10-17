# Third-party notices

PII Zero is maintained by Scam AI. Its original code and documentation are
licensed under `AGPL-3.0-only`; see [LICENSE](LICENSE) and [NOTICE](NOTICE).
Third-party components retain their own copyrights, licenses, and notices.
This file does not relicense them or grant rights to their training data.

This index was checked on **2026-10-17** against upstream license files and
publisher metadata. It covers declared direct dependencies and notable model
paths. Dependency ranges and most model revisions are not locked in this
repository, so this is not an inventory of a particular installed environment
or a complete list of transitive dependencies. Preserve the actual licenses
and notices accompanying the versions and artifacts you distribute; the links
below do not replace those notices or any required source distribution.

## Dependencies that affect licensing choices

| Component | Upstream terms and scope |
| --- | --- |
| PyMuPDF / MuPDF | [Upstream offers AGPL and commercial licensing](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright). The public dependency is not made permissively licensed by PII Zero's license. A separate commercial agreement must cover the intended use if relying on that alternative. |
| Ultralytics / YOLO | [Ultralytics offers AGPL-3.0 and Enterprise licensing](https://www.ultralytics.com/license). Review the code and weights you actually use, including `yolov8n.pt` downloaded by the legacy helper. No Enterprise license is supplied by this repository. |
| Surya OCR | The declared range is `surya-ocr>=0.17`, which spans license changes. The code at [v0.17.1](https://github.com/datalab-to/surya/blob/v0.17.1/LICENSE) uses GPL v3; at [v0.22.1](https://github.com/datalab-to/surya/blob/v0.22.1/LICENSE) it uses Apache-2.0. Model weights have separate terms in both versions; see below. These examples do not establish compatibility with every release in the range. |

GPL-v3-covered Surya code retains its GPL terms when combined under the
permissions in AGPL section 13. A project's AGPL declaration does not change
the licenses of upstream files.

### Surya model weights

Surya's modified AI Pubs OpenRAIL-M model license is separate from its code
license. It includes use restrictions and conditions on commercial use:

- [v0.17.1 model terms](https://github.com/datalab-to/surya/blob/v0.17.1/MODEL_LICENSE)
  restrict use where the relevant entity's prior-year gross revenue or total
  equity/debt funding exceeds **US$2 million**, with stated personal-use and
  research exceptions.
- [v0.22.1 model terms](https://github.com/datalab-to/surya/blob/v0.22.1/MODEL_LICENSE)
  use **US$5 million** thresholds, with their own full conditions.

These amounts are not the complete terms or a general commercial clearance.
Record the exact model artifact and applicable license before use. A newer
package's code license does not retroactively change previously downloaded
weights, and using PII Zero under AGPL does not remove these model restrictions.

## Other declared Python dependencies

These are upstream project-level licenses observed at the time of this review.
A package or wheel may also contain separately licensed components. Consult the
selected release's complete notices, especially for binary packages.

| Package | Upstream license / primary source |
| --- | --- |
| `presidio-analyzer`, `presidio-anonymizer` | [MIT](https://github.com/microsoft/presidio/blob/main/LICENSE) |
| `spacy` | [MIT](https://github.com/explosion/spaCy/blob/master/LICENSE) |
| `scispacy` | [Apache-2.0](https://github.com/allenai/scispacy/blob/main/LICENSE) |
| `gliner` | [Apache-2.0](https://github.com/urchade/GLiNER/blob/main/LICENSE) |
| `transformers` | [Apache-2.0](https://github.com/huggingface/transformers/blob/main/LICENSE) |
| `torch` | [BSD-3-Clause, with additional third-party notices](https://github.com/pytorch/pytorch/blob/main/LICENSE) |
| `torchvision` | [BSD-3-Clause](https://github.com/pytorch/vision/blob/main/LICENSE) |
| `segment-anything` | [Apache-2.0](https://github.com/facebookresearch/segment-anything/blob/main/LICENSE) |
| `pyzbar` | [MIT, per publisher metadata](https://pypi.org/project/pyzbar/); the ZBar native library is separate |
| `zxing-cpp` | [Apache-2.0](https://github.com/zxing-cpp/zxing-cpp/blob/master/LICENSE) |
| `piexif` | [MIT, per publisher metadata](https://pypi.org/project/piexif/) |
| `opencv-python-headless` | [OpenCV Apache-2.0](https://github.com/opencv/opencv/blob/4.x/LICENSE) and [MIT packaging code](https://github.com/opencv/opencv-python/blob/4.x/LICENSE.txt), plus bundled third-party notices |
| `Pillow` | [MIT-CMU (PIL/Pillow license)](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| `cryptography` | [Apache-2.0 OR BSD-3-Clause](https://github.com/pyca/cryptography/blob/main/LICENSE), plus bundled third-party notices |
| `pyyaml` | [MIT, per publisher metadata](https://pypi.org/project/PyYAML/) |
| `click` | [BSD-3-Clause](https://github.com/pallets/click/blob/main/LICENSE.txt) |
| `gradio` | [Apache-2.0](https://github.com/gradio-app/gradio/blob/main/LICENSE) |
| `imagehash` | [BSD-2-Clause](https://github.com/JohannesBuchner/imagehash/blob/master/LICENSE) |
| `docling` | [MIT](https://github.com/docling-project/docling/blob/main/LICENSE); downloaded model artifacts have their own licenses |

Development/build dependencies are also separately licensed:

| Package | Upstream license / primary source |
| --- | --- |
| `hatchling` | [MIT](https://github.com/pypa/hatch/blob/master/LICENSE.txt) |
| `pytest` | [MIT](https://github.com/pytest-dev/pytest/blob/main/LICENSE) |
| `pytest-cov` | [MIT, per publisher metadata](https://pypi.org/project/pytest-cov/) |
| `ruff` | [MIT, with additional third-party notices](https://github.com/astral-sh/ruff/blob/main/LICENSE) |
| `datasets` | [Apache-2.0, per publisher metadata](https://pypi.org/project/datasets/); datasets loaded by the library retain their own terms |

ZBar, used through `pyzbar`, has its own
[LGPL-2.1 license](https://github.com/mchehab/zbar/blob/master/LICENSE.md).
System packages and libraries bundled in containers or binary wheels need
their own license review and notices.

## Models and optional integrations

Model cards and the downloaded artifact's license apply to that model, not to
every model supported by the same Python library. Replacing a model identifier
can change the applicable terms. No third-party model weights are included in
this source tree.

| Model or path | Source and licensing information |
| --- | --- |
| Surya OCR checkpoints | Selected by the installed Surya version; see the separate model terms above. Initialization can download weights. |
| `Qwen/Qwen3-VL-8B-Instruct-FP8` and fallback `Qwen/Qwen3-VL-8B-Instruct` | Publisher cards declare Apache-2.0: [FP8](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct-FP8), [base](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct). The default configuration selects FP8; record the revision actually loaded. |
| `urchade/gliner_medium-v2.1` | Optional GLiNER recognizer default; [publisher model card](https://huggingface.co/urchade/gliner_medium-v2.1) declares Apache-2.0. Other GLiNER models can have different licenses. |
| `obi/deid_roberta_i2b2` | Default for the opt-in `PII_USE_TRANSFORMERS=1` backend; [publisher card](https://huggingface.co/obi/deid_roberta_i2b2) declares MIT. The i2b2 training dataset has separate access/use conditions; the model card does not license that dataset. |
| `en_core_web_lg` | spaCy model package. [Release 3.8.0 metadata](https://github.com/explosion/spacy-models/blob/master/meta/en_core_web_lg-3.8.0.json) declares MIT and lists its data sources separately. Preserve the metadata and notices for the release you install, including any smaller fallback model. |
| `en_core_sci_lg` | Separate scispaCy model package. The legacy helper points to release 0.5.3; inspect that artifact's model license and data-source notices before redistribution. The [scispaCy project](https://github.com/allenai/scispacy) code license alone does not establish the model's terms. |
| `microsoft/trocr-base-handwritten` | Referenced by configuration and the legacy downloader; [publisher card](https://huggingface.co/microsoft/trocr-base-handwritten) declares MIT. Its training datasets retain their own terms. |
| SAM checkpoints | Referenced by configuration and manual download instructions. The [upstream project](https://github.com/facebookresearch/segment-anything#license) licenses its code and model checkpoints under Apache-2.0. Match the actual downloaded checkpoint to its upstream source. |
| `yolov8n.pt` | Referenced by configuration and the legacy downloader; see Ultralytics above. A custom checkpoint needs its own provenance and license. |
| PaddleOCR checkpoints | The legacy downloader still refers to PaddleOCR; the active OCR path uses Surya. Check the exact artifact's terms if using that helper or a PaddleOCR integration. |
| Optional `deface` / CenterFace, OpenCV Haar cascades | The face detector tries `deface` when installed and otherwise uses OpenCV's bundled cascade. These are separate code/model artifacts; preserve their individual notices and verify the version and model actually used. `deface` is not a declared dependency. |
| `models/insurance_ner` and other custom models | User-provided or trained artifacts. This repository grants no rights to their base models or training datasets. Record their provenance and terms separately. |
| Docling model artifacts | Depend on the installed Docling release and enabled parsing path. Preserve the license and revision of each downloaded model; the library's MIT license does not establish a license for all model artifacts. |

## Datasets and user documents

Benchmark loaders and training scripts do not relicense the data they access.
Review each dataset's publisher terms, access agreements, and redistribution
conditions. The same applies to documents supplied by users. PII Zero's project
license does not grant permission to publish personal information or redistribute
third-party datasets.
