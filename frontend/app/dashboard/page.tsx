"use client";

import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, RefreshCw } from "lucide-react";
import { AppShell } from "@/components/app-shell/AppShell";
import { MissionProgressBar } from "@/components/dashboard/MissionProgressBar";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { api } from "@/lib/api/client";

export default function DashboardPage() {
  const queryClient = useQueryClient();
  const dashboard = useQuery({ queryKey: ["dashboard"], queryFn: api.dashboard });
  const generate = useMutation({ mutationFn: api.generateRoadmap, onSuccess: () => queryClient.invalidateQueries({ queryKey: ["dashboard"] }) });
  const mission = dashboard.data?.today_mission;
  const completedTasks = mission?.tasks.filter((task) => task.status === "completed").length ?? 0;
  const totalTasks = mission?.tasks.length ?? 0;

  return (
    <AppShell>
      <div className="grid gap-4 xl:grid-cols-[1.35fr_.65fr]">
        <Card className="min-h-[320px]">
          <div className="mb-6 flex items-start justify-between gap-4">
            <div>
              <div className="text-sm text-steel">Today</div>
              <h1 className="mt-1 text-2xl font-semibold text-silver">{mission?.title ?? "No active mission"}</h1>
            </div>
            {mission ? (
              <Link href={`/mission/${mission.id}`}>
                <Button><ArrowRight className="h-4 w-4" /> Continue</Button>
              </Link>
            ) : (
              <Button onClick={() => generate.mutate()} disabled={generate.isPending}><RefreshCw className="h-4 w-4" /> Generate Roadmap</Button>
            )}
          </div>
          {mission && (
            <div className="space-y-5">
              <p className="max-w-3xl text-sm leading-6 text-slate-300">{mission.objective}</p>
              <MissionProgressBar completed={completedTasks} total={totalTasks} />
              <div className="grid gap-3 md:grid-cols-3">
                <Metric label="Difficulty" value={`${mission.difficulty}/5`} />
                <Metric label="Minutes" value={`${mission.estimated_minutes}`} />
                <Metric label="Topic" value={mission.learning_topic} />
              </div>
            </div>
          )}
        </Card>
        <div className="grid gap-4">
          <MetricCard label="Streak" value={`${dashboard.data?.streak ?? 0} days`} />
          <MetricCard label="Completed" value={`${dashboard.data?.completed_missions ?? 0} missions`} />
          <Card>
            <div className="text-sm text-steel">Skill focus</div>
            <div className="mt-3 flex flex-wrap gap-2">
              {(dashboard.data?.skill_focus ?? []).map((skill) => <span key={skill} className="rounded-md border border-silver/20 px-2 py-1 text-xs text-silver">{skill}</span>)}
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="rounded-md border border-line bg-panel2 p-3"><div className="text-xs text-steel">{label}</div><div className="mt-1 text-sm text-silver">{value}</div></div>;
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return <Card><div className="text-sm text-steel">{label}</div><div className="mt-2 text-2xl font-semibold text-silver">{value}</div></Card>;
}
