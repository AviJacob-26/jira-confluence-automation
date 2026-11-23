# QA Report

**Date:** 2026-11-23 | **Application:** Stand-up to Jira
**Environment:** Local Docker Compose, backend, and Vite frontend; Chrome

## Summary

The application starts and the New session page renders. The notes form accepts input and submits, but processing is not implemented or connected: submission shows a preview notice and does not create proposals or send notes to an API. No unexpected browser console errors or warnings were observed.

## Pages Visited

- **New session** (`http://127.0.0.1:5173/`): visited and captured as a full-page screenshot during the session.
- **Review queue:** not a reachable page; displayed as disabled with a “SOON” label.
- **Review candidates** and **Results:** displayed as workflow step labels, not separate navigable pages.

## Elements Tested

- Notes textarea and character counter.
- **Process notes** button: disabled with an empty form; enabled after entering a 75-character sample note.
- Form submission and its inline status message.
- Action proposals empty state and counter.
- Navigation and connection statuses (Jira: not connected; Confluence: not configured).

## Results and Issues

- Docker Compose PostgreSQL started and became healthy on port 5432.
- Backend health endpoint at `http://127.0.0.1:3001/health` returned `{"status":"ok"}`.
- Frontend at `http://127.0.0.1:5173/` returned HTTP 200.
- Submitting `QA smoke test: confirm dashboard loading. No Jira action should be created.` displayed: “Processing is not connected yet. Your notes were not sent.”
- Action proposals remained at 0. No processing/API request was made; observed network traffic was for the page and its assets.
- Browser console: no JavaScript errors or warnings.

## Bugs Found

- **No unexpected runtime bugs observed.**
- **Known functional limitation:** processing is not connected, so the primary flow stops after form submission. The UI explicitly identifies itself as a preview and says processing is inactive; this is reported as an unavailable feature rather than an unexpected error.

## Fixes Applied

- None.

## Current Status

**Partial pass.** Startup, page rendering, form validation/enablement, submission feedback, and console checks passed. End-to-end note processing and Jira/Confluence integrations remain unavailable. This was a manual browser smoke test; no automated test suite was run.
