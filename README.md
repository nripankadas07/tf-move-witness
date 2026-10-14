# tf-move-witness

Trace exact managed-resource address moves across chains against a supplied state-address list, rejecting cycles, occupied intermediate/final destinations and actual fan-in collisions.

Built for infrastructure reviewers preparing instance-explicit state rename declarations. A chain of moves can intersect an occupied address or converge onto one destination before a reviewer reaches the real Terraform plan.

## Quickstart

Python 3.10+; no runtime dependencies. The build uses setuptools from the official Python registry. This repository is the install source; no external registry release is claimed.

```sh
git clone https://github.com/nripankadas07/tf-move-witness.git
cd tf-move-witness
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/tf-move-witness example.json
```

On Windows, use `.venv\Scripts\python` and `.venv\Scripts\tf-move-witness`. Windows behavior has not been exercised; Linux CI is configured to verify Python 3.10, 3.12 and 3.14. An input filename or `-` for standard input is required. Valid analysis returns exit 0, including negative findings; malformed or unsupported input returns exit 2 and a JSON error on stderr. Input is bounded to 1 MiB; duplicate JSON keys and nonfinite numbers fail.

The runnable [example](example.json) uses synthetic data. Run `python tf_move_witness.py example.json` directly for a source-only demo. Import `analyze(data)` for the Python API; unsupported input raises an exception. The tool makes no network request or operational write.

## Input and output contract

Top level state is a unique address string array; moves is an array of exactly from/to address strings. Grammar supports module.NAME[index]. prefixes followed by TYPE.NAME[index], with a nonnegative numeric or canonical JSON string index. Exact unindexed addresses mean singleton objects. A missing source is reported, not invented. Unused_sources names declarations whose from address was not initially present, including historical intermediate links.

The example's installed behavior is asserted in [test_installed_cli.py](test_installed_cli.py). [Unit cases](test_behavior.py) cover positive decisions and meaningful failure cases. The report records actual captured evidence; absence of a finding does not certify an operational environment.

## Limits

Not Terraform or a plan simulator. No HCL/state-file parser, provider schema, real resources, state writes, workspace migration, module-wide moves, whole-resource moves over indexed instances, data-resource moves or cross-type moves. Enumerate exact instances. Canonical JSON quoting is required for string keys; escaping alternatives fail rather than alias silently. State <=1000 addresses, moves <=256.

## Validation and research

Run `python -m unittest -v` and `python -m compileall -q tf_move_witness.py`. [Validation](VALIDATION.md) records exercised configurations. [Research and candidate brief](RESEARCH.md) compares current alternatives and states the inferred demand. No customer adoption or measured performance advantage is claimed.

## Contributing and support

[Contribution guide](CONTRIBUTING.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [MIT license](LICENSE)

Original implementation developed with AI assistance and reviewed through acceptance tests. No competitor source, branding or prose was copied. Primary specifications informed the explicitly supported semantics.
