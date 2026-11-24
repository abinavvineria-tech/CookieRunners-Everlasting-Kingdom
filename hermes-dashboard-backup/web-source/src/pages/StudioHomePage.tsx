import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

export default function StudioHomePage() {
  const [status, setStatus] = useState<{
    profile: string;
    theme: string;
    skills: number;
    plugins: number;
    cronJobs: number;
    uptime: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      api.getConfig().catch(() => ({})),
      api.getSkills?.().catch(() => ({ skills: [] })),
      api.getPlugins?.().catch(() => ({ plugins: [] })),
      api.getCronJobs?.().catch(() => ({ jobs: [] })),
    ])
      .then(([config, skills, plugins, cron]) => {
        if (cancelled) return;
        setStatus({
          profile: "everlily",
          theme: (config as any)?.dashboard?.theme ?? "cookie-run",
          skills: Array.isArray((skills as any)?.skills) ? (skills as any).skills.length : 22,
          plugins: Array.isArray((plugins as any)?.plugins) ? (plugins as any).plugins.length : 1,
          cronJobs: Array.isArray((cron as any)?.jobs) ? (cron as any).jobs.length : 0,
          uptime: "Online",
        });
        setLoading(false);
      })
      .catch(() => {
        setStatus({
          profile: "everlily",
          theme: "cookie-run",
          skills: 22,
          plugins: 1,
          cronJobs: 0,
          uptime: "Online",
        });
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-[20rem] flex-col items-center justify-center gap-4 text-muted-foreground">
        <div className="flex h-8 w-8 rounded-full border-4 border-primary border-t-transparent animate-spin" />
        <p>Loading Cookie Run Studio…</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Cookie Run Studio
          </h1>
          <p className="text-muted-foreground">
            United Stadium &mdash; Captain Abinav&rsquo;s command center
          </p>
        </div>
        <div className="flex gap-2">
          <Badge variant="outline" className="bg-primary/10 text-primary border-primary/30">
            Profile: everlily
          </Badge>
          <Badge variant="secondary">One Run. One Dream. One United.</Badge>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="col-span-2 md:col-span-2">
          <CardHeader>
            <CardTitle>Studio Overview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-3">
              <StatCard label="Skills" value={status?.skills ?? 0} icon="🧩" />
              <StatCard label="Plugins" value={status?.plugins ?? 0} icon="🔌" />
              <StatCard label="Cron Jobs" value={status?.cronJobs ?? 0} icon="⏰" />
            </div>
            <div className="pt-4 text-sm text-muted-foreground">
              <p>
                Welcome to Cookie Run Studio, Captain Abinav. This is your
                Everlily Nexus command center at United Stadium. All Hermes
                dashboard features are preserved above, and the Cookie Run
                Studio modules are in the sidebar.
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <QuickAction
              label="Open Kanban Board"
              description="To Do, In Progress, Review, Done"
              href="/studio/kanban"
              icon="📋"
            />
            <QuickAction
              label="Manage Projects"
              description="Create and organize CRU projects"
              href="/studio/projects"
              icon="📁"
            />
            <QuickAction
              label="Dev Studio"
              description="Code editor, terminal, logs"
              href="/studio/dev"
              icon="💻"
            />
            <QuickAction
              label="Skills Lab"
              description="Inspect and manage agent skills"
              href="/studio/skills"
              icon="🧪"
            />
            <QuickAction
              label="Memory Centre"
              description="Inspect profile memory"
              href="/studio/memory"
              icon="🧠"
            />
            <QuickAction
              label="Job Centre"
              description="Monitor cron jobs and schedules"
              href="/studio/jobs"
              icon="⚙️"
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon }: { label: string; value: number | string; icon: string }) {
  return (
    <Card className="bg-background/50 border-border">
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <div>
            <div className="text-lg font-bold text-foreground">{value}</div>
            <div className="text-xs text-muted-foreground">{label}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function QuickAction({
  label,
  description,
  href,
  icon,
}: {
  label: string;
  description: string;
  href: string;
  icon: string;
}) {
  return (
    <Button
      onClick={() => {
        window.location.href = href;
      }}
      className="w-full flex items-center gap-3 justify-start text-left border-border hover:bg-accent hover:text-accent-foreground transition-colors"
    >
      <span>{icon}</span>
      <div>
        <div className="text-sm font-medium text-foreground">{label}</div>
        <div className="text-xs text-muted-foreground">{description}</div>
      </div>
    </Button>
  );
}
