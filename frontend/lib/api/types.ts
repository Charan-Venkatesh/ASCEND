export type ApiEnvelope<T> = { data: T; meta: Record<string, unknown>; errors: Array<{ code: string; message: string }> };

export type MissionTask = {
  id: string;
  type: string;
  title: string;
  instructions: string;
  skill_improved: string;
  completion_criteria: string;
  status: string;
};

export type Mission = {
  id: string;
  day_number: number;
  title: string;
  objective: string;
  business_context: string;
  learning_topic: string;
  practical_task: string;
  documentation_prompt: string;
  reflection_prompt: string;
  interview_question: string;
  difficulty: number;
  estimated_minutes: number;
  status: string;
  tasks: MissionTask[];
};

export type DashboardSnapshot = {
  streak: number;
  completed_missions: number;
  skill_focus: string[];
  review_due: string;
  today_mission: Mission | null;
};

export type AuthResponse = {
  access_token: string;
  token_type: string;
  user: { id: string; email: string; display_name: string; auth_provider: string };
};
