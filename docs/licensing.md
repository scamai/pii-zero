# Licensing PII Zero

PII Zero's original code and documentation are licensed under the
[GNU Affero General Public License, version 3 only](../LICENSE)
(`AGPL-3.0-only`). [NOTICE](../NOTICE) identifies the project copyright and
warranty disclaimer. Separately licensed material retains its existing terms.

## Using and modifying the project

AGPL permits commercial use, modification, and redistribution subject to its
conditions. It is not a noncommercial license and does not require a purchase
from Scam AI to exercise the rights it grants.

When redistributing covered source or other forms of the program, preserve the
required notices and license, identify modifications, and satisfy the applicable
Corresponding Source requirements. Sections 4–6 of the license describe these
conditions. The source must include the material needed to build, install, run,
and modify the covered work, as defined by the license.

If you modify the program and let users interact with that version remotely over
a network, section 13 requires a prominent offer of its Corresponding Source to
those users, at no charge. This applies to the version they actually use,
including your modifications. A link to unmodified upstream code alone does not
provide the source of your modified deployment.

The review UI and CLI help include license and upstream source links. If you
distribute or host a modified version, retain the legal notices and update the
source offer to provide your corresponding version. This repository does not
automatically publish downstream modifications for you.

Running PII Zero on a document does not, by itself, place that document or the
redacted output under AGPL. The license's treatment of program output is in
section 2; any existing rights in the input still apply.

This guide summarizes the project license; the full license governs.

## Dependencies, models, and datasets

The project license covers the project's original material. It does not
relicense downloaded models, third-party packages, training data, or user
documents. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md), especially
the PyMuPDF, Ultralytics, and version-specific Surya entries.

For a redistributed environment or deployment, record the exact dependency
versions, model identifiers and revisions, and any modifications. Preserve the
licenses and notices shipped with those artifacts, including transitive
dependencies and system libraries where required. A list of package names or
links is not a substitute for the license notices and source that a distribution
must supply.

No alternative commercial license for the combined dependency stack is offered
by this repository. Separate upstream commercial agreements, where available,
must cover the components and uses in question; they do not automatically change
PII Zero's AGPL license.

## Contributions

Submit original contributions under `AGPL-3.0-only`. Keep copyright and license
notices for any included third-party material and document its provenance.
Contributors retain their copyright; this project does not require a copyright
assignment. See the [contribution guide](development.md#contributing).
