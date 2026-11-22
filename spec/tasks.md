# Tasks: Meeting Notes to Jira/Confluence Automation

**Input**: [Implementation plan](./plan.md), [feature specification](./specification.md), and project constitution  
**Status**: Draft; implementation tasks are gated by Phase 0 decisions.

## Phase 0: Resolve Scope and Freeze Requirements

**Purpose**: Reconcile the written Jira-only specification with the user's decision to include Confluence and confirm decisions that affect external operations, privacy, and data handling.

- [ ] T001 [M0] Update `spec/specification.md` to reflect that only the project manager may use the application and that Confluence is in scope. Preserve the existing Jira requirements.  
  **Acceptance criteria**: The spec states the single-user role/access boundary; FR-026 no longer prohibits the intended Confluence scope; no Confluence operation is invented.
- [ ] T002 [M0] Define and document the approved Confluence workflows in `spec/specification.md`.  
  **Acceptance criteria**: Each approved operation identifies its user goal, Confluence content/space scope, data read or written, authorization and approval requirements, failure behavior, and testable acceptance scenarios. Unselected operations are explicitly out of scope.
- [ ] T003 [M0] Select the application identity and Jira/Confluence authentication approach; record it in `spec/specification.md` or an approved design decision.  
  **Acceptance criteria**: The project manager's sign-in and Atlassian authorization model, token handling, revocation, and reauthorization behavior are documented and consistent with least privilege.
- [ ] T004 [M0] Confirm the Jira project and issue-creation configuration.  
  **Acceptance criteria**: The project key, supported issue types, required fields, field mappings, allowed values, and configuration owner are documented and validated against an approved test project.
- [ ] T005 [M0] Define duplicate matching and uncertain-match handling.  
  **Acceptance criteria**: Jira search scope, matching signals, threshold, treatment of resolved issues, and the user's decision options for uncertain matches are specified; confirmed likely duplicates remain blocked from creation.
- [ ] T006 [M0] Confirm note-upload and text-input constraints.  
  **Acceptance criteria**: The spec lists supported file formats, maximum size, language support, and whether mixed or multiple inputs are allowed; invalid-input behavior is testable.
- [ ] T007 [M0] Approve the extraction approach and its data handling.  
  **Acceptance criteria**: The provider or local approach, organizational approval, data-handling constraints, representative evaluation data, and acceptance thresholds for missed/unsupported actions and evidence are recorded.
- [ ] T008 [M0] Define session lifecycle, persistence, retention, and deletion.  
  **Acceptance criteria**: The spec defines when sessions start/end, whether they can be resumed, how long notes/drafts/results remain available (including failed drafts), and how deletion is performed.
- [ ] T009 [M0] Define candidate approval and retry semantics.  
  **Acceptance criteria**: Approval is tied to a defined candidate draft; edit-after-approval behavior, rejection/reopen behavior, and safe handling of concurrent or ambiguous create requests are specified.
- [ ] T010 [M0] Confirm measurable release and operational targets.  
  **Acceptance criteria**: Any required performance, availability, scale, supported-browser, and data-residency targets are documented, or explicitly marked not required for the initial release.
- [ ] T011 [M0] Review and reconcile `spec/constitution.md`, `spec/specification.md`, and `spec/plan.md`.  
  **Acceptance criteria**: No unresolved scope contradiction remains; remaining undecided items are marked as gates; the project owner approves the baseline before implementation tasks proceed.

**Milestone M0**: Approved, internally consistent implementation baseline. All later tasks that depend on an unresolved decision remain blocked.

## Phase 1: Development Foundation

**Purpose**: Make the existing frontend/API/shared/test folder skeleton runnable and establish local development conventions.

- [ ] T012 [M1] Confirm the Node.js version, JavaScript/TypeScript choice, package manager, workspace conventions, and test/lint tooling.  
  **Acceptance criteria**: The choices are recorded in the plan or developer documentation and are compatible with React 18, Vite, Express, and the supported development environment.
