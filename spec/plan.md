# Implementation Plan: Meeting Notes to Jira/Confluence Automation

**Branch**: `not-assigned` | **Date**: 2026-11-22 | **Spec**: [specification.md](./specification.md)

**Input**: Feature specification plus the user's clarification that Confluence is in scope and the project manager is the only application user. The Jira/Confluence authentication method remains undecided.

## Summary

Deliver an internal web application for the project manager to submit stand-up notes, review evidence-backed action candidates, avoid duplicate Jira issues, and create only individually approved issues. Include Confluence in the project scope, but do not implement Confluence operations until the required workflows and authorization rules are specified.

Use the established React 18/Vite frontend, Node.js/Express backend, and PostgreSQL 15 database running via Docker. Keep AI extraction and Atlassian integrations behind server-side adapters. The current repository already contains an empty frontend, API, shared-contracts, and test folder skeleton.

**Planning gate**: The written feature specification still says Confluence reads and writes are out of scope (FR-026), and the duplicate-resolution, authentication, and data-retention decisions remain open. Update and review the specification before implementing affected features. This plan does not assume which Confluence operations will be supported.

## Technical Context

**Language/Version**: React 18 specified; Node.js version and JavaScript-versus-TypeScript choice need confirmation  
**Primary Dependencies**: Vite, React 18, Node.js, Express; extraction and Atlassian client/provider choices need approval  
**Storage**: PostgreSQL 15 via Docker; persisted data scope, session lifecycle, and retention need confirmation  
**Testing**: Unit, integration, and end-to-end testing required; runner and exact commands are not yet selected  
**Target Platform**: Internal web application; hosting environment, browser support, and data residency need confirmation  
**Project Type**: Web application with frontend, API, and shared contracts  
**Performance Goals**: **[NEEDS CLARIFICATION: response-time, throughput, and availability targets are unspecified]**  
**Constraints**: External writes require explicit user authorization; Jira duplicate-search failure blocks creation; secrets and Atlassian API calls remain server-side  
**Scale/Scope**: One application user (project manager) per clarification; production-support context includes a 14-person team. Expected session volume is unspecified.

## Constitution Check

- **Human authorization**: Jira and any future Confluence writes require explicit authorization; Jira issue approval is per candidate.
- **Privacy and least privilege**: Authentication and secret handling must be settled before connecting to Atlassian services. Do not send notes to an external extraction provider before approval.
- **Fail-safe integration**: Jira issue creation remains disabled until project/field validation and duplicate checking succeed.
- **Integration boundaries**: The browser calls the application API only; PostgreSQL and Atlassian services are accessed by the backend.
- **Evidence and verification**: Candidates must retain evidence excerpts; tests must cover unsupported/speculative actions, duplicates, approval, failures, and retry behavior.
- **Outstanding gate**: The constitution and feature specification are drafts. Resolve the scope mismatch for Confluence and review the updated specification before integration implementation.

## Project Structure

### Documentation

```text
spec/
├── constitution.md
├── specification.md
├── clarify.md
└── plan.md
```

### Source Code

```text
apps/
├── web/
│   └── src/
│       ├── api/
│       ├── components/
│       └── features/
│           ├── sessions/
│           ├── review/
│           └── results/
└── api/
    └── src/
        ├── auth/
        ├── config/
        ├── confluence/       # Add after Confluence workflows are specified
        ├── duplicates/
        ├── extraction/
        ├── jira/
        ├── routes/
        ├── services/
        └── sessions/
packages/
└── shared/
    └── src/
        └── contracts/
tests/
├── e2e/
└── integration/
```

**Structure Decision**: Extend the existing `apps/web`, `apps/api`, `packages/shared`, and `tests` skeleton. Keep provider-specific code in the API adapters and use shared contracts for frontend/API data. Add database migrations and local Docker configuration during the foundation phase, after package and environment conventions are selected.

## Phases and Milestones

