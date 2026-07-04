"use client";

import { useUIStore } from "@/lib/store/ui";

export function ReflectionEditor({ prompt }: { prompt: string }) {
  const draft = useUIStore((state) => state.draftReflection);
  const setDraft = useUIStore((state) => state.setDraftReflection);
  return (
    <div className="space-y-3">
      <p className="text-sm text-steel">{prompt}</p>
      <textarea className="min-h-32 w-full rounded-md border border-line bg-panel2 p-3 text-sm text-slate-100 outline-none focus:border-silver" value={draft} onChange={(event) => setDraft(event.target.value)} placeholder="What changed in your thinking today?" />
    </div>
  );
}
