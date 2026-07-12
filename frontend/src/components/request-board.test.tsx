import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { RequestBoard } from "./request-board";

const pendingRequest = {
  id: 1,
  title: "Increase worker concurrency",
  description: "Raise concurrency.",
  requester_id: 1,
  assigned_reviewer_id: 2,
  reviewer_team_id: 1,
  status: "pending",
  version: 1,
  decision_note: null,
  decided_by_id: null,
  created_at: "2026-01-01T00:00:00Z",
  decided_at: null,
};

describe("RequestBoard starter", () => {
  beforeEach(() => {
    vi.stubGlobal("crypto", { randomUUID: () => "test-command" });
    vi.stubGlobal("fetch", vi.fn(async (input: string | URL, init?: RequestInit) => {
      const path = String(input);
      if (path.endsWith("/session")) {
        return new Response(JSON.stringify({ id: 2, name: "Bob", team_id: 1, is_reviewer: true }));
      }
      if (path.endsWith("/requests") && !init?.method) {
        return new Response(JSON.stringify([pendingRequest]));
      }
      return new Response(JSON.stringify({ request: { ...pendingRequest, status: "approved", version: 2 } }));
    }));
  });

  it("loads requests and completes the starter happy path", async () => {
    render(<RequestBoard />);
    expect(
      await screen.findByRole("heading", { name: "Increase worker concurrency" }),
    ).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Approve" }));
    await waitFor(() => expect(screen.getByText("Request approved.")).toBeInTheDocument());
  });
});
