# CLA signatures

This branch holds the record of who has signed the PII Zero
[Contributor License Agreement](https://github.com/scamai/pii-zero/blob/main/CLA.md).
It contains no project code.

The CLA workflow (`.github/workflows/cla.yml` on `main`) creates
`signatures/version1/cla.json` on its first run and adds one entry each time a
contributor signs: GitHub username and user ID, comment ID and time, and the
repository and pull request numbers.

Do not edit or create the signatures file by hand, and do not protect this
branch: the workflow commits here with `GITHUB_TOKEN`.