- [ ] T013 [M1] Create workspace manifests and scripts at `package.json`, `apps/web/package.json`, `apps/api/package.json`, and `packages/shared/package.json`.  
  **Acceptance criteria**: Workspace install and documented development scripts complete successfully without adding feature behavior.
- [ ] T014 [M1] Configure the React 18/Vite app under `apps/web/`.  
  **Acceptance criteria**: The frontend starts locally and loads a minimal application shell; the Vite build succeeds.
- [ ] T015 [M1] Configure the Node.js/Express app under `apps/api/`.  
  **Acceptance criteria**: The API starts locally and exposes a basic readiness endpoint without exposing credentials or requiring Atlassian access.
- [ ] T016 [M1] Add local PostgreSQL 15 Docker configuration and secret-free environment templates.  
  **Acceptance criteria**: The database starts using documented commands; committed configuration contains placeholders only and no credentials.
- [ ] T017 [M1] Establish shared request/response contracts in `packages/shared/src/contracts/`.  
  **Acceptance criteria**: Frontend and API can consume the same typed or validated contract definitions; contract validation rejects malformed payloads.
- [ ] T018 [M1] Add backend error handling and readiness checks in `apps/api/src/`.  
  **Acceptance criteria**: API readiness distinguishes process startup from database connectivity; errors use a consistent response shape and are not represented as success.

**Milestone M1**: Frontend, API, and PostgreSQL can be started and checked locally using documented commands.

## Phase 2: Identity, Session, and Data Foundations

**Purpose**: Implement the approved single-user access policy and data lifecycle before storing meeting notes or calling Atlassian services.

- [ ] T019 [M2] Implement the approved project-manager authentication and authorization in `apps/api/src/auth/` and `apps/web/src/`.  
  **Acceptance criteria**: Unauthenticated requests cannot access sessions or invoke protected operations; only the configured project manager can use the application.
- [ ] T020 [M2] Add versioned PostgreSQL migrations for sessions, source notes/references, candidates, duplicate matches, decisions, and results.  
  **Acceptance criteria**: A clean database can be migrated to the current schema and migration rollback/recovery behavior is documented.
- [ ] T021 [M2] Implement session and candidate persistence in `apps/api/src/sessions/`.  
  **Acceptance criteria**: Records follow the approved lifecycle and retention rules; session data is not accessible outside the authorized user's boundary.
- [ ] T022 [M2] Implement retention and deletion behavior for notes, drafts, decisions, matches, and results.  
  **Acceptance criteria**: Expired or user-deleted data is removed according to the approved policy, including stored upload content or references.
- [ ] T023 [M2] Record approval and external-operation audit events without sensitive content in `apps/api/src/`.  
  **Acceptance criteria**: An authorized reviewer can determine who approved which final candidate and the outcome of the associated operation; audit records omit full notes and secrets.
- [ ] T024 [M2] Add tests for authorization, session isolation, persistence, and deletion.  
  **Acceptance criteria**: Tests demonstrate denied unauthorized access, correct owner isolation, and retention/deletion behavior against PostgreSQL.

**Milestone M2**: The authorized project manager can create and access a session whose data follows the approved persistence and privacy policy.

## Phase 3: Notes Intake and Evidence-Based Extraction

**User Story 1**: Submit notes and review proposed actions.

- [ ] T025 [US1] Implement text-note submission and input validation in `apps/web/src/features/sessions/` and `apps/api/src/routes/`.  
  **Acceptance criteria**: Valid text creates a processing session; empty or invalid input produces a clear error and no success-shaped session.
- [ ] T026 [US1] Implement the approved file-upload path in `apps/web/src/features/sessions/` and `apps/api/src/`.  
  **Acceptance criteria**: Only approved formats and sizes are accepted; unreadable, unsupported, or invalid files are rejected safely and reported clearly.
- [ ] T027 [US1] Implement the extraction-provider interface and approved adapter in `apps/api/src/extraction/`.  
  **Acceptance criteria**: Provider-specific logic is server-side and replaceable; notes are not sent to an unapproved provider; provider failures are distinguishable from successful extraction.
