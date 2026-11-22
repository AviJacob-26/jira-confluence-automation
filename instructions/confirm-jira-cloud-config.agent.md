- **Input format**
  + Accept a Jira Cloud site URL or configured Jira base URL.
  + Accept the intended first-release project key or name.
  + Accept authentication details only when they are necessary to query Jira; never request passwords, API tokens, or other secrets in chat or instruction files.
  + Accept Jira API metadata or an approved administrator/exported configuration report when direct Jira access is unavailable.
  + Accept these mappings only as proposed values: `Story`, `Task`, `Bug`, and `Spike`.

- **Processing steps**
  + Identify the Jira Cloud site and confirm access to the intended project.
  + Resolve the project key and confirm project access, status, and whether the project is suitable for first-release issue creation.
  + Retrieve or validate the project issue types and mark each of `Story`, `Task`, `Bug`, and `Spike` as supported or unsupported.
  + Retrieve the create-screen configuration and list required fields for each supported issue type.
  + Identify field IDs and names for summary, description, issue type, priority, components, labels, owner, and due date.
  + Retrieve available priorities, components, and labels; record exact IDs/names or state that each value is unavailable.
  + Confirm whether components and labels are project-level or unrestricted; do not infer project ownership for either.
  + Map each supported draft issue type to the exact Jira issue-type ID/name.
  + Define the mapping result for each type as `configured`, `unsupported`, or `blocked` by missing required-field information.
  + Mark required fields that are not mapped as blocking decisions.
  + Mark optional owner and due date mappings as unset unless the Jira project and team explicitly approve and configure them.
  + Reject any configuration that does not support all four mappings unless the project owner explicitly approves a first-release subset.
  + Verify whether priority is required, optional, or unavailable for each issue type; do not invent a default.
  + Surface uncertain or conflicting values for human confirmation instead of selecting them silently.
  + Add a configuration check for startup or integration validation before Jira creation is enabled.

- **Output format**
  + Return a concise Markdown configuration record with these sections in order: `## Project`, `## Required Fields`, `## Supported Issue Types`, `## Available Values`, `## Issue-Type Mappings`, `## Blocking Decisions`, `## Release Gate`.
  + In `## Project`, report the site, project name, project key, and access/verification status.
  + In `## Required Fields`, report each field by issue type with field ID, field name, requirement, and whether it is mapped.
  + In `## Supported Issue Types`, list `Story`, `Task`, `Bug`, and `Spike` as supported, unsupported, or unable to verify.
  + In `## Available Values`, list exact priority names/IDs, component names/IDs, and label names/IDs discovered for the project.
  + In `## Issue-Type Mappings`, provide one row or bullet per type with source value, Jira issue-type ID/name, status, and required-field status.
  + In `## Blocking Decisions`, list every unresolved project key, field, issue-type, value, or approval decision that prevents implementation.
  + In `## Release Gate`, state `enabled` only after every required field and supported mapping is verified; otherwise state `blocked`.
  + Preserve Jira IDs and names exactly when provided.
  + Include evidence source and verification date for each externally discovered configuration value.
  + Include no more than one `enabled` release gate if all blocking decisions are resolved.

- **Constraints**
  + Do not guess the project key or Jira configuration values.
  + Do not expose credentials or secret values in output.
  + Do not approve a project configuration if required fields or supported issue types cannot be verified.
  + Do not infer assignees or owners without an explicit team decision.
  + Do not use unsupported issue types or create an issue while configuration is blocked.
  + Do not silently substitute a priority, component, or label for a missing required value.
  + Do not treat an API error or unavailable metadata as a confirmed no-match or empty configuration.
  + Keep the first-release configuration minimal; add mappings or values only after they are approved.
  + Use exact Jira terminology and IDs; distinguish project configuration from application defaults.
