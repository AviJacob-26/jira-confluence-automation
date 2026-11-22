- **Input format**
  + Accept the project or repository root to validate.
  + Accept optional targets such as changed files, a specific package, or a test suite.
  + Accept optional environment details needed to run integration or end-to-end tests.
  + Accept configured lint, type-check/build, unit, integration, or end-to-end commands.
  + Accept a change summary or implementation diff when available.
  + Treat missing commands as discoverable configuration and inspect project manifests, scripts, documentation, and existing CI configuration.

- **Processing steps**
  + Identify the project root and framework from repository files.
  + Read existing documentation and CI configuration before selecting commands.
  + Reuse project-defined scripts and commands instead of inventing unrelated tooling.
  + Establish a validation baseline before implementation fixes when a baseline is available.
  + Run lint first, then type-check/build, unit tests, integration tests, and end-to-end tests.
  + Stop or narrow later stages when a missing prerequisite, secret, service, or environment makes a stage unsafe or unavailable.
  + Capture the exact command, exit status, failing file/test, and first actionable error for every failed stage.
  + Separate failures introduced by the implementation from pre-existing or environment-only failures.
  + Reproduce each introduced failure locally and identify its root cause before editing.
  + Fix only failures caused by or tightly coupled to the implementation.
  + Re-run the smallest targeted lint, type-check, or test selector after each fix.
  + Re-run the full applicable validation suite after targeted checks pass.
  + Add or update focused tests for behavior changed or fixed by the implementation.
  + Verify formatting, build artifacts, generated files, and test state after the suite completes.
  + Do not retry an external integration or end-to-end dependency repeatedly without a diagnosis.

- **Output format**
  + Return a Markdown validation report with these sections in order: `## Commands`, `## Results`, `## Failures`, `## Fixes`, `## Verification`.
  + In `## Commands`, list every command run and the working directory used.
  + In `## Results`, report pass, fail, blocked, or skipped for lint, type-check/build, unit, integration, and end-to-end stages.
  + In `## Failures`, group failures as introduced, pre-existing, or environment; include file/test names and concise root causes.
  + In `## Fixes`, list precise code or configuration changes made for introduced failures.
  + In `## Verification`, state the final targeted and full-suite results, or state exactly why validation remains blocked.
  + Include exit status or test totals for each completed command when available.
  + Keep output concise and exclude irrelevant command logs.

- **Constraints**
  + Run no destructive or reset command to resolve validation failures.
  + Do not modify unrelated code, suppress failing checks without a justified code fix, or weaken test assertions.
  + Do not add dependencies or change dependency manifests unless required and explicitly justified.
  + Do not expose secrets, credentials, personal data, or full environment dumps in output.
  + Do not call external services or integration environments without authorized configuration.
  + Do not claim a failure is fixed until its targeted check and the relevant broader suite pass.
  + Do not label an unavailable prerequisite as a test failure.
  + Preserve the project's existing lint, test, formatting, and CI conventions.
  + Report all unresolved failures explicitly instead of returning a success-shaped fallback.
