# Jira/Confluence Automation Project Constitution

**Status:** Draft for review  
**Version:** 1.0.0

This constitution defines the principles that all project specifications, plans, and implementations must follow. Feature specifications define behavior; this document defines the constraints and quality standards for delivering it.

## Core Principles

### 1. Human Authorization for External Changes

- Every operation that creates or changes Jira or Confluence data must be explicitly authorized by an authenticated user.
- For the initial Jira issue workflow, each proposed issue must be reviewed and approved individually. Unattended creation and batch approval are out of scope.
- Do not update or delete existing Jira or Confluence content unless a reviewed feature specification explicitly authorizes that behavior.

### 2. Evidence-Based Automation

- AI-assisted outputs must be grounded in supplied or authorized source content and must preserve enough evidence for the user to verify them.
- For meeting-note action extraction, include the supporting note excerpt; do not turn speculation into work or infer unstated owners or due dates.
- Represent uncertain or missing information as uncertain or missing. Keep drafts editable and require user review before external writes.

### 3. Security, Privacy, and Least Privilege

- Restrict the application to authorized users and use least-privilege access to Jira, Confluence, and the database.
- Keep Atlassian credentials and other secrets on the server; never expose or store them in browser code or plaintext records.
- Protect sensitive content in transit and at rest. Do not log full meeting notes, credentials, or unnecessary personal data.
- Do not send user content to an external extraction provider until its data handling and organizational approval are confirmed. Define retention and deletion behavior before production use.

### 4. Fail-Safe Integrations

- Validate the configured Jira project, permissions, required fields, and supported issue types before enabling issue creation.
- Complete duplicate checks before presenting Jira candidates for approval. If duplicate checking fails, block creation rather than bypassing the safeguard.
- Make external writes idempotent where practical. Before retrying an ambiguous result, verify whether the original operation succeeded.
- Report validation, authentication, search, extraction, and write failures distinctly. Never present an unverified or failed operation as successful.

### 5. Clear Integration Boundaries

- Keep Jira, Confluence, and extraction-provider interactions behind server-side adapters with replaceable interfaces.
- The browser communicates with the application API; it must not connect directly to PostgreSQL or call Atlassian APIs using application-held credentials.
- Keep provider-specific behavior out of the user workflow so approved integrations can change without rewriting that workflow.

### 6. Requirements-Driven, Verifiable Delivery

- Each feature must have a reviewed specification with testable acceptance criteria before implementation.
- Plans and tasks must trace back to approved requirements, including permissions, external side effects, failure behavior, and relevant data handling.
- Test extraction validation, issue mapping, duplicate decisions, and approval rules with unit tests; use authorized test environments for integration tests and representative non-sensitive data for evaluation.
- Before release, verify the implemented behavior against the specification, including failure and retry cases.

### 7. Simplicity and User Clarity

- Choose the simplest design that satisfies approved requirements; avoid speculative integrations and abstractions.
- Make review decisions, duplicate warnings, successes, and failures clear to the user. Do not silently skip work or infer decisions on the user's behalf.
- Keep unresolved requirements explicit instead of inventing project, identity, field-mapping, retention, or duplicate-matching policies.

## Technology Constraints

- **Frontend:** React 18 with Vite.
- **Backend:** Node.js with Express.
- **Database:** PostgreSQL 15, run via Docker.
- Database access and third-party integrations are server-side responsibilities. Persisted schema changes must use reviewed, versioned migrations.
- Changing these baseline technologies requires an explicit, reviewed update to the project plan and this constitution.

## Governance

- This constitution applies to all feature specifications, plans, tasks, and implementation decisions.
- If a feature conflicts with a principle, resolve the conflict in the specification or propose an explicit constitution amendment before implementation.
- Amendments must record the reason and be reviewed; dependent specifications and plans must then be checked for consistency.
- Requirements not settled by the product specification remain open decisions and must be confirmed before the affected behavior is enabled.
