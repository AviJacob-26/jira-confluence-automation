# Specification Implementation Checklist

**Compared against:** [specification.md](./specification.md)
**Assessment date:** 2026-11-22

## Status key

- **Yes**: Implemented and verified for the current build.
- **Partial**: Some behavior exists, but the requirement is not fully met.
- **No**: Not implemented, or no working path exists.
- **Current guard only**: The current prototype avoids the prohibited action because the integration or capability is absent; this does not verify a future implementation.

## Current implementation and verification

- **Frontend:** React 18/Vite screen exists. `npm run build` passes. The page returns HTTP 200. A browser smoke check confirmed that the empty submit button is disabled, entering text enables it, and clicking it displays a "Processing is not connected yet" message without sending the notes.
- **API:** Express exposes only `GET /health`. It returned HTTP 200 with `{"status":"ok"}`. This is a process check, not a database readiness check.
- **Database:** Compose runs PostgreSQL 15.20 and reports healthy. Port `127.0.0.1:5432` is reachable, and a SQL query inside the container returned the configured database and user.
- **Integration boundary:** The API has no database connection, migrations, session routes, extraction provider, Jira integration, or Confluence integration. The database is not used by the application.
- **Automated application tests:** The web and API package manifests do not define test scripts. The build and smoke checks above do not verify the end-to-end product workflows.

## Functional requirements

| Requirement | Implemented? | Does it work? | Evidence and remaining gap |
|---|---|---|---|
| **FR-001** Project-manager-only access and sign-in | No | No | There is no sign-in or authorization in the UI or API. The identity provider and access policy remain undecided. |
| **FR-002** Text entry and file upload | Partial | Partial | The text area and character count work locally. Submitting only displays the not-connected message. File upload is not implemented. |
| **FR-003** Confirm upload formats, size, and languages before enabling processing | Partial; safe gate only | Yes for the current gate | No upload path is enabled, and the UI says formats and limits still need confirmation. The decisions remain open; no file processing can be verified. |
| **FR-004** Preserve source notes for a processing session | No | No | Notes exist only in component state; there is no processing session or server persistence, and reloading clears them. |
| **FR-005** Reject invalid or unreadable inputs clearly without false success | No | Partial | No input-processing or validation endpoint exists. The UI does not claim success and warns that notes were not sent, but invalid-input handling is absent. |
| **FR-006** Propose only explicit or clearly committed actions | No | No | No extraction or candidate-generation behavior exists. |
| **FR-007** Include required action, summary, description, evidence, and issue type in candidates | No | No | There is no candidate model or review data. |
| **FR-008** Limit proposed Jira issue types to Story, Task, Bug, and Spike | No | No | No issue-type selection or validation exists. |
| **FR-009** Do not infer unstated owners or due dates | No | No | Candidates and owner/due-date fields are not implemented. |
| **FR-010** Identify missing/uncertain fields and allow draft edits | No | No | There is no candidate review or editing flow. |
| **FR-011** Search the configured Jira project before approval | No | No | There is no Jira client, project configuration, or duplicate-search route. |
| **FR-012** Skip and report likely duplicates without creating or linking them | No | No | Duplicate matching and reporting are absent. |
| **FR-013** Define duplicate signals, threshold, and uncertain-match behavior | No | No | These decisions remain open in the specification; no matching logic exists. |
| **FR-014** Block creation if duplicate search fails | No | No | Neither duplicate search nor issue creation exists, so the failure safeguard is not exercised. |
| **FR-015** Configure and validate Jira project, fields, mappings, and issue types | No | No | No Jira configuration or validation exists; required values remain undecided. |
| **FR-016** Individually approve or reject each candidate | No | No | The UI describes individual approval, but has no candidate actions or decision recording. |
| **FR-017** Create at most one issue per explicitly approved candidate | No; write flow absent | Current safety holds only by absence | No Jira issue can be created by this build. There is no approval enforcement or duplicate-safe creation behavior to test. |
| **FR-018** Do not automatically update, close, assign, or delete existing Jira issues | Current guard only | Yes for the current build | No Jira integration or write route exists, so these changes cannot be initiated. Future integrations are unverified. |
| **FR-019** Show the Jira key and link after successful creation | No | No | Issue creation and result display are absent. |
| **FR-020** Separate successes, duplicates, rejections, and errors | No | No | No candidate outcomes or results workflow exists. |
| **FR-021** Retain failed drafts and support safe correction/retry | No | No | There are no server-side drafts, failure records, or retry flow. |
| **FR-022** Use the approving user's identity and least privilege; protect Jira credentials | Partial | Partial | No Jira credentials are present in the browser, but there is also no authentication, user identity, authorization, or Jira integration. The approved Atlassian auth method remains undecided. |
| **FR-023** Protect notes in transit/at rest and avoid sensitive logging | Partial | Partial | The preview does not send or persist notes. Production transport/storage protections and logging controls are not implemented or verifiable. |
| **FR-024** Do not send notes to an external extraction provider before approval | Current guard only | Yes for the current build | The submit handler only updates local UI state; no extraction provider or outbound processing request exists. Provider approval remains open. |
| **FR-025** Define retention and deletion before production | No | No | There is no application data lifecycle or retention/deletion policy. The database has no application schema or migrations. |
| **FR-026** Do not perform unspecified Confluence operations; require authorization for writes | Current guard only | Yes for the current build | Confluence is not configured and no Confluence operations exist. This satisfies the present no-unspecified-operation constraint, not a future workflow. |

