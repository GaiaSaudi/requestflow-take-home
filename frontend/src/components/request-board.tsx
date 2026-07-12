"use client";

import { SyntheticEvent, useEffect, useState } from "react";

import { decideRequest, getRequests, getSession } from "../lib/api";
import type { ChangeRequest, RequestStatus, User } from "../lib/types";

const sessions = [
  ["Alice Requester", "session-alice"],
  ["Bob Reviewer", "session-bob"],
  ["Carol Reviewer", "session-carol"],
  ["Dana Outsider", "session-dana"],
  ["Erin Dual Role", "session-erin"],
] as const;

export function RequestBoard() {
  const [token, setToken] = useState("session-bob");
  const [user, setUser] = useState<User | null>(null);
  const [requests, setRequests] = useState<ChangeRequest[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    let active = true;
    Promise.all([getSession(token), getRequests(token)])
      .then(([nextUser, nextRequests]) => {
        if (!active) return;
        setUser(nextUser);
        setRequests(nextRequests);
        setSelectedId(nextRequests[0]?.id ?? null);
        setMessage("");
      })
      .catch((error: Error) => active && setMessage(error.message));
    return () => {
      active = false;
    };
  }, [token]);

  const selected = requests.find((item) => item.id === selectedId) ?? null;

  async function submit(event: SyntheticEvent, decision: RequestStatus) {
    event.preventDefault();
    if (!selected || !user) return;
    setBusy(true);
    setMessage("");

    // This optimistic update and the browser-supplied actor are intentional starter defects.
    setRequests((current) =>
      current.map((item) => (item.id === selected.id ? { ...item, status: decision } : item)),
    );
    try {
      const result = await decideRequest(
        selected.id,
        user.id,
        decision,
        reason,
        selected.version,
        token,
      );
      setRequests((current) =>
        current.map((item) => (item.id === selected.id ? result.request : item)),
      );
      setMessage(`Request ${decision}.`);
      setReason("");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unexpected error");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main>
      <header>
        <div>
          <p className="eyebrow">Production change exercise</p>
          <h1>RequestFlow</h1>
        </div>
        <label>
          Simulated session
          <select value={token} onChange={(event) => setToken(event.target.value)}>
            {sessions.map(([name, value]) => (
              <option key={value} value={value}>{name}</option>
            ))}
          </select>
        </label>
      </header>

      <section className="workspace">
        <nav aria-label="Change requests">
          <h2>Requests</h2>
          {requests.map((item) => (
            <button
              className={item.id === selectedId ? "request selected" : "request"}
              key={item.id}
              onClick={() => setSelectedId(item.id)}
              type="button"
            >
              <span>{item.title}</span>
              <small>{item.status} · v{item.version}</small>
            </button>
          ))}
        </nav>

        <article>
          {selected ? (
            <>
              <p className={`status ${selected.status}`}>{selected.status}</p>
              <h2>{selected.title}</h2>
              <p>{selected.description}</p>
              <dl>
                <div><dt>Requester</dt><dd>User {selected.requester_id}</dd></div>
                <div><dt>Assigned reviewer</dt><dd>User {selected.assigned_reviewer_id ?? "—"}</dd></div>
                <div><dt>Version</dt><dd>{selected.version}</dd></div>
              </dl>
              {selected.status === "pending" && (
                <form onSubmit={(event) => submit(event, "approved")}>
                  <label>
                    Decision note / rejection reason
                    <textarea value={reason} onChange={(event) => setReason(event.target.value)} />
                  </label>
                  <div className="actions">
                    <button disabled={busy} type="submit">Approve</button>
                    <button
                      className="reject"
                      disabled={busy}
                      onClick={(event) => submit(event, "rejected")}
                      type="button"
                    >
                      Reject
                    </button>
                  </div>
                </form>
              )}
              {message && <p aria-live="polite" className="message">{message}</p>}
            </>
          ) : <p>No visible request selected.</p>}
        </article>
      </section>
    </main>
  );
}
