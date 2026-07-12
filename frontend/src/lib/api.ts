import type { ChangeRequest, DecisionResult, RequestStatus, User } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, token: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "X-Session-Token": token,
      ...init?.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(body.detail ?? `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const getSession = (token: string) => request<User>("/session", token);
export const getRequests = (token: string) => request<ChangeRequest[]>("/requests", token);

export function decideRequest(
  id: number,
  actorId: number,
  decision: RequestStatus,
  reason: string,
  version: number,
  token: string,
) {
  return request<DecisionResult>(`/requests/${id}/decision`, token, {
    method: "POST",
    body: JSON.stringify({
      actor_id: actorId,
      decision,
      reason: reason || null,
      idempotency_key: crypto.randomUUID(),
      expected_version: version,
    }),
  });
}