- [ ] T028 [US1] Validate extraction output and construct evidence-backed action candidates in `apps/api/src/extraction/` and `apps/api/src/services/`.  
  **Acceptance criteria**: Candidates require valid evidence excerpts; speculative or uncommitted statements are excluded; unstated owners and due dates remain unset; malformed output is rejected or reported.
- [ ] T029 [US1] Implement candidate/session status reporting in `apps/api/src/sessions/` and shared contracts.  
  **Acceptance criteria**: Empty results, processing failures, partial results, and completed extraction have distinct states defined by the approved specification.
- [ ] T030 [US1] Build the session submission and candidate display UI in `apps/web/src/features/sessions/` and `apps/web/src/components/`.  
  **Acceptance criteria**: The project manager can submit approved input types and inspect each candidate's proposed action, summary, description, issue type, evidence, and missing/uncertain fields.
- [ ] T031 [US1] Add extraction and input tests under `tests/`.  
  **Acceptance criteria**: Tests cover text and approved files, unsupported inputs, explicit versus speculative actions, missing fields, missing evidence, malformed provider output, and no-action sessions.
- [ ] T032 [US1] Run the approved extraction evaluation dataset and record results.  
  **Acceptance criteria**: Missed-action, unsupported-action, and evidence-quality results meet the thresholds approved in T007, or failures are documented and block the milestone.

**Milestone M3**: Approved note inputs produce reviewable, evidence-backed candidates meeting the agreed extraction criteria.

## Phase 4: Jira Configuration and Duplicate Screening

**User Story 2**: Identify and review possible duplicates.

- [ ] T033 [US2] Implement Jira authentication and project/configuration preflight in `apps/api/src/jira/` and `apps/api/src/config/`.  
  **Acceptance criteria**: The backend verifies the authorized identity, project access, supported issue types, required fields, and configured mappings; failed checks disable creation and identify the failed check.
- [ ] T034 [US2] Implement Jira search and duplicate classification in `apps/api/src/jira/` and `apps/api/src/duplicates/`.  
  **Acceptance criteria**: Search uses only the approved project scope and matching rules; results include issue key, summary, link, and match status; search failures block downstream approval/creation as specified.
- [ ] T035 [US2] Implement duplicate and possible-match presentation in `apps/web/src/features/review/`.  
  **Acceptance criteria**: Confirmed likely duplicates are clearly marked skipped and cannot be created; uncertain matches follow the approved resolution workflow; non-duplicates proceed to review.
- [ ] T036 [US2] Add Jira test-project integration tests under `tests/integration/`.  
  **Acceptance criteria**: Tests cover matching, non-matching, uncertain, inaccessible-project, and search-failure outcomes without using production data.

**Milestone M4**: Jira configuration is validated and every candidate receives a fail-safe duplicate decision before approval.

## Phase 5: Candidate Review and Jira Issue Creation

**User Story 3**: Approve, reject, and create issues individually.

- [ ] T037 [US3] Implement editable candidate drafts in `apps/web/src/features/review/`.  
  **Acceptance criteria**: The project manager can edit only the fields allowed by the approved spec; required-field validation is shown before approval.
- [ ] T038 [US3] Implement per-candidate review state and approval binding in `apps/api/src/services/` and `apps/api/src/sessions/`.  
  **Acceptance criteria**: Approve/reject applies to one candidate only; approval is bound to the final draft; edits after approval trigger the approved reapproval behavior; batch approval is unavailable.
- [ ] T039 [US3] Implement Jira issue validation and creation in `apps/api/src/jira/`.  
  **Acceptance criteria**: Only an individually approved, validated, non-duplicate candidate can be created; each candidate creates at most one issue; initial-release updates, closes, assignments, and deletes are not performed.
- [ ] T040 [US3] Implement safe retry and idempotency handling for Jira creation in `apps/api/src/jira/` and `apps/api/src/services/`.  
  **Acceptance criteria**: Definite and ambiguous failures follow the approved retry policy; after an ambiguous response the backend checks creation state before retrying; concurrent attempts cannot create duplicate issues.
- [ ] T041 [US3] Implement per-candidate outcomes in `apps/web/src/features/results/`.  
  **Acceptance criteria**: Successful issues show key and URL; rejected drafts, skipped duplicates, pending work, and failures are visibly distinct; failures are never displayed as success.
