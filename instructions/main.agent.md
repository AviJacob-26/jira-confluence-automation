# Instructions Catalog

Each entry below is an instruction file with a one-line description. Optional sub-fields after `+`:
- **Keywords** — trigger words/phrases: if the user's request matches, load this instruction.
- **Target** — file glob pattern: if the current file or context matches, consider this instruction relevant.
- **Exceptions** — edge cases or clarifications that don't fit in the one-liner.

---

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — create or update instructions and configure instruction infrastructure.
  + Keywords: creating instructions, create instruction, update instruction, add instruction, set up instructions, shortcut, wrapper, catalog
  + Target: `instructions/**/*.md`, `.github/**/*.md`, `.vscode/**/*.json`, `AGENTS.md`

- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — generate a concise weekly status report.
  + Keywords: weekly status report, status report, accomplishments, blockers, next week
  + Target: `*.md`, `reports/**/*.md`, `work/**/*.md`

- [`./instructions/format-status-report.agent.md`](./format-status-report.agent.md) — format a weekly status report's Markdown structure and length.
  + Keywords: format weekly status report, status report structure
  + Exceptions: follow the complete create-status-report instruction when generating a report.

- [`./instructions/write-status-report-content.agent.md`](./write-status-report-content.agent.md) — write concrete, concise weekly status report content.
  + Keywords: write status report content, status report tone
  + Exceptions: follow the complete create-status-report instruction when generating a report.

- [`./instructions/confirm-jira-cloud-config.agent.md`](./confirm-jira-cloud-config.agent.md) — confirm Jira Cloud project, field, issue-type, and value mappings for first-release issue creation.
  + Keywords: Jira Cloud, Jira project key, required fields, issue types, Story, Task, Bug, Spike, priorities, components, labels, field mappings
  + Target: `backlog.md`, `**/*jira*`, `instructions/**/*.md`

- [`./instructions/run-project-validation.agent.md`](./run-project-validation.agent.md) — run project lint, build/type checks, and test suites; triage and fix introduced failures.
  + Keywords: lint, type check, build, unit tests, integration tests, end-to-end tests, test suite, validation, resolve failures
  + Target: `package.json`, `pyproject.toml`, `Makefile`, `**/*test*`, `.github/workflows/**`
