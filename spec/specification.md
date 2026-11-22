# Feature Specification: Stand-up Notes to Jira and Confluence Automation

**Feature Branch**: `not-assigned`

**Created**: 2026-11-22

**Status**: Draft

**Input**: User description: "Build an internal web application for the project manager to submit production-support stand-up notes, review evidence-backed action proposals, avoid likely Jira duplicates, create only individually approved Jira issues, and support defined Confluence automation workflows."

## Users and Permissions

- **Only application user for the initial release**: The project manager overseeing the 14-person production-support team. No other application user role is in scope.
- The project manager submits notes, reviews and edits candidates, and approves or rejects each Jira candidate individually.
- The identity provider and application sign-in method are **[NEEDS CLARIFICATION: authentication method is undecided]**.
- Atlassian access must follow the project constitution's least-privilege and explicit-authorization principles. The Jira/Confluence authentication method and permissions are **[NEEDS CLARIFICATION: approved Atlassian authorization approach is undecided]**.

## Confluence Scope

Confluence automation is in scope for this feature, as confirmed by the user. The specific user workflows and operations have not yet been defined. This specification does not assume whether the application will search, read, create, or update Confluence content, or which spaces and pages it may access. Each operation must be specified and reviewed before implementation; no unspecified Confluence operation may be performed.

## User Scenarios & Testing

### User Story 1 - Submit notes and review proposed actions (Priority: P1)

The project manager submits stand-up notes and reviews proposed actions with evidence from the source notes before any Jira issue is created.

**Why this priority**: Reliable extraction and review are the foundation of the workflow. The project manager must be able to verify that each proposal reflects an actual commitment rather than speculation.

**Independent Test**: Submit representative notes containing a clearly committed action, an uncommitted suggestion, and an action with no stated owner or due date. Verify that only the committed action is proposed, its evidence is shown, and missing values remain unset.

**Acceptance Scenarios**:

1. **Given** an authorized user starts a processing session, **When** they submit notes through the text-entry path, **Then** the system preserves the source notes for the duration of that session and begins processing them.
2. **Given** the user submits a file in a supported format, **When** the file is readable, **Then** the system processes its contents and retains the source material for review during the session.
3. **Given** the notes contain both committed actions and speculation, **When** the system proposes candidates, **Then** each candidate represents an explicit or clearly committed action and includes a supporting excerpt; speculative ideas and general discussion are not proposed as work.
4. **Given** a candidate has no clearly stated owner or due date, **When** it is displayed, **Then** those fields remain unset and are identified as missing or uncertain rather than inferred.
5. **Given** an input is unsupported, unreadable, or invalid, **When** processing is attempted, **Then** the user receives a clear error and the system does not report successful processing.

### User Story 2 - Identify and review possible duplicates (Priority: P2)

Before a proposal is offered for approval, the system searches the configured Jira project for likely matching issues and explains any possible duplicate.

**Why this priority**: Avoiding duplicate or low-value Jira issues is a core project goal and must be enforced before issue creation.

**Independent Test**: Use a Jira test project containing a matching issue, a non-matching issue, and a case that falls near the configured matching threshold. Verify that likely duplicates are skipped and reported, non-duplicates proceed to review, and uncertain matches are surfaced rather than silently ignored.

**Acceptance Scenarios**:

1. **Given** a candidate has a likely matching Jira issue, **When** duplicate screening completes, **Then** the candidate is skipped from creation and the user sees the matching issue key, summary, and link.
2. **Given** no likely duplicate is found, **When** screening completes, **Then** the candidate is presented for user review.
3. **Given** a possible match is uncertain, **When** screening completes, **Then** the possible match is surfaced for review and the system does not silently proceed as though no match exists.
4. **Given** Jira duplicate search fails, **When** the system evaluates a candidate, **Then** creation is blocked and the search failure is reported distinctly.

### User Story 3 - Approve, reject, and create issues individually (Priority: P3)

The project manager edits each non-duplicate draft, approves or rejects it independently, and receives a clear result for each decision.

**Why this priority**: Explicit, per-issue human approval is required to prevent unwanted external changes and keep control with the project manager.

**Independent Test**: Review multiple non-duplicate drafts, edit one, approve one, and reject another. Verify that only the approved candidate is created, the rejected candidate is not created, and every result is accurately reported.

**Acceptance Scenarios**:

1. **Given** a non-duplicate candidate is ready for review, **When** the project manager edits its draft, **Then** the edits are retained for that candidate before the approval decision.
2. **Given** multiple candidates are awaiting review, **When** the project manager approves one candidate, **Then** approval applies only to that candidate and does not approve any other candidate.
3. **Given** a candidate is rejected, **When** the decision is recorded, **Then** no Jira issue is created for that candidate and the rejection is reported separately from successful creations.
4. **Given** a candidate is approved and passes validation, **When** creation succeeds, **Then** the system displays the Jira issue key and a link to the issue.
5. **Given** Jira creation fails, **When** the result is returned, **Then** the draft is retained, the failure is reported clearly, and the result is not shown as a success.
6. **Given** a creation request returns an ambiguous result, **When** a retry is considered, **Then** the system verifies whether the original creation succeeded before retrying.

## Edge Cases

- The notes contain no explicit or clearly committed actions.
- Notes contain ambiguous statements, conflicting commitments, or incomplete context.
- A file is empty, corrupted, unreadable, oversized, or in an unsupported format. Supported formats and size limits are open decisions.
- The extraction service fails, returns malformed data, or omits evidence for a proposed action.
- Owner or due-date language is ambiguous or conflicts with another statement.
- Jira authentication expires, the configured project is unavailable, or required fields are missing.
- Jira search returns an error or an uncertain possible duplicate.
- Jira creation times out after the request may have reached Jira.
- The same candidate is submitted for creation more than once.
- A user attempts to approve a candidate without the required authorization.
- A request involves a Confluence operation that is not specified and approved; the system does not perform that operation.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST restrict the initial application to the project manager. No other application user role is in scope for the initial release. The identity provider and sign-in method are **[NEEDS CLARIFICATION: authentication method is undecided]**.
- **FR-002**: The system MUST allow a user to provide meeting notes through text entry and file upload.
- **FR-003**: The supported upload formats, maximum file size, and supported languages MUST be confirmed before file processing is enabled **[NEEDS CLARIFICATION: formats, size limits, and languages are unspecified]**.
- **FR-004**: The system MUST preserve the source notes, or a protected reference to them, for the duration of the processing session so the user can verify proposed actions.
- **FR-005**: The system MUST reject unsupported, invalid, or unreadable inputs with a clear error and MUST NOT present them as successfully processed.
- **FR-006**: The system MUST propose only actions that are explicit or clearly committed to in the source notes. It MUST NOT turn speculation, uncommitted suggestions, or general discussion into action candidates.
- **FR-007**: Each candidate MUST include a concise proposed action, a summary, a draft description, a supporting excerpt from the source notes, and a proposed issue type.
- **FR-008**: Proposed Jira issue types MUST be limited to `Story`, `Task`, `Bug`, and `Spike`.
- **FR-009**: The system MUST populate an owner or due date only when that value is clearly stated in the notes. Otherwise, the field MUST remain unset and be identified for review.
- **FR-010**: The system MUST identify missing or uncertain candidate fields and allow the project manager to edit each draft before deciding.
- **FR-011**: Before a candidate is presented for approval, the system MUST search the configured Jira project for likely duplicates.
- **FR-012**: A likely duplicate MUST be skipped from creation and reported with the matching Jira issue key, summary, and link. The system MUST NOT create or automatically link that duplicate.
- **FR-013**: Duplicate matching signals, confidence threshold, and the resolution behavior for uncertain matches MUST be defined before implementation **[NEEDS CLARIFICATION: matching rules and uncertain-match handling are unspecified]**.
- **FR-014**: If Jira duplicate search fails, the system MUST block issue creation for the affected candidate and report the failure.
- **FR-015**: The Jira project key, required fields, field mappings, and availability of supported issue types MUST be configured and validated before creation is enabled **[NEEDS CLARIFICATION: Jira project and field configuration are unspecified]**.
- **FR-016**: The system MUST allow the project manager to approve or reject each candidate independently. Batch approval and unattended creation are out of scope for the initial release.
- **FR-017**: The system MUST create no more than one Jira issue for a single approved candidate and MUST NOT create an issue without that candidate's explicit approval.
- **FR-018**: The initial release MUST NOT automatically update, close, assign, or delete existing Jira issues.
- **FR-019**: After successful creation, the system MUST display the Jira issue key and link.
- **FR-020**: The system MUST report successful creations, skipped duplicates, rejected drafts, and errors separately. A failure MUST NOT appear as a success.
- **FR-021**: On a creation failure, the system MUST retain the draft and provide enough error information for the user to correct or retry it without creating an unverified duplicate.
- **FR-022**: The system MUST use the approving user's authorized Jira identity, MUST apply least-privilege access, and MUST NOT expose Jira credentials to the browser or store them in plaintext. The authentication method is a deployment decision **[NEEDS CLARIFICATION: approved Jira Cloud authentication method is unspecified]**.
- **FR-023**: The system MUST protect meeting notes and extracted content in transit and at rest, and MUST avoid logging full notes, credentials, or unnecessary personal data.
- **FR-024**: The system MUST NOT send notes to an external extraction provider until the provider, data-handling terms, and organizational approval are confirmed **[NEEDS CLARIFICATION: extraction provider and approval are unspecified]**.
- **FR-025**: Retention and deletion behavior for notes, drafts, decisions, duplicate matches, and results MUST be defined before production use **[NEEDS CLARIFICATION: persistence duration and deletion policy are unspecified]**.
- **FR-026**: Confluence automation is in scope, but no specific Confluence operation is approved by the current requirements. The system MUST NOT perform a Confluence operation until its user goal, content/space scope, authorization, behavior, failure handling, and acceptance criteria are added to this specification and reviewed. Any operation that creates or changes Confluence content MUST require explicit authorization from the authenticated user **[NEEDS CLARIFICATION: Confluence workflows and operation scope are not defined]**.