### Phase 0 — Resolve Scope and Freeze Requirements

**Milestone M0: Approved implementation baseline**

- Update the feature specification to reflect the user's decisions: Confluence is in scope and only the project manager uses the application.
- Define the Confluence workflows, data sources/destinations, read/write boundaries, and approval behavior. Do not infer these from the project name.
- Select the approved app identity and Jira/Confluence authorization approach, consistent with using the approving user's identity.
- Resolve blocking Jira project/field configuration, duplicate matching and uncertain-match handling, supported upload formats/limits, extraction-provider approval, and session retention.
- Agree on measurable extraction/duplicate evaluation criteria and release acceptance thresholds.
- Re-run a consistency review against the constitution; update FR-026 and related scenarios/requirements.

**Exit criteria**: The feature specification no longer contradicts the intended Confluence scope; all decisions needed to safely implement authentication, data retention, Jira creation, and the selected Confluence workflows are explicit and reviewed.

### Phase 1 — Development Foundation

**Milestone M1: Reproducible local development environment**

- Confirm Node.js version, JavaScript or TypeScript, package manager, workspace layout, and test tooling.
- Turn the existing folder skeleton into runnable React 18/Vite and Node.js/Express applications.
- Add local Docker configuration for PostgreSQL 15, configuration templates without secrets, and database migration conventions.
- Add minimal frontend/API startup checks and backend/database readiness checks.
- Define shared API contracts and a consistent error response shape before feature routes are added.

**Exit criteria**: A developer can start the frontend, API, and PostgreSQL locally using documented commands; health/readiness checks distinguish service startup from database connectivity; no credentials are committed.

### Phase 2 — Identity, Session, and Data Foundations

**Milestone M2: Authorized project-manager session flow**

- Implement the approved authentication and access policy for the single project-manager user.
- Define session, candidate, review-decision, duplicate-match, and result records and their relationships.
- Add versioned PostgreSQL migrations and repository/service boundaries.
- Implement the approved notes/session retention and deletion lifecycle, including access isolation.
- Record minimum audit information for approval and external-operation results without logging full notes or secrets.

**Exit criteria**: Only the authorized project manager can access session data; persistence and deletion behavior match the approved policy; migration and access-isolation tests pass.

### Phase 3 — Notes Intake and Evidence-Based Extraction

**Milestone M3: Validated notes produce reviewable candidates**

- Implement text entry and only the approved file formats, limits, and languages.
- Validate and reject unsupported or unreadable inputs with clear errors; preserve source notes for the approved session lifetime.
- Implement an extraction adapter only after provider and data-handling approval.
- Validate extraction output; create candidates only for explicit or clearly committed actions and retain supporting excerpts.
- Leave unstated owners and due dates unset; flag uncertainty and missing fields.
- Add representative, non-sensitive evaluation cases and tests for speculation, ambiguity, malformed output, and no-action sessions.

**Exit criteria**: Accepted inputs produce candidates that meet the approved evaluation thresholds; invalid inputs and extraction failures are visible and never appear successful.

### Phase 4 — Jira Configuration and Duplicate Screening

**Milestone M4: Authorized project discovery and duplicate screening**

- Implement the server-side Jira adapter and validate the user's authorized Jira identity.
- Validate Jira identity, project access, supported issue types, required fields, and configured mappings before enabling writes.
- Implement Jira duplicate search with the approved scope, signals, threshold, and uncertain-match behavior.
- Surface matching issue keys, summaries, and links; block issue creation on search failure.
- Add authorized integration tests using approved test resources. Do not use production data for routine tests.

**Exit criteria**: Jira project/configuration checks and duplicate-search results are correct in the test environment; failures block dependent writes. No Confluence behavior is implemented in this phase.

### Phase 5 — Candidate Review and Jira Issue Creation

**Milestone M5: Individually approved candidates create at most one issue**

