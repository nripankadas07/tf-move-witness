# Candidate brief and comparison — 14 October 2026

**User:** Infrastructure reviewers preparing instance-explicit state rename declarations. **Painful task:** A chain of moves can intersect an occupied address or converge onto one destination before a reviewer reaches the real Terraform plan.

**Smallest useful capability:** Trace exact managed-resource address moves across chains against a supplied state-address list, rejecting cycles, occupied intermediate/final destinations and actual fan-in collisions.

**Acceptance:** the supplied synthetic example must produce the documented installed result; core edge cases and invalid-input paths must pass; a wheel installed outside the checkout must run the CLI and reject malformed input. The public default commit, remote matrix CI and rendered documentation must be verified before LIVE.

**Demand evidence:** inferred from the workflow and relevant accessible documentation/issues, not a verified customer request. **Discovery path:** descriptive repository topics, a runnable example, searchable edge-case documentation and the user's chronological portfolio index. No unsolicited promotion is performed.

**Distinctness:** No Terraform tool existed in the inspected 173-repository inventory. Generic graph/index utilities do not provide occupied-state identity and typed address checks. PostgreSQL candidate analyzes runtime waiting; this candidate checks a proposed address migration.

## Current comparables

hashicorp/terraform is the highest-star relevant infrastructure engine found in the terraform query. The higher devops-exercises result is an exercise collection, not a comparable engine. Queries were executed live on GitHub with Sort by Most stars. Search result coverage is bounded to visible first pages, then relevant established repositories; stars inform discovery, not quality or performance.

| Repository | Stars observed | Latest push observed UTC | License metadata | Observation UTC |
| --- | ---: | --- | --- | --- |
| [hashicorp/terraform](https://github.com/hashicorp/terraform) | 49909 | 2026-10-13T16:57:47Z | NOASSERTION | 2026-10-14T06:09:39.634Z |
| [opentofu/opentofu](https://github.com/opentofu/opentofu) | 30486 | 2026-10-13T22:07:35Z | MPL-2.0 | 2026-10-14T06:09:40.148Z |
| [minamijoyo/tfmigrate](https://github.com/minamijoyo/tfmigrate) | 1279 | 2026-09-26T03:58:05Z | MIT | 2026-10-14T06:09:39.693Z |

Terraform and OpenTofu produce authoritative infrastructure plans and validate providers. tfmigrate integrates state migration into GitOps. This MVP runs before those tools with explicitly captured addresses; its conservative collisions can reject a plan the real runtime handles differently.

Comparables' current READMEs, installation examples and accessible issues were inspected. Established tools supply broader integration, docs and community support; this project's support consists of reproducible GitHub reports, source tests and explicit bounded semantics. Its clean install has no runtime dependencies, but that alone establishes no time-to-first-result or reliability advantage. Comparator install success and benchmark performance were not measured. License metadata marked NOASSERTION is unresolved metadata, not a permissive-reuse claim. No reuse was needed.

[Primary behavior reference](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring). Competitor README blob hashes, exact star query URLs and source observations are retained in the dated profile research receipt. A local success proves our example, not absence of the behavior in a competitor. Negative results and unsupported configurations remain visible; no superiority claim is made.
