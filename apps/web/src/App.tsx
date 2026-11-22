import { useState, type FormEvent } from "react";

const steps = ["Add notes", "Review candidates", "Results"];

function App() {
  const [notes, setNotes] = useState("");
  const [notice, setNotice] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice("Processing is not connected yet. Your notes were not sent.");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#new-session" aria-label="Stand-up to Jira home">
          <span className="brand-mark" aria-hidden="true">J</span>
          <span>
            <strong>Stand-up to Jira</strong>
            <small>Automation workspace</small>
          </span>
        </a>

        <div className="nav-caption">WORKSPACE</div>
        <nav aria-label="Workspace">
          <a className="nav-item active" href="#new-session" aria-current="page">
            <span className="nav-icon note-icon" aria-hidden="true" />
            New session
          </a>
          <span className="nav-item disabled" aria-disabled="true">
            <span className="nav-icon history-icon" aria-hidden="true" />
            Review queue
            <span className="soon-label">SOON</span>
          </span>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-rule" />
          <div className="connection-label">CONNECTIONS</div>
          <div className="connection-row">
            <span className="connection-dot" />
            <span>Jira</span>
            <span className="connection-state">Not connected</span>
          </div>
          <div className="connection-row">
            <span className="connection-dot muted" />
            <span>Confluence</span>
            <span className="connection-state">Not configured</span>
          </div>
          <div className="sidebar-note">
            <span className="shield-mark" aria-hidden="true">i</span>
            <span>Every Jira issue requires your individual approval.</span>
          </div>
        </div>
      </aside>

      <main className="workspace" id="new-session">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Workspace</span>
            <span className="breadcrumb-divider">/</span>
            <strong>New session</strong>
          </div>
          <div className="preview-chip">
            <span className="preview-dot" />
            UI PREVIEW
          </div>
        </header>

        <div className="page-content">
          <section className="page-heading">
            <div>
              <p className="eyebrow">MEETING NOTES WORKFLOW</p>
              <h1>Turn stand-up notes into clear next steps.</h1>
              <p className="heading-copy">
                Review evidence-backed action proposals before anything reaches Jira.
              </p>
            </div>
            <div className="draft-badge">
              <span className="draft-dot" />
              New draft
            </div>
          </section>

          <section className="stepper" aria-label="Workflow progress">
            {steps.map((step, index) => (
              <div
                className={`step ${index === 0 ? "current" : ""}`}
                key={step}
                aria-current={index === 0 ? "step" : undefined}
              >
                <span className="step-number">{`0${index + 1}`}</span>
                <span>{step}</span>
                {index < steps.length - 1 && <span className="step-line" />}
              </div>
            ))}
          </section>

          <div className="content-grid">
            <section className="notes-card" aria-labelledby="notes-title">
              <div className="card-heading">
                <div>
                  <p className="section-kicker">STEP 01</p>
                  <h2 id="notes-title">Add your stand-up notes</h2>
                </div>
                <span className="required-label">TEXT ENTRY</span>
              </div>
              <p className="card-description">
                Paste the notes from your production-support stand-up. Proposed actions
                should stay grounded in what was actually agreed.
              </p>

              <form onSubmit={handleSubmit}>
                <label className="visually-hidden" htmlFor="meeting-notes">
                  Stand-up notes
                </label>
                <textarea
                  id="meeting-notes"
                  value={notes}
                  onChange={(event) => {
                    setNotes(event.target.value);
                    setNotice("");
                  }}
                  placeholder="Paste stand-up notes here..."
                  rows={9}
                />
                <div className="input-meta">
                  <span>{notes.length} characters</span>
                  <span>Source notes are shown during review</span>
                </div>

                <div className="upload-notice">
                  <span className="upload-mark" aria-hidden="true">+</span>
                  <span>
                    <strong>File upload is not enabled yet</strong>
                    <small>Supported formats and size limits still need confirmation.</small>
                  </span>
                </div>

                {notice && (
                  <div className="inline-notice" role="status">
                    <span className="notice-mark" aria-hidden="true">i</span>
                    {notice}
                  </div>
                )}

                <div className="form-footer">
                  <p>
                    <span className="lock-mark" aria-hidden="true" />
                    Preview only. Notes are not sent or stored.
                  </p>
                  <button className="primary-button" type="submit" disabled={!notes.trim()}>
                    Process notes
                    <span aria-hidden="true">-&gt;</span>
                  </button>
                </div>
              </form>
            </section>

            <aside className="guidance-column">
              <section className="guidance-card">
                <div className="guidance-icon" aria-hidden="true">
                  <span />
                </div>
                <p className="section-kicker">BUILT FOR REVIEW</p>
                <h2>You stay in control.</h2>
                <p className="guidance-copy">
                  Automation prepares drafts. You decide what, if anything, becomes a Jira
                  issue.
                </p>
                <ul className="safeguard-list">
                  <li>
                    <span className="check-mark" aria-hidden="true">✓</span>
                    Each proposal includes its source excerpt
                  </li>
                  <li>
                    <span className="check-mark" aria-hidden="true">✓</span>
                    Possible duplicates are surfaced first
                  </li>
                  <li>
                    <span className="check-mark" aria-hidden="true">✓</span>
                    Every issue is approved individually
                  </li>
                </ul>
              </section>

              <section className="empty-review-card">
                <div className="empty-review-top">
                  <span className="empty-icon" aria-hidden="true">
                    <span />
                    <span />
                    <span />
                  </span>
                  <span className="empty-count">0</span>
                </div>
                <h3>Action proposals</h3>
                <p>
                  Your reviewed candidates will appear here after notes are processed.
                </p>
                <span className="empty-state-label">WAITING FOR NOTES</span>
              </section>
            </aside>
          </div>

          <footer className="page-footer">
            <span>Preview build</span>
            <span className="footer-separator">|</span>
            <span>Processing and Atlassian connections are not active.</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
