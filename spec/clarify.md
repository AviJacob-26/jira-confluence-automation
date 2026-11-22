# Senior Review: Specification Gaps and Clarifications

## Documents Reviewed

- [Project constitution](./constitution.md)
- [Feature specification](./specification.md)

## Review Summary

- No unambiguous, direct contradiction between the constitution and feature specification was found.
- The documents are still drafts and are **not ready for implementation planning** until the blocking questions below are resolved.
- The project is described as Jira/Confluence automation, while this feature specification defines only a meeting-notes-to-Jira workflow and explicitly prohibits Confluence reads and writes. This is a valid feature boundary, but the overall product scope needs confirmation.
- Several requirements specify desired outcomes without defining the decision rules, lifecycle, or measurable quality thresholds needed to implement and verify them.

## Scope Tensions and Internal Ambiguities

1. **Jira/Confluence project versus Jira-only feature**  
   FR-026 excludes all Confluence reads and writes, while the project is described as a Jira/Confluence automation project. This is not a direct contradiction because the specification is feature-scoped, but it is unclear whether Confluence is a later feature or whether this specification was intended to cover the full product.

2. **Likely duplicate versus uncertain possible match**  
   FR-012 requires likely duplicates to be skipped, while User Story 2 says an uncertain possible match is surfaced for review. FR-013 leaves the match threshold and uncertain-match resolution open. The specification does not say whether a user may dismiss a possible match and approve creation, whether it remains blocked, or whether the only outcome is skip-and-report.

3. **Retain failed drafts versus undefined retention**  
   FR-021 requires retaining a draft after creation failure, while FR-025 leaves retention and deletion behavior undecided. The minimum retention needed to correct and retry a failed draft, and when that draft is eventually deleted, are unspecified.

4. **Authorization boundary for external operations**  
   The constitution requires explicit authorization for every Jira or Confluence data change; the feature specification clearly requires per-candidate approval for Jira creation. It does not define whether approval is bound to an exact final draft, how edits invalidate prior approval, or how authorization is recorded. These details matter to enforce the principle consistently.

## Gaps Requiring Decisions

### Blocking Before Planning or Implementation

| ID | Area | Gap / unclear requirement | Decision needed |
|---|---|---|---|
| G-01 | Product scope | Confluence behavior is not specified; the feature explicitly forbids it. | Confirm this feature is Jira-only and whether Confluence will have a separate feature specification. |
| G-02 | Users and authorization | “Authorized internal users” and “approving user's authorized Jira identity” do not define the identity provider, roles, or who may submit, review, approve, or configure the integration. | Define the user roles, access boundaries, identity provider, Jira authorization model, and whether anyone besides the project manager may use the app. |
| G-03 | Input formats | File upload is required, but formats, size limits, languages, and handling of multiple files are open. | Define accepted formats, maximum size, language support, and whether one session may contain multiple files or text-plus-file input. |
| G-04 | Input/session behavior | The session's start, completion, cancellation, resumption, and empty-result behavior are not defined. | Define what the user sees when no actions are found, processing is partial, or a session is interrupted; specify whether sessions can be resumed. |
| G-05 | Extraction behavior | The extraction provider is undecided. The spec does not define how malformed output, missing evidence, conflicting statements, or low-confidence action candidates are handled. | Select an approved provider or local approach; define output validation, uncertainty handling, and behavior when the extractor cannot support a candidate with evidence. |
| G-06 | Extraction quality | “Explicit or clearly committed” is central but subjective. The verification section mentions measuring missed actions and unsupported proposals without defining datasets, thresholds, or rollout criteria. | Define an evaluation set and acceptable missed-action, unsupported-action, and evidence-quality thresholds before release. |
| G-07 | Jira configuration | Project key, required fields, mappings, and issue-type availability are unresolved; there is no defined configuration owner or validation flow. | Define required configuration, who supplies it, how it is validated, and which errors prevent creation. |
| G-08 | Draft fields and mappings | The candidate includes summary, description, issue type, optional owner, and due date, but the editable fields and mapping/validation rules are unspecified. Priority, components, labels, and other required Jira fields are open. | Define which fields users can edit, supported values, field-specific validation, and whether additional Jira fields are in scope. |
| G-09 | Issue-type selection | The spec lists `Story`, `Task`, `Bug`, and `Spike` but does not define how the system chooses among them or what happens when the type is unclear. | Define selection rules and whether an uncertain type must be left unset for user choice. |
| G-10 | Duplicate matching | Matching signals, threshold, scope of Jira search, and treatment of issue statuses/types are not defined. | Define the search scope and matching criteria, including whether closed/resolved issues count and how threshold behavior is tested. |
| G-11 | Duplicate review outcome | An uncertain match is surfaced, but its effect on approval and creation is unspecified. The data model has no explicit duplicate-resolution decision. | Decide whether users may dismiss a possible match, whether it remains blocked, and what decision/audit data must be recorded. Preserve the explicit rule that confirmed likely duplicates are not created or automatically linked. |
| G-12 | Persistence and retention | The constitution fixes PostgreSQL 15 as the database, but the feature specification does not say which session data is persisted, whether it survives sign-out/restart, or when records are deleted. | Define session persistence, access isolation, minimum retry retention, deletion behavior, and whether source files are stored or only extracted text/references. |
| G-13 | Jira authentication | Use of the approving user's identity is required, but the authentication method and token lifecycle are not selected. | Confirm the approved Jira Cloud auth flow, credential/token storage, revocation, and reauthorization behavior. |
| G-14 | Creation retries and idempotency | “No more than one issue” and “verify before retry” are stated, but the mechanism for detecting an already-created issue after a timeout is not. | Define the idempotency/deduplication strategy, handling of concurrent approvals, and safe retry behavior for definite versus ambiguous failures. |

