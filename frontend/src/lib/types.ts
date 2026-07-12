export type RequestStatus = "pending" | "approved" | "rejected";

export interface User {
  id: number;
  name: string;
  team_id: number;
  is_reviewer: boolean;
}

export interface ChangeRequest {
  id: number;
  title: string;
  description: string;
  requester_id: number;
  assigned_reviewer_id: number | null;
  reviewer_team_id: number;
  status: RequestStatus;
  version: number;
  decision_note: string | null;
  decided_by_id: number | null;
  created_at: string;
  decided_at: string | null;
}

export interface DecisionResult {
  request: ChangeRequest;
}
