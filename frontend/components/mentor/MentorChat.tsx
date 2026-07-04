"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { api } from "@/lib/api/client";
import { useUIStore } from "@/lib/store/ui";

export function MentorChat() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const mode = useUIStore((state) => state.mentorMode);
  const setMode = useUIStore((state) => state.setMentorMode);
  const chat = useMutation({ mutationFn: () => api.mentorChat(message, mode), onSuccess: (data) => setAnswer(data.answer) });

  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        {(["mentor", "strict", "review"] as const).map((item) => (
          <button key={item} onClick={() => setMode(item)} className={`h-8 rounded-md border px-3 text-xs ${mode === item ? "border-silver bg-silver text-black" : "border-line text-steel"}`}>{item}</button>
        ))}
      </div>
      <textarea className="min-h-24 w-full rounded-md border border-line bg-panel2 p-3 text-sm text-slate-100 outline-none focus:border-silver" value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Ask for critique, a sharper architecture angle, or interview coaching." />
      <Button onClick={() => chat.mutate()} disabled={chat.isPending || message.trim().length === 0}><Send className="h-4 w-4" /> Ask Mentor</Button>
      {answer && <div className="rounded-md border border-silver/20 bg-black/20 p-3 text-sm leading-6 text-slate-200">{answer}</div>}
    </div>
  );
}