### Important Before Production

| ID | Area | Gap / unclear requirement | Decision needed |
|---|---|---|---|
| G-15 | Candidate lifecycle | Candidate states and allowed transitions are not defined. It is unclear how a candidate moves among extraction failure, possible duplicate, ready for review, approved, rejected, creating, created, or failed. | Define states, transitions, terminal states, and whether decisions can be changed or reopened. |
| G-16 | Approval semantics | The specification does not say whether editing after approval invalidates approval, whether approval expires, or whether a user can approve their own submission. | Define what exact content an approval covers, who may approve, and whether reapproval is required after edits. |
| G-17 | Error UX and recovery | Errors must be distinct, but user-facing error categories, retry controls, and recoverable versus terminal failures are unspecified. | Define expected recovery for extraction, Jira search, field validation, authentication, and issue-creation failures. |
| G-18 | Auditability | Review Decision records only status and time; the approver, approved draft snapshot, and external request/result correlation are not specified. | Define the minimum audit trail needed to explain who approved which content and what external action followed, without logging sensitive notes unnecessarily. |
| G-19 | Privacy and security detail | The constitution requires protection in transit/at rest and least privilege, but does not define access isolation, retention enforcement, file-upload safeguards, session protection, or logging redaction requirements. | Define concrete security requirements and verification criteria during planning, consistent with organizational policy. |
| G-20 | Success metrics | Most success criteria are behavioral assertions. There are no targets for extraction accuracy, duplicate precision/recall, processing time, usability, availability, or supported load. | Decide which quantitative targets are required for acceptance and rollout; do not invent targets without product approval. |
| G-21 | User/team mapping | The 14-person team is noted, but the roster, Jira account mapping, and whether owner suggestions are allowed are unresolved. | Confirm whether owner assignment/suggestion is in scope and how identities map to Jira accounts. |
| G-22 | Operational constraints | Hosting, data residency, supported browsers, backups/recovery, and deployment configuration are not defined. | Record deployment and operational constraints in the plan before production readiness decisions. |
| G-23 | Governance metadata | The constitution is marked “Draft for review,” the feature is “Draft,” and the feature branch is `not-assigned`. | Confirm who approves these documents and assign a feature branch when implementation begins. |

## Clarification Questions to Resolve

1. Is this specification intentionally limited to the stand-up-notes-to-Jira feature, with Confluence covered separately?
2. Which users may access the app, submit notes, review candidates, approve issues, and configure integrations? What identity provider and Jira auth method are approved?
3. Which file formats, maximum file size, languages, and combinations of text/files must be supported?
4. What should happen when a session has no candidates, partial extraction results, an interrupted request, or an extraction failure?
5. Which extraction provider or local approach is approved, and what accuracy/evaluation thresholds must it meet before rollout?
6. What Jira project key, required fields, field mappings, allowed values, and issue-type availability apply?
7. Which fields are editable, and how should the system choose an issue type when notes do not make it clear?
8. What Jira search scope and duplicate signals define a likely duplicate? Do resolved/closed issues count?
9. For an uncertain possible duplicate, can the reviewer dismiss the match and approve creation, or must the candidate stay blocked or be skipped?
10. Which candidate/session states and transitions are required, and can a rejected or failed candidate be reopened?
11. Does editing a draft after approval require a new approval? Can the submitter approve their own candidate?
12. How long must notes and failed drafts remain available for review/retry, and when/how must they be deleted?
13. How will the system prevent duplicate issue creation after concurrent approvals or ambiguous Jira timeouts?
14. What audit information must be retained for decisions and Jira operations?
15. What measurable targets are required for action extraction, duplicate detection, response time, and operational readiness?
16. What hosting, data-residency, browser, backup, and recovery constraints apply?

## Readiness

Resolve the blocking items before generating implementation tasks. The constitution and feature specification can then be updated, followed by a consistency review of the revised requirements and acceptance scenarios.
