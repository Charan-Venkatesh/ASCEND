"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { LogIn, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { api } from "@/lib/api/client";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const auth = useMutation({
    mutationFn: () => mode === "login" ? api.login(email, password) : api.register(email, password, displayName || email.split("@")[0]),
    onSuccess: (data) => {
      window.localStorage.setItem("ascend_token", data.access_token);
      router.push("/dashboard");
    }
  });

  return (
    <main className="flex min-h-screen items-center justify-center bg-background p-4 text-slate-100">
      <Card className="w-full max-w-md">
        <div className="mb-6">
          <div className="text-sm text-steel">ASCEND OS</div>
          <h1 className="mt-1 text-2xl font-semibold text-silver">{mode === "login" ? "Sign in" : "Create account"}</h1>
        </div>
        <div className="space-y-3">
          <input className="h-10 w-full rounded-md border border-line bg-panel2 px-3 text-sm outline-none focus:border-silver" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="email" />
          {mode === "register" && <input className="h-10 w-full rounded-md border border-line bg-panel2 px-3 text-sm outline-none focus:border-silver" value={displayName} onChange={(event) => setDisplayName(event.target.value)} placeholder="display name" />}
          <input className="h-10 w-full rounded-md border border-line bg-panel2 px-3 text-sm outline-none focus:border-silver" type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="password" />
          <Button className="w-full" disabled={auth.isPending || !email || password.length < 10} onClick={() => auth.mutate()}>
            {mode === "login" ? <LogIn className="h-4 w-4" /> : <UserPlus className="h-4 w-4" />}
            {mode === "login" ? "Sign in" : "Create account"}
          </Button>
          {auth.error && <div className="text-sm text-red-300">{auth.error.message}</div>}
          <button className="text-sm text-steel hover:text-silver" onClick={() => setMode(mode === "login" ? "register" : "login")}>
            {mode === "login" ? "Create a new account" : "Use existing account"}
          </button>
        </div>
      </Card>
    </main>
  );
}
