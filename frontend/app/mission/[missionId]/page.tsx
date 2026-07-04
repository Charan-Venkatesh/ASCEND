"use client";

import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Check, ChevronLeft, Trophy } from "lucide-react";
import { AppShell } from "@/components/app-shell/AppShell";
import { MentorChat } from "@/components/mentor/MentorChat";
import { EvidenceUploader } from "@/components/mission/EvidenceUploader";
import { ReflectionEditor } from "@/components/mission/ReflectionEditor";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { api } from "@/lib/api/client";

export default function MissionPage({ params }: { params: { missionId: string } }) {
  const queryClient = useQueryClient();
  const missionQuery = useQuery({ queryKey: ["mission", params.missionId], queryFn: () => api.mission(params.missionId) });
  const completeTask = useMutation({ mutationFn: (taskId: string) => api.completeTask(params.missionId, taskId), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["mission", params.missionId] }) });
  const addEvidence = useMutation({ mutationFn: (summary: string) => api.addEvidence(params.missionId, summary), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["mission", params.missionId] }) });
  const completeMission = useMutation({ mutationFn: () => api.completeMission(params.missionId), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["dashboard"] }) });
  const mission = missionQuery.data;

  return (
    <AppShell>
      <div className="mb-4">
        <Link href="/dashboard" className="inline-flex items-center gap-2 text-sm text-steel hover:text-silver"><ChevronLeft className="h-4 w-4" /> Dashboard</Link>
      </div>
      {mission && (
        <div className="grid gap-4 xl:grid-cols-[1fr_380px]">
          <div className="space-y-4">
            <Card>
              <div className="text-sm text-steel">Day {mission.day_number}</div>
              <h1 className="mt-1 text-2xl font-semibold text-silver">{mission.title}</h1>
              <p className="mt-4 text-sm leading-6 text-slate-300">{mission.business_context}</p>
            </Card>
            <Card>
              <h2 className="mb-3 text-sm font-semibold text-silver">Execution Checklist</h2>
              <div className="space-y-2">
                {mission.tasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between gap-3 rounded-md border border-line bg-panel2 p-3">
                    <div>
                      <div className="text-sm text-slate-100">{task.title}</div>
                      <div className="mt-1 text-xs text-steel">{task.completion_criteria}</div>
                    </div>
                    <Button className="h-8" disabled={task.status === "completed" || completeTask.isPending} onClick={() => completeTask.mutate(task.id)}>
                      <Check className="h-4 w-4" /> {task.status === "completed" ? "Done" : "Complete"}
                    </Button>
                  </div>
                ))}
              </div>
            </Card>
            <Card>
              <h2 className="mb-3 text-sm font-semibold text-silver">Evidence</h2>
              <EvidenceUploader pending={addEvidence.isPending} onSubmit={(summary) => addEvidence.mutate(summary)} />
            </Card>
            <Card>
              <h2 className="mb-3 text-sm font-semibold text-silver">Reflection</h2>
              <ReflectionEditor prompt={mission.reflection_prompt} />
            </Card>
          </div>
          <aside className="space-y-4">
            <Card>
              <h2 className="mb-3 text-sm font-semibold text-silver">Interview Question</h2>
              <p className="text-sm leading-6 text-slate-300">{mission.interview_question}</p>
            </Card>
            <Card>
              <h2 className="mb-3 text-sm font-semibold text-silver">Mentor</h2>
              <MentorChat />
            </Card>
            <Button className="w-full" onClick={() => completeMission.mutate()} disabled={completeMission.isPending}>
              <Trophy className="h-4 w-4" /> Complete Mission
            </Button>
          </aside>
        </div>
      )}
    </AppShell>
  );
}