- Build the review interface for evidence, draft fields, missing/uncertain values, duplicate warnings, and per-candidate edit/approve/reject decisions.
- Bind approval to the final draft content; require renewed approval if approved content changes.
- Validate each approved candidate against configured Jira fields before submission.
- Create no more than one Jira issue per approved candidate; do not create likely duplicates or support batch/unattended approval.
- Implement safe retry/idempotency behavior, including verification after ambiguous Jira responses.
- Show successful Jira keys/links and clearly distinguish rejected, skipped, pending, and failed candidates.

**Exit criteria**: End-to-end tests prove no issue is created without approval, duplicates and failed searches block creation, and retries do not create an unverified second issue.

### Phase 6 — Approved Confluence Workflows

**Milestone M6: Specified Confluence operations work within approved boundaries**

- Implement the Confluence operations selected and specified in Phase 0; separate read-only behavior from writes.
- Require explicit authorization for each operation that creates or changes Confluence content.
- Validate page/space permissions and required content fields before writes; report external failures without success-shaped fallbacks.
- Add test-environment integration coverage for each approved Confluence workflow.

**Exit criteria**: Every implemented Confluence operation maps to a reviewed acceptance scenario; no operation outside the approved scope is possible; all writes are authorized and auditable.

### Phase 7 — System Validation and Release Readiness

**Milestone M7: Acceptance criteria verified for release**

- Run unit tests for input validation, extraction, issue mapping, duplicate decisions, approvals, and state transitions.
- Run integration tests for PostgreSQL migrations, authentication, Jira search/create/retry, and approved Confluence workflows.
- Run end-to-end tests for text/file intake through review and results, including duplicates, rejection, and failure cases.
- Verify privacy controls, redacted logs, access isolation, retention/deletion, and secret handling.
- Evaluate extraction and duplicate quality against the agreed non-sensitive datasets and thresholds.
- Document local setup, required external configuration, operational limitations, and known issues.

**Exit criteria**: All required acceptance criteria and agreed quality thresholds pass; no unresolved blocking clarification remains; failures are reported accurately and do not bypass approval or duplicate safeguards.

## Decision Gates and Dependencies

| Gate | Must be resolved before |
|---|---|
| Confluence workflows and approval boundaries | Confluence adapter or UI work |
| App identity and Jira/Confluence authentication | Any authenticated Atlassian integration |
| Jira project key, required fields, and mappings | Enabling Jira issue creation |
| Duplicate signals, threshold, and uncertain-match outcome | Presenting candidates as safe to approve |
| File formats, limits, and languages | Enabling file upload |
| Extraction provider and data approval | Sending notes to any external provider |
| Retention/deletion and session lifecycle | Persisting source notes and drafts |
| Idempotency and ambiguous retry behavior | Jira create/retry implementation |

## Verification Approach

- **Unit**: Input validation; candidate schema/evidence; issue-type and field validation; duplicate decisions; approval state; retry rules.
- **Integration**: PostgreSQL migrations and persistence; authorized Jira project/search/create flows; only the approved Confluence operations.
- **End-to-end**: Submit notes, inspect evidence, handle duplicate warnings, edit and individually approve/reject candidates, and verify final outcomes.
- **Evaluation**: Use representative non-sensitive notes and the approved metrics for missed actions, unsupported proposals, evidence quality, and duplicate proposals.

## Risks and Open Decisions

- The written specification and the user's latest scope clarification disagree about Confluence. Phase 0 must update the spec before implementation.
- Confluence operations are not yet described; Phase 6 is intentionally conditional on their approval.
- Authentication, extraction provider, upload rules, Jira configuration, duplicate policy, retention, and quality thresholds remain unresolved.
- No performance, availability, scale, hosting, or data-residency targets are set; these may change the plan before release.

## Complexity Tracking

No constitution violations are currently proposed. The frontend, API, shared-contracts package, and database are the project's stated baseline; provider adapters and versioned migrations are required by the constitution, not optional future-proofing. Revisit this section if planning introduces additional services or abstractions.
