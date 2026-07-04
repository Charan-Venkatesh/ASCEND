"use client";

import { useState } from "react";
import { Upload } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function EvidenceUploader({ onSubmit, pending }: { onSubmit: (summary: string) => void; pending: boolean }) {
  const [summary, setSummary] = useState("");
  return (
    <div className="space-y-3">
      <textarea className="min-h-28 w-full rounded-md border border-line bg-panel2 p-3 text-sm text-slate-100 outline-none focus:border-silver" value={summary} onChange={(event) => setSummary(event.target.value)} placeholder="Capture lab output, GitHub link context, decision notes, or reviewer-ready evidence." />
      <Button disabled={pending || summary.trim().length < 5} onClick={() => onSubmit(summary)}>
        <Upload className="h-4 w-4" /> Attach Evidence
      </Button>
    </div>
  );
}