## Success criteria

| Criterion | Implemented? | Does it work? | Evidence and remaining gap |
|---|---|---|---|
| **SC-001** Every input is processed or rejected clearly; invalid inputs are never reported as successful | Partial | Partial | The preview warns that processing is unavailable and notes were not sent. There is no processing or validation path to cover supported and invalid inputs. |
| **SC-002** Every proposed action includes a source excerpt | No | No | No proposals are generated. |
| **SC-003** Missing owners/due dates remain unset unless supplied during review | No | Not testable | No candidates or owner/due-date fields exist. |
| **SC-004** No Jira issue is created without approval for that candidate | Current guard only | Not exercised | No Jira creation route exists, so the build cannot create an issue. The approval safeguard is not implemented or tested. |
| **SC-005** Likely duplicates are not created and are reported with key, summary, and link | No | No | No duplicate search or Jira result UI exists. |
| **SC-006** Duplicate-search failures block creation | No | No | Duplicate search and creation are both absent. |
| **SC-007** Successful, rejected, duplicate, and failed outcomes are distinguishable | No | No | There are no outcome states or results view. |
| **SC-008** Ambiguous Jira create responses are checked before retry | No | No | Jira creation, idempotency, and retry handling are absent. |
| **SC-009** No Confluence operation occurs without an approved scenario and authorization | Current guard only | Yes for the current build | No Confluence client or operation exists. Future Confluence behavior remains untested and must be specified first. |

## User-story outcome

- **User Story 1 - Submit notes and review proposals:** Not met. A local text field exists, but notes are not processed, retained in a session, or turned into evidence-backed candidates. File upload is not enabled.
- **User Story 2 - Identify and review possible duplicates:** Not implemented. No Jira search or duplicate-review behavior exists.
- **User Story 3 - Approve, reject, and create issues individually:** Not implemented. No candidates, decisions, Jira writes, or creation results exist.

## Overall assessment

The current implementation is a working UI preview, a process-level API health endpoint, and a healthy local PostgreSQL container. It is not yet a working notes-to-Jira/Confluence application. Most functional requirements and success criteria cannot pass because the session, extraction, candidate review, duplicate, authorization, and Atlassian workflows are absent. Requirements marked **Current guard only** are safe only because those capabilities do not exist yet.