### Key Entities

- **Processing Session**: A user's processing attempt, including its identifier, creation time, processing status, user identity, and source notes or a protected reference to them.
- **Action Candidate**: A proposed action linked to its session, with evidence excerpt, draft summary and description, issue type, optional owner and due date, review status, and duplicate-check status.
- **Duplicate Match**: A possible matching Jira issue associated with a candidate, including its issue key, summary, link, and match assessment.
- **Review Decision**: The project manager's edit, approval, or rejection of an individual candidate, including the decision status and time.
- **Creation Result**: The outcome for a candidate, including status, Jira issue key and URL when successful, or an error description when unsuccessful.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every submitted input is either processed or rejected with a clear error; no invalid or unreadable input is reported as successfully processed.
- **SC-002**: Every proposed action candidate includes a source-note excerpt that allows the project manager to verify its origin.
- **SC-003**: In evaluation cases where notes omit an owner or due date, the corresponding values remain unset unless the project manager supplies them during review.
- **SC-004**: In all tested workflows, no Jira issue is created without explicit approval for that specific candidate.
- **SC-005**: In all tested likely-duplicate cases, the candidate is not created and the user receives the matching issue key, summary, and link.
- **SC-006**: In all tested Jira duplicate-search failure cases, no issue is created for the affected candidate.
- **SC-007**: Each successful creation displays its Jira key and link, while rejected candidates, skipped duplicates, and failures are distinguishable from successes.
- **SC-008**: In retry tests with an ambiguous Jira response, the system checks the original operation's state before issuing another create request.
- **SC-009**: No Confluence operation is performed unless that operation has an approved user scenario, authorization rule, and acceptance criteria in this specification.

## Assumptions

- The initial release is an internal web application primarily used by a project manager overseeing a 14-person production-support team.
- The project manager is the only application user in the initial release.
- The initial workflow processes daily stand-up notes and targets Jira Cloud.
- Confluence automation is in scope, but the supported operations and content boundaries remain undecided and must be specified before implementation.
- Text entry and file upload are the initial input methods; exact upload formats remain unconfirmed.
- Candidate extraction, duplicate screening, draft editing, and per-candidate review occur before Jira issue creation.
- The configured Jira project supports some or all of the four issue types, subject to validation before creation is enabled.
- Meeting-platform integrations and automatic Jira updates are outside the initial release.

## Open Questions

- Which file formats, maximum input size, and languages must be supported?
- What Jira project key, required fields, issue-type-specific mappings, priorities, components, and labels are required?
- How should issue type be chosen when the notes do not make it clear?
- Which duplicate signals and confidence threshold define a likely duplicate, and how should uncertain matches be resolved?
- Which identity provider and Jira Cloud authentication method are approved, and will anyone besides the project manager use the application?
- What team roster and Jira account mapping, if any, should be available for owner suggestions?
- What session persistence, retention, and deletion rules apply?
- Which extraction provider, if any, is approved, and what data-handling terms apply?
- Which Confluence operations are required, which spaces/pages may they access, and what authorization, approval, validation, and error behavior applies?
- What hosting environment and data-residency constraints apply?
