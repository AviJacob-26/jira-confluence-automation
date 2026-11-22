# Jira Cloud Configuration

## Project

- Jira site: Unable to verify; no Jira Cloud site URL was provided.
- Project name: Unable to verify.
- Project key: Unable to verify.
- Access/verification status: Blocked; no Jira credentials or read-only metadata export were provided.
- Evidence source: `work/module03-task/backlog.md`
- Verification date: `2026-11-22`

## Required Fields

- Unable to verify project access or create-screen configuration.
- `Story`, `Task`, `Bug`, and `Spike`: required fields unavailable.
- Summary, description, issue type, priority, components, and labels: no field IDs or requirement status verified.
- Owner and due date: mapping remains unset until explicitly approved.

## Supported Issue Types

- Story: Unable to verify.
- Task: Unable to verify.
- Bug: Unable to verify.
- Spike: Unable to verify.

## Available Values

- Priorities: Unable to verify.
- Components: Unable to verify.
- Labels: Unable to verify.
- Evidence source: no Jira API metadata or approved configuration export was provided.

## Issue-Type Mappings

- Story: `blocked` — Jira issue-type ID/name unavailable.
- Task: `blocked` — Jira issue-type ID/name unavailable.
- Bug: `blocked` — Jira issue-type ID/name unavailable.
- Spike: `blocked` — Jira issue-type ID/name unavailable.

## Blocking Decisions

- Confirm the Jira Cloud site URL.
- Confirm the first-release Jira project key.
- Provide authorized read-only Jira access or an approved configuration export.
- Verify the project create screens and required fields.
- Verify project support for `Story`, `Task`, `Bug`, and `Spike`.
- Verify available priorities, components, and labels.
- Approve explicit mappings and optional owner/due-date behavior.

## Release Gate

- State: `blocked`
- Jira issue creation must remain disabled until the blocking decisions above are resolved.