- [ ] T042 [US3] Add approval, creation, and retry tests under `tests/`.  
  **Acceptance criteria**: Tests prove no write occurs without explicit approval, only the approved candidate is created, duplicates/search failures block creation, failures retain editable drafts, and ambiguous retries do not duplicate issues.

**Milestone M5**: The project manager can safely review candidates and create only individually approved Jira issues.

## Phase 6: Approved Confluence Workflows

**Dependency**: T002 and T003 must be complete. Implement only workflows approved in the updated specification.

- [ ] T043 [US4] Implement the server-side Confluence adapter in `apps/api/src/confluence/`.  
  **Acceptance criteria**: The adapter exposes only the approved operations, uses the selected authorization model, and does not expose credentials or unrestricted page/space access to the browser.
- [ ] T044 [US4] Implement the approved Confluence user workflow in `apps/api/src/` and `apps/web/src/features/`.  
  **Acceptance criteria**: Behavior matches an approved Confluence acceptance scenario; each content-changing action requires explicit authorization; no unapproved operation is reachable.
- [ ] T045 [US4] Add Confluence integration tests under `tests/integration/`.  
  **Acceptance criteria**: Tests cover each approved operation, permission failures, validation failures, and external-service errors in an authorized test environment.

**Milestone M6**: Every approved Confluence workflow operates within its documented scope and authorization rules.

## Phase 7: System Validation and Release Readiness

- [ ] T046 [P] Add end-to-end coverage under `tests/e2e/` for the complete note-to-result workflow.  
  **Acceptance criteria**: Tests cover text and approved file inputs, candidate review, duplicate behavior, individual approval/rejection, Jira results, and approved Confluence workflows.
- [ ] T047 [P] Verify privacy, security, and secret handling across `apps/web/`, `apps/api/`, and Docker configuration.  
  **Acceptance criteria**: No credentials appear in browser bundles, committed configuration, or logs; protected routes and session data are inaccessible to unauthorized users; retention/deletion checks pass.
- [ ] T048 [P] Run the agreed extraction and duplicate-quality evaluation.  
  **Acceptance criteria**: Results meet the approved thresholds and use representative non-sensitive data; any miss or unsupported proposal is recorded for triage.
- [ ] T049 Document local setup, required external configuration, and known limitations in `README.md`.  
  **Acceptance criteria**: A developer can follow the documented setup from a clean checkout without production credentials; unresolved operational constraints are listed.
- [ ] T050 Run the complete applicable validation suite and reconcile results with the acceptance criteria.  
  **Acceptance criteria**: Lint, type-check/build, unit, integration, and end-to-end results are recorded; no blocking failure or unresolved safety gate is represented as passing.

**Milestone M7**: The release candidate satisfies the reviewed specification, constitution, security requirements, and agreed quality thresholds.

## Dependencies and Execution Order

- **M0 / T001–T011** must complete before implementing authentication, extraction providers, Jira creation, or Confluence behavior.
- **M1 / T012–T018** establishes the runnable project and is a prerequisite for application development.
- **M2 / T019–T024** depends on M1 and blocks persistence of source notes and authenticated external integrations.
- **US1 / T025–T032** depends on M0–M2 and the extraction-provider/input decisions.
- **US2 / T033–T036** depends on M0–M2 and the Jira authorization, project configuration, and duplicate policy decisions.
- **US3 / T037–T042** depends on US1 and US2; writes remain disabled until configuration and duplicate checks pass.
- **US4 / T043–T045** depends on M0–M2 and the approved Confluence operations and authorization model.
- **M7 / T046–T050** depends on all in-scope features.
- Tasks marked `[P]` can run in parallel after their dependencies are complete; other work should proceed in phase and dependency order.

## Execution Notes

- All tasks are unchecked; this file is a plan, not a record of completed work.
- Tasks gated on unresolved requirements must remain blocked until the corresponding specification decision is approved.
- Tests are included because the constitution and verification approach require unit, integration, end-to-end, and evaluation coverage.
