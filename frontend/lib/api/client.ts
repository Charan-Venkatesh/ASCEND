import type { ApiEnvelope, AuthResponse, DashboardSnapshot, Mission } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

function token() {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem("ascend_token") ?? "";
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: token() ? `Bearer ${token()}` : "",
      ...(init?.headers ?? {})
    }
  });
  const envelope = (await response.json()) as ApiEnvelope<T>;
  if (!response.ok || envelope.errors.length) {
    throw new Error(envelope.errors[0]?.message ?? "ASCEND API request failed");
  }
  return envelope.data;
}

export const api = {
  login: (email: string, password: string) => request<AuthResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  register: (email: string, password: string, display_name: string) => request<AuthResponse>("/auth/register", { method: "POST", body: JSON.stringify({ email, password, display_name }) }),
  dashboard: () => request<DashboardSnapshot>("/dashboard/today"),
  generateRoadmap: () => request("/roadmaps/generate", { method: "POST", body: JSON.stringify({}) }),
  mission: (id: string) => request<Mission>(`/missions/${id}`),
  todayMission: () => request<Mission | null>("/missions/today"),
  completeTask: (missionId: string, taskId: string) => request<Mission>(`/missions/${missionId}/tasks/${taskId}/complete`, { method: "POST" }),
  addEvidence: (missionId: string, summary: string, evidence_type = "text") => request<{ id: string; summary: string }>(`/missions/${missionId}/evidence`, { method: "POST", body: JSON.stringify({ summary, evidence_type }) }),
  completeMission: (missionId: string) => request<Mission>(`/missions/${missionId}/complete`, { method: "POST" }),
  mentorChat: (message: string, mode: string) => request<{ answer: string }>("/mentor/chat", { method: "POST", body: JSON.stringify({ message, mode }) })
};
