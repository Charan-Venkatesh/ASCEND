import Link from "next/link";
import { Activity, Brain, Gauge, Map, Settings } from "lucide-react";

const nav = [
  { href: "/dashboard", label: "Dashboard", icon: Gauge },
  { href: "/roadmap", label: "Roadmap", icon: Map },
  { href: "/mentor", label: "Mentor", icon: Brain },
  { href: "/reviews", label: "Reviews", icon: Activity },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-slate-100">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-panel2/80 p-4 lg:block">
        <div className="mb-8 border-b border-line pb-4 text-lg font-semibold text-silver">ASCEND OS</div>
        <nav className="space-y-1">
          {nav.map((item) => (
            <Link key={item.href} href={item.href} className="flex h-10 items-center gap-3 rounded-md px-3 text-sm text-steel hover:bg-silver/10 hover:text-silver">
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="lg:pl-64">
        <div className="border-b border-line bg-background/95 px-6 py-4">
          <div className="text-xs uppercase text-steel">Enterprise AI Career Command Center</div>
        </div>
        <div className="p-4 md:p-6">{children}</div>
      </main>
    </div>
  );
}
